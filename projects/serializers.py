from .models import Project, Task
from users.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import serializers

class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    collaborators_emails = serializers.ListField(child=serializers.EmailField(), write_only=True, required=False)
    collaborators = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'status', 'github_url', 'created_at', 'updated_at', 'owner', 'collaborators', 'collaborators_emails']

    def create(self, validated_data):
        collaborators_emails = validated_data.pop('collaborators_emails', [])
        user = self.context['request'].user
        project = Project.objects.create(**validated_data, owner=user)
        self._update_collaborators(project, collaborators_emails)
        return project

    def update(self, instance, validated_data):
        collaborators_emails = validated_data.pop('collaborators_emails', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        self._update_collaborators(instance, collaborators_emails)
        return instance

    def _update_collaborators(self, project, emails):
        if emails:
            collaborators = []
            for email in emails:
                try:
                    user = User.objects.get(email=email)
                    collaborators.append(user)
                except User.DoesNotExist:
                    pass
            project.collaborators.set(collaborators)

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
        representation = super(TaskSerializer, self).to_representation(instance)
        representation['assignee'] = UserSerializer(instance.assignee).data if instance.assignee else None
        return representation