from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.core.cache import cache

from tasks.models import Task  # , Category
from tasks.serializers import RegisterSerializer, TaskModelSerializer  # , CategoryModelSerializer
from tasks.filters import TaskFilter
from tasks.permissions import TaskOwnerPermission


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    queryset = get_user_model().objects.all()


# class CategoryModelViewSet(viewsets.ModelViewSet):
#   queryset = Category.objects.all()
#   serializer_class = CategoryModelSerializer


class TaskModelViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskModelSerializer
    permission_classes = [IsAuthenticated, TaskOwnerPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_queryset(self):
        # Apenas objetos do usuário
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        cache.delete_pattern(f'*agenda_{self.request.user.id}*')

    def perform_update(self, serializer):
        instance = serializer.save()
        cache.delete_pattern(f'*agenda_{self.request.user.id}*')

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete_pattern(f'*agenda_{self.request.user.id}*')

    # Cria o endpoint dentro do projeto para retornar as tarefas do usuário
    @action(detail=False, methods=['get'], url_path='agenda')
    def agenda(self, request):
        cache_key = f'agenda_{request.user.id}'
        data = cache.get(cache_key)
        if data is not None:
            return Response(data)

        tasks = self.get_queryset()
        tasks = self.filter_queryset(tasks)
        tasks = tasks.order_by('execution_date')
        page = self.paginate_queryset(tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            cache.set(cache_key, data, timeout=60 * 5)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(tasks, many=True)

        cache.set(cache_key, data, timeout=60 * 5)
        return Response(serializer.data, status=status.HTTP_200_OK)
