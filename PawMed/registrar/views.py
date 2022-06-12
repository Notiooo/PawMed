from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.datetime_safe import datetime
from django.views.generic import TemplateView, FormView, DetailView, UpdateView, CreateView
from .forms import PatientBoardForm, AppointmentForm
from .models import Patient, Visit
from doctor.models import Doctor, DoctorSpecialization, Specialization


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
        user_id = form.find_patient().first().id
        self.request.session['patient-submitted-id'] = user_id
        return redirect('registrar_patient', pk=user_id)


class AddAppointmentView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """View in which a registrant can schedule a patient for an appointment"""
    template_name = 'registrar/add_appointment.html'
    form_class = AppointmentForm

    def test_func(self):
        return self.request.user.role == 'REGISTRAR'

    def get_context_data(self, **kwargs):
        context = super(AddAppointmentView, self).get_context_data(**kwargs)

        patient_pk = self.kwargs['patient_pk']
        context['patient'] = get_object_or_404(Patient, pk=patient_pk)
        return context

    def form_valid(self, form):
        """Data is passed to the next view via a session"""

        self.request.session["add_appointment_view_redirect"] = True
        self.request.session["specialization_id"] = int(form.cleaned_data['specialization'])
        self.request.session["patient_pk"] = self.kwargs['patient_pk']
        self.request.session["earliest_date"] = form.cleaned_data['earliest_date'].strftime('%Y-%m-%d')
        self.request.session["latest_date"] = form.cleaned_data['latest_date'].strftime('%Y-%m-%d')

        if form.cleaned_data['doctor']:
            self.request.session["doctor_id"] = form.cleaned_data['doctor']

        return redirect('registrar_appointment_doctor_list')


def load_doctors(request):
    """Reads a list of doctors in a particular specialty. Returns as an option for the <select> field."""

    specialization_id = request.GET.get('specialization')
    doctor_specializations = DoctorSpecialization.objects.filter(specialization=specialization_id)
    doctors = [doctor.doctorid for doctor in doctor_specializations]
    return render(request, 'registrar/hr/doctors_dropdown_list_options.html', {'doctors': doctors})


class AppointmentDoctorFreeVisitsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Displays free visits based on specified filters"""
    template_name = 'registrar/appointment_doctor_list.html'

    def dispatch(self, request, *args, **kwargs):
        """If someone has refreshed the page it will go back to adding appointment view"""

        if 'add_appointment_view_redirect' not in self.request.session and 'patient-submitted-id' in self.request.session:
            return redirect('registrar_add_appointment', patient_pk=self.request.session['patient-submitted-id'])

        return super(AppointmentDoctorFreeVisitsView, self).dispatch(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.role == 'REGISTRAR' and 'add_appointment_view_redirect' in self.request.session

    def get_context_data(self, **kwargs):
        """
        It takes the data needed to filter the results from the form.
        The form passes it through sessions.
        """
        context = super(AppointmentDoctorFreeVisitsView, self).get_context_data(**kwargs)
        del self.request.session['add_appointment_view_redirect']

        context['specialization'] = get_object_or_404(Specialization, pk=self.request.session.pop('specialization_id', None))
        context['patient'] = get_object_or_404(Patient, pk=self.request.session.pop('patient_pk', None))
        context['earliest_date'] = datetime.strptime(self.request.session.pop('earliest_date'), '%Y-%m-%d').date()
        context['latest_date'] = datetime.strptime(self.request.session.pop('latest_date'), '%Y-%m-%d').date()

        doctor_id = self.request.session.pop('doctor_id', None)
        if doctor_id:
            context['doctor'] = get_object_or_404(Doctor, pk=doctor_id)

        return context


class RegistrarOnlyAuthorizedView(LoginRequiredMixin, UserPassesTestMixin):
    """View in which a role of registrant is tested"""
    login_url = 'login'

    def test_func(self):
        return self.request.user.role == 'REGISTRAR'


class RegistrarOnlyAuthorizedPatientView(RegistrarOnlyAuthorizedView):
    patient_pk = 'pk'

    def test_func(self):
        return super(RegistrarOnlyAuthorizedPatientView, self).test_func() \
               and 'patient-submitted-id' in self.request.session\
               and self.request.session['patient-submitted-id'] == self.kwargs[self.patient_pk]


class AddPatientView(RegistrarOnlyAuthorizedView, CreateView):
    """View in which the registrant can add a new patient to the database"""
    template_name = 'registrar/add_patient.html'
    model = Patient
    fields = ['name', 'surname', 'personid', 'birth_date', 'gender', 'phone_number', 'city', 'zip_code']

    def form_valid(self, form):
        new_patient = form.save(commit=False)

        new_id = 0
        last_object = Patient.objects.all().last()
        if last_object:
            new_id = last_object.id + 1

        new_patient.id = new_id
        form.save()
        return redirect('registrar_patient_board')

    def test_func(self):
        return self.request.user.role == 'REGISTRAR'


class PatientView(RegistrarOnlyAuthorizedPatientView, DetailView):
    """View in which the registrant can see patients data"""
    model = Patient
    template_name = 'registrar/patient_profile.html'
    login_url = 'login'
    context_object_name = 'patient'

    def get_context_data(self, **kwargs):
        """
        If the form has not saved a user id in the session it will
        throw a 404. If the form id is incompatible with the id we are trying
        to display it will also return a 404.
        """
        context = super(PatientView, self).get_context_data(**kwargs)
        context['visit_list'] = Visit.objects.filter(patient__id=self.get_object().id)

        return context


class EditPatientView(RegistrarOnlyAuthorizedPatientView, UpdateView):
    """View in which the registrant can edit the patients data"""
    model = Patient
    template_name = 'registrar/edit_patient.html'
    fields = ['name', 'surname', 'personid', 'birth_date', 'gender', 'phone_number', 'city', 'zip_code']


def delete_visit(request, **kwargs):
    get_object_or_404(Visit, id=kwargs['visit_id']).delete()
    return JsonResponse({'status': "deleted"})


class InfoVisitView(RegistrarOnlyAuthorizedView, DetailView):
    """View in which the registrant can check the details of the visit"""
    model = Visit
    template_name = 'registrar/appointment_info.html'
    login_url = 'login'
    context_object_name = 'visit'

    def test_func(self):
        return super(InfoVisitView, self).test_func() \
               and 'patient-submitted-id' in self.request.session\
               and self.request.session['patient-submitted-id'] == self.get_object().patient.pk