# Generated by Django 4.0 on 2024-06-19 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_usergitrepos'),
    ]

    operations = [
        migrations.AddField(
            model_name='careerinfo',
            name='user_name',
            field=models.CharField(default='none', max_length=50),
        ),
        migrations.AddField(
            model_name='usergitrepos',
            name='user_name',
            field=models.CharField(default='none', max_length=50),
        ),
    ]
