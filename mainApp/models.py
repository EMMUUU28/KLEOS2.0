from django.db import models
from django.contrib.auth.models import User  # Import the User model from Django's built-in authentication system

class PersonalInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link to a user
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    about = models.CharField(max_length=200)
    # Add more fields as needed for personal information

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link to a user
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=100)
    start_date = models.CharField(max_length=7,blank=True, null=True)  
    end_date = models.CharField(max_length=7,blank=True, null=True)
    # Add more fields as needed for education details

class WorkExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link to a user
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField()
    # Add more fields as needed for work experience

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ForeignKey to link to a user
    skill_name = models.CharField(max_length=100)
    # Add more fields as needed for skills

class CareerInfo(models.Model):
    user_name   = models.CharField(max_length=50, default='none')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_year = models.CharField(max_length=10)
    dream_role = models.CharField(max_length=255)
    linkedin_link = models.URLField(blank=True)
    github_link = models.URLField(blank=True)


class UserGitRepos(models.Model):
    gid         = models.AutoField(primary_key=True)
    user_name   = models.CharField(max_length=50, default='none')
    title       = models.CharField(max_length=400, default='none')
    description = models.TextField(default='no description...')
    github_link = models.URLField(blank=True)


class AllCourses(models.Model):
    courseid        = models.AutoField(primary_key=True)
    coursename      = models.CharField(max_length=1000, default='none')
    thumbnail      = models.CharField(max_length=1000, default='none')
    description       = models.TextField(default='no content...')
    videolink       = models.URLField(default='https://www.youtube.com/')

    def __str__(self):
        return f"{self.courseid} - {self.coursename} - coursename: {self.coursename} - title: {self.title}"

class AllCourses(models.Model):
    courseid        = models.AutoField(primary_key=True)
    coursename      = models.CharField(max_length=1000, default='none')
    title      = models.CharField(max_length=1000, default='none')
    content         = models.TextField(default='no content...')
    videolink       = models.URLField(default='https://www.youtube.com/')

    def __str__(self):
        return f"{self.courseid} - {self.coursename} - coursename: {self.coursename} - title: {self.title}"


class UserCourses(models.Model):
    usercourseid    = models.AutoField(primary_key=True)
    user_name   = models.CharField(max_length=50)

    coursename      = models.CharField(max_length=1000, default='none')
    title           = models.CharField(max_length=1000, default='none')
    content         = models.TextField(default='no content...')
    videolink       = models.URLField(default='https://www.youtube.com/')
    seen            = models.CharField(max_length=2, default='0') # 0 = unseen or 1 = seen 
    def __str__(self):
        return f"{self.usercourseid} - {self.user_name} - coursename: {self.coursename} - title: {self.title} - seen: {self.seen}"




class NotificationData(models.Model):
    eid         = models.AutoField(primary_key=True)
    user_name   = models.CharField(max_length=50)

    emailid     = models.CharField(max_length=100)
    fav         = models.CharField(max_length=2, default='0') # 0 or 1 
    seen        = models.CharField(max_length=2, default='0') # 0 = unseen or 1 = seen 
    
    title       = models.TextField(default='none')    # markdown content
    content     = models.TextField(default='none')  # markdown content
    
    timestamp   = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.eid} - {self.user_name} - emailid: {self.emailid} - timestamp: {self.timestamp} - title: {self.title}"




    # YYYY-MM-DD : 2025-07-10