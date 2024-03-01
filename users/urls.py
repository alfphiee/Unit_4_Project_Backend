from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.UserViewSet, basename='user')
urlpatterns = [
  path('', include(router.urls)),
  path('<int:user_id>/add_photo/', views.AddPhotoView.as_view(), name='add_photo')
]
