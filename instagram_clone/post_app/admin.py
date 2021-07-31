from django.contrib import admin
from post_app.models import Posts, Comments, Likes, SavedPost

# Register your models here.
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(Likes)
admin.site.register(SavedPost)
