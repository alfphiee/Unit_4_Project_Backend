from .models import Project, Task
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields= '__all__'
        read_only_fields = ('project',)

    def create(self, validated_data):
        project_id = self.context['project_id']
        return Task.objects.create(project_id=project_id, **validated_data)

