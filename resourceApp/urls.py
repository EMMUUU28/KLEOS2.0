from django.contrib import admin
from django.urls import path, include
# from .views import talkpdf, talkpdf1, category,ar
from django.conf import settings
from . import views
from django.conf.urls.static import static

urlpatterns = [
    # path("resume/", views.talkpdf, name="talkpdf"),


    # path('roadmap/',views.roadmap,name='roadmap'),
    # path('downloadroadmap/',views.downloadroadmap,name='downloadroadmap'),
    # path('resumeassistant/', views.resumeassistant, name='resumeassistant'),
    # path('studyplan/', views.studyplan, name='studyplan'),

    # path("ar", ar, name="ar"),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)