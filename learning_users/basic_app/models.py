from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfileInfo(models.Model):


    # use to add information that the default user does not have
    user= models.OneToOneField(User)

    #additional
    portfolio_site=models.URLField(blank=True)


    profile_pic=models.ImageField(upload_to='profile_pics',blank=True)
    #need to have 'profile_pics' be a sub directory within the media director

    def __str__(self):
        return self.user.username
