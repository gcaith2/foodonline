# Generated by Django 4.2.11 on 2024-04-21 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_role_choice_user_role_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cover_photos',
            field=models.ImageField(blank=True, null=True, upload_to='users/cover_photos'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='users/profile_pictures'),
        ),
    ]
