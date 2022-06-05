from django.urls import path

from .views import PatientBoardView, AddAppointmentView, AddPatientView, PatientView, load_doctors, \
    AppointmentDoctorFreeVisitsView

urlpatterns = [
    path('', PatientBoardView.as_view(), name="registrar_patient_board"),
    path('add_patient/', AddPatientView.as_view(), name="registrar_add_patient"),
    path('appointment/<int:patient_pk>/', AddAppointmentView.as_view(), name="registrar_add_appointment"),
    path('appointment/doctor_list/', AppointmentDoctorFreeVisitsView.as_view(), name="registrar_appointment_doctor_list"),
    path('patient/<int:pk>/', PatientView.as_view(), name="registrar_patient"),

    path('ajax/load-doctors/', load_doctors, name='ajax_load_doctors')
]