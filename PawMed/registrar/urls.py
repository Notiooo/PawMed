from django.urls import path

from .views import PatientBoardView, AddAppointmentView

urlpatterns = [
    path('', PatientBoardView.as_view(), name="registrar_patient_board"),
    path('appointment/', AddAppointmentView.as_view(), name="registrar_add_appointment")
]