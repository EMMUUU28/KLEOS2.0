
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views 
urlpatterns = [
    path("",views.index,name='index'),
    path("profile/",views.profile,name='profile'),
    path("updateprofile/",views.updateprofile,name='updateprofile'),
    path("updateworkexp/",views.updateworkexp,name='updateworkexp'),
    path("updateeducation/",views.updateeducation,name='updateeducation'),
    path("updateskills/",views.updateskills,name='updateskills'),
    path("studymaterials/",views.studymaterials,name='studymaterials'),
    path("calendar/",views.calendar,name='calendar'),

    path("updateprofile_resume/",views.updateprofile_resume,name='updateprofile_resume'),
    path("updatecareerinfo/",views.updatecareerinfo,name='updatecareerinfo')
]
