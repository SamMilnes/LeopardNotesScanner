from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')


'''
User Profile Model
Each user who signs up will have its own profile and it will be stored in the database as such
'''


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    gender = models.TextField(blank=True)
    location = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    age = models.TextField(blank=True)
    sleeping_habits = models.TextField(blank=True)
    number_of_roommates = models.TextField(blank=True)
    personality_types = models.TextField(blank=True)
    interests = models.TextField(blank=True)
    ocr_option = models.CharField(max_length=10, choices=[('text', 'Text'), ('math', 'Math')])


    def __str__(self):
        return self.user.username

