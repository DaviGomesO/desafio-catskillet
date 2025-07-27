from rest_framework import serializers
from tasks.models import Task  # , Category
from django.contrib.auth import get_user_model


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Não retornar a senha

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

# class CategoryModelSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = Category
#     fields = '__all__'


class TaskModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # fields = '__all__'
        fields = ['id', 'title', 'description', 'execution_date', 'status', 'categories']
