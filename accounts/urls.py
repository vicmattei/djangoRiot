from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', views.UserCreateView.as_view(), name='register'),
]
