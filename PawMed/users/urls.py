from django.contrib.auth.views import LoginView
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', views.SignUpView.as_view(), name='signup'),
]