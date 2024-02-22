from .models import Project
from rest_framework import permissions, viewsets

from .serializers import *

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer