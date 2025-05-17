from django.urls import path
from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]