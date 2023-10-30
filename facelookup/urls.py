from django.contrib import admin
from django.urls import path
from facelookup import views
from .views import index, success_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='faceDetective'),
    path('success/', success_view, name='success'),
    path('video_feed/', views.video_feed, name='video_feed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)