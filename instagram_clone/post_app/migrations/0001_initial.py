# Generated by Django 3.2 on 2021-07-30 05:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_pic', models.ImageField(upload_to='post_pic', verbose_name='Image')),
                ('post_caption', models.TextField(max_length=264, verbose_name='Caption')),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('edited_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_date',),
            },
        ),
        migrations.CreateModel(
            name='SavedPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('save_date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_save', to='post_app.posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_save', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-save_date',),
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_like', to='post_app.posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_like', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=264, verbose_name='Add a Comment...')),
                ('comment_date', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comment', to='post_app.posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
