from django.contrib import admin
from .models import Skill,Education,WorkExperience,CareerInfo, NotificationData, UserGitRepos, AllCourses

admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(CareerInfo)
admin.site.register(NotificationData)
admin.site.register(UserGitRepos)
admin.site.register(AllCourses)

# Register your models here.
