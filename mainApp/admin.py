from django.contrib import admin
from .models import Skill,Education,WorkExperience,CareerInfo, NotificationData, UserGitRepos, AllCourses, MyCareerDisplay, MyCareerDetailed, MyCareerTaskDetailed, MyRecCareer, CraeerSearch, QuizDetails

admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(WorkExperience)
admin.site.register(CareerInfo)
admin.site.register(NotificationData)
admin.site.register(UserGitRepos)
admin.site.register(AllCourses)
admin.site.register(MyCareerDisplay)
admin.site.register(MyCareerDetailed)
admin.site.register(MyCareerTaskDetailed)
admin.site.register(MyRecCareer)
admin.site.register(CraeerSearch)
admin.site.register(QuizDetails)

# Register your models here.
