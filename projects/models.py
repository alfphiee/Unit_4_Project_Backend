from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    STATUS_CHOICES = [
        ('PL', 'Planning'),
        ('IP', 'In Progress'),
        ('CO', 'Completed'),
        ('OH', 'On Hold')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects')
    collaborators = models.ManyToManyField(User, related_name='projects', blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='PL')
    github_url = models.URLField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Task(models.Model):
    STATUS_CHOICES = [
        ('TD', 'To Do'),
        ('IP', 'In Progress'),
        ('CO', 'Completed')
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    start_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='TD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        self.title