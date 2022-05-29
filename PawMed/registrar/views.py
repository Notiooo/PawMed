from django.views.generic import TemplateView


class PatientBoardView(TemplateView):
    """View where registrar can search for a patient by name and ID"""
    template_name = 'registrar/patient_board.html'

class AddAppointmentView(TemplateView):
    """View in which a registrant can schedule a patient for an appointment"""
    template_name = 'registrar/add_appointment.html'

class AddPatientView(TemplateView):
    """View in which the registrant can add a new patient to the database"""
    template_name = 'registrar/add_patient.html'
