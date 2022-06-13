from django.contrib.auth.views import LoginView
from django.urls import path
from . import views


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('redirect', views.RedirectView.as_view(), name='redirect'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('no_role/', views.NoRoleView.as_view(), name='no_role'),
    path('admin/', views.AdminAssigningRolesListView.as_view(), name='admin_roles'),
    path('admin-doctor/', views.AdminDoctorListView.as_view(), name='admin_doctors'),
    path('admin/<int:pk>/', views.AdminAssigningRolesUpdateView.as_view(), name='admin_roles_update'),
    path('admin-doctor-update/<int:pk>/', views.AdminDoctorUpdateView.as_view(), name='admin_doctor_update'),
    path('admin-doctor-specialization-update/<int:pk>/', views.AdminDoctorSpecializationUpdateView.as_view(),
         name='admin_doctor_specialization_update'),
    path('ajax/delete-doctor-specialization/<int:doctor_specialization_id>/', views.delete_doctor_specialization,
         name="ajax_doctor_specialization_delete"),
    path('ajax/add-doctor-specialization/<int:specialization_id>/<int:doctor_id>/', views.add_doctor_specialization,
         name="ajax_doctor_specialization_add")

]
