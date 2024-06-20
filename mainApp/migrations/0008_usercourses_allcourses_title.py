# Generated by Django 4.0 on 2024-06-19 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0007_allcourses'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCourses',
            fields=[
                ('usercourseid', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=50)),
                ('coursename', models.CharField(default='none', max_length=1000)),
                ('title', models.CharField(default='none', max_length=1000)),
                ('content', models.TextField(default='no content...')),
                ('videolink', models.URLField(default='https://www.youtube.com/')),
                ('seen', models.CharField(default='0', max_length=2)),
            ],
        ),
        migrations.AddField(
            model_name='allcourses',
            name='title',
            field=models.CharField(default='none', max_length=1000),
        ),
    ]
