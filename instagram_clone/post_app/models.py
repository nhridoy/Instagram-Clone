from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts')
    post_pic = models.ImageField(upload_to='post_pic', verbose_name="Image")
    post_caption = models.TextField(max_length=264, verbose_name="Caption")
    slug = models.SlugField(max_length=250, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}s post"

    class Meta:
        ordering = ('-created_date',)


class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='post_comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    comment = models.CharField(max_length=264, verbose_name='Add a Comment...')
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\'s comment on {self.post}'


class Likes(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='post_like')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')

    def __str__(self):
        return f'{self.user.username}\'s Likes on {self.post}'


class SavedPost(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='post_save')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_save')
    save_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\' save {self.post}'

    class Meta:
        ordering = ('-save_date',)
