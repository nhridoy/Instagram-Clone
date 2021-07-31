from django.urls import path
from profile_app import views

app_name = 'profile_app'

urlpatterns = [
    path('login/', views.loginview, name='login'),
    path('register/', views.registerview, name='register'),
    path('logout/', views.logoutview, name='logout'),
    path('profile/', views.UserProfileView, name='profile'),
    path('edit-profile/<user_name>/', views.editprofileview, name='edit-profile'),
    path('change-password/', views.passchangeview, name='change-password'),
    path('user/<str:user_name>/', views.OtherUserProfileView, name='user'),
    path('follow/<str:user_name>/', views.userfollowview, name='follow'),
    path('search/', views.searchview, name='search'),
]
