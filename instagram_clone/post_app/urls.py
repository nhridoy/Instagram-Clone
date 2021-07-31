from django.urls import path
from post_app import views

app_name = 'post_app'

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('post-save/', views.postsaveview, name='post-save'),
    path('like/<slug:slug_name>/', views.likeview, name='like'),
    path('save/<slug:slug_name>/', views.saveview, name='save'),
    path('edit-post/<slug:slug_name>/', views.EditPostView, name='edit-post'),
    path('delete-post/<slug:slug_name>/', views.DeletePostView.as_view(), name='delete-post'),
    path('post/<slug:slug_name>/', views.PostView, name='post'),
]
