from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView, DetailView
from .forms import PatientBoardForm
from .models import Patient


class PatientBoardView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """View where registrar can search for a patient by name and ID"""
    template_name = 'registrar/patient_board.html'
    form_class = PatientBoardForm
    login_url = 'login'

    def test_func(self):
        return self.request.user.role == 'REGISTRAR'

    def form_valid(self, form):
        """
        To session stores the id of the current patient.
        This ensures that only this profile can be viewed by
        the registrar and by no other id will the registrar get a profile view.
        """
        user_id = form.find_patient().first().pk
        self.request.session['patient-submitted-id'] = user_id
        return redirect('registrar_patient', pk=user_id)


class AddAppointmentView(TemplateView):
    """View in which a registrant can schedule a patient for an appointment"""
    template_name = 'registrar/add_appointment.html'


class AddPatientView(TemplateView):
    """View in which the registrant can add a new patient to the database"""
    template_name = 'registrar/add_patient.html'


class PatientView(DetailView, LoginRequiredMixin, UserPassesTestMixin):
    """View in which the registrant can see patients data"""
    model = Patient
    template_name = 'registrar/patient.html'
    context_object_name = 'patient'
    login_url = 'login'

    def test_func(self):
        return self.request.user.role == 'REGISTRAR'

    def get_context_data(self, **kwargs):
        """
        If the form has not saved a user id in the session it will
        throw a 404. If the form id is incompatible with the id we are trying
        to display it will also return a 404.
        """
        context = super(PatientView, self).get_context_data(**kwargs)

        if 'patient-submitted-id' not in self.request.session or self.request.session['patient-submitted-id'] != self.request.user.pk:
            raise Http404

        return context
