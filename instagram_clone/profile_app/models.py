from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Making Email Field Unique
User._meta.get_field('email')._unique = True


# Create your models here.
class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_details')
    profile_pic = models.ImageField(upload_to='profile_pic', verbose_name='Profile Picture', blank=True)
    dob = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
    about_user = models.TextField(max_length=264, verbose_name='About You', blank=True)
    website = models.URLField(max_length=100, verbose_name='Website', blank=True)
    facebook = models.URLField(max_length=100, verbose_name='Facebook', blank=True)

    def __str__(self):
        return f'{self.user.username} details'


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')

    def __str__(self):
        return f'{self.follower} is following {self.following}'
