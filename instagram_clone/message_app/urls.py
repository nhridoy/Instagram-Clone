from django.urls import path
from message_app import views

app_name = 'message_app'

urlpatterns = [
    path('inbox/', views.inboxview, name='inbox'),
    path('message/<str:user_name>/', views.messageview, name='message'),
]
