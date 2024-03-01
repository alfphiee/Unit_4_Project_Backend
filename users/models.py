from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Photo(models.Model):
  url = models.CharField(max_length=200)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for user_id {self.user.id} @ {self.url}"