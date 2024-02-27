from .models import Project, Task
from rest_framework import permissions, viewsets
from django.db.models import Q

from .serializers import *

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user = self.request.user.id
        return Project.objects.filter(Q(owner=user) | Q(collaborators=user)).distinct()
    

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs['project_pk'])

    def get_serializer_context(self):
        return {'project_id': self.kwargs['project_pk']}
