from .models import Project, Task
from users.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    collaborators = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'status', 'github_url', 'created_at', 'updated_at', 'owner', 'collaborators']


class TaskSerializer(serializers.ModelSerializer):
    assignee_id = serializers.IntegerField(allow_null=True, required=False, write_only=True)
    assignee = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('project',)

    def create(self, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        project_id = self.context['project_id']
        if assignee_id is not None:
            validated_data['assignee'] = User.objects.get(id=assignee_id)
        return Task.objects.create(project_id=project_id, **validated_data)

    def to_representation(self, instance):
        """Modify the representation of the serializer to include user details."""
        representation = super(TaskSerializer, self).to_representation(instance)
        representation['assignee'] = UserSerializer(instance.assignee).data if instance.assignee else None
        return representation