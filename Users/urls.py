from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import EmailBasedPasswordResetForm

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),

    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        form_class=EmailBasedPasswordResetForm,
        template_name='main/password_reset.html',
    ), name='password_reset'),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='main/password_reset_sent.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'),
         name='password_reset_complete'),
]