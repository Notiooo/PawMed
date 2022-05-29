from django.urls import path

from .views import PatientBoardView, AddAppointmentView, AddPatientView

urlpatterns = [
    path('', PatientBoardView.as_view(), name="registrar_patient_board"),
    path('add_patient/', AddPatientView.as_view(), name="registrar_add_patient"),
    path('appointment/', AddAppointmentView.as_view(), name="registrar_add_appointment")
]