from django.urls import path

from .views import PatientBoardView, AddAppointmentView, AddPatientView, PatientView, EditPatientView, \
    InfoVisitView, LoadDoctorsView, CreateVisitView, DeleteVisitView
from .views import AppointmentDoctorFreeVisitsView

urlpatterns = [
    path('', PatientBoardView.as_view(), name="registrar_patient_board"),
    path('add_patient/', AddPatientView.as_view(), name="registrar_add_patient"),
    path('appointment/<int:patient_pk>/', AddAppointmentView.as_view(), name="registrar_add_appointment"),
    path('appointment/doctor_list/', AppointmentDoctorFreeVisitsView.as_view(), name="registrar_appointment_doctor_list"),
    path('patient/<int:pk>/', PatientView.as_view(), name="registrar_patient"),
    path('info/<int:pk>/', InfoVisitView.as_view(), name="appointment_info"),
    path('edit_patient/<int:pk>/', EditPatientView.as_view(), name="edit_patient"),
    path('ajax/load-doctors/', LoadDoctorsView.as_view(), name='ajax_load_doctors'),
    path('ajax/create-visit/<int:doctor_id>/<int:patient_id>/<start_date>/<doctor_room>/',
         CreateVisitView.as_view(), name='ajax_create_visit'),
    path('ajax/delete-visit/<int:visit_id>/', DeleteVisitView.as_view(), name='ajax_delete_visit')
]