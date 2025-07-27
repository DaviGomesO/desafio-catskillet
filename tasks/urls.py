from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tasks.views import TaskModelViewSet  # , CategoryModelViewSet

router = DefaultRouter()
# router.register('categories', CategoryModelViewSet) ## Possivelmente não precise dessa por ser apenas em /admin
router.register('tasks', TaskModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
