from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.ProjectViewSet, basename='project')

project_router = routers.NestedDefaultRouter(router, '', lookup='project')
project_router.register('tasks', views.TaskViewSet, basename='project-tasks')

urlpatterns = router.urls + project_router.urls
