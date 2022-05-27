from django.urls import path

from . import views

urlpatterns = [
    path('', views.DoctorHomepageView.as_view(), name='doctor_homepage'),
    path('<int:pk>/end/', views.DoctorEndVisitView.as_view(), name='doctor_endvisit'),
]