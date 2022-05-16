from django.contrib.auth.views import LoginView
from django.urls import path
from . import views


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('redirect', views.RedirectView.as_view(), name='redirect'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('no_role/', views.NoRoleView.as_view(), name='no_role')
]
