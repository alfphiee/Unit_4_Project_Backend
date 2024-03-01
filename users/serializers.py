from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Photo

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['url', 'user']
        
class UserSerializer(serializers.ModelSerializer):
    photo_set = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'photo_set']

    def get_photo_set(self, obj):
        # Assuming each user has at most one photo. Adjust logic as needed for multiple photos.
        photo = Photo.objects.filter(user=obj).first()
        return photo.url if photo else None