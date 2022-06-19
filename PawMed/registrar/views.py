from datetime import timedelta

from dateutil.rrule import rrule, DAILY, MINUTELY
from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.datetime_safe import datetime
from django.views import generic
from django.views.generic import FormView, DetailView, UpdateView, ListView, CreateView
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

        self.request.session["specialization_id"] = int(form.cleaned_data['specialization'])
        self.request.session["patient_pk"] = self.kwargs['patient_pk']
        self.request.session["earliest_date"] = form.cleaned_data['earliest_date'].strftime('%Y-%m-%d')
        self.request.session["latest_date"] = form.cleaned_data['latest_date'].strftime('%Y-%m-%d')

        if form.cleaned_data['doctor']:
            self.request.session["doctor_id"] = form.cleaned_data['doctor']
        else:
            self.request.session["doctor_id"] = None

        return redirect('registrar_appointment_doctor_list')


class AppointmentDoctorFreeVisitsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """Displays free visits based on specified filters"""
    template_name = 'registrar/appointment_doctor_list.html'
    paginate_by = 10
    context_object_name = 'possible_visits'

    def get_queryset(self):
        earliest_date = datetime.strptime(self.request.session['earliest_date'], '%Y-%m-%d').date()
        latest_date = datetime.strptime(self.request.session['latest_date'], '%Y-%m-%d').date()
        specialization_id = self.request.session['specialization_id']
        found_doctor_ids = DoctorSpecialization.objects.filter(specialization_id=specialization_id).values_list('doctorid', flat=True)

        found_visits = Visit.objects.filter(
            date__gte=earliest_date,
            date__lte=latest_date,
            doctor__in=found_doctor_ids
        )

        if self.request.session['doctor_id'] is not None:
            found_doctor_ids = self.request.session['doctor_id']
            found_visits = found_visits.filter(doctor=self.request.session['doctor_id'])

        possible_visits = []

        for day in rrule(freq=DAILY, dtstart=earliest_date, until=latest_date):

            start_day = day.replace(hour=8, minute=0)
            end_day = day.replace(hour=16, minute=0)
            for visit_time in rrule(freq=MINUTELY, interval=30, dtstart=start_day, until=end_day):
                for doctor_id in found_doctor_ids:
                    if found_visits.filter(
                            doctor=doctor_id,
                            date=visit_time,
                            took_place=False).count() == 0:
                        possible_visits.append({'doctor': get_object_or_404(Doctor, pk=doctor_id),
                                                'visit_start': visit_time,
                                                'visit_end': (visit_time + timedelta(minutes=30))})
        possible_visits = sorted(possible_visits, key=lambda x: x['visit_start'])
        return possible_visits

    def test_func(self):
        return self.request.user.role == 'REGISTRAR' \
               and all(elem in self.request.session
                       for elem in ['patient-submitted-id', 'specialization_id', 'patient_pk',
                                    'earliest_date', 'latest_date'])

    def get_context_data(self, **kwargs):
        """
        It takes the data needed to filter the results from the form.
        The form passes it through sessions.
        """
        context = super(AppointmentDoctorFreeVisitsView, self).get_context_data(**kwargs)

        context['specialization'] = get_object_or_404(Specialization, pk=self.request.session['specialization_id'])
        context['patient'] = get_object_or_404(Patient, pk=self.request.session['patient_pk'])
        context['earliest_date'] = datetime.strptime(self.request.session['earliest_date'], '%Y-%m-%d').date()
        context['latest_date'] = datetime.strptime(self.request.session['latest_date'], '%Y-%m-%d').date()

        doctor_id = self.request.session['doctor_id']
        if doctor_id is not None:
            context['doctor'] = get_object_or_404(Doctor, pk=self.request.session['doctor_id'])

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
        context['visit_list'] = Visit.objects.filter(patient__id=self.get_object().id).order_by('date')

        return context


class EditPatientView(RegistrarOnlyAuthorizedPatientView, UpdateView):
    """View in which the registrant can edit the patients data"""
    model = Patient
    template_name = 'registrar/edit_patient.html'
    fields = ['name', 'surname', 'personid', 'birth_date', 'gender', 'phone_number', 'city', 'zip_code']


class LoadDoctorsView(RegistrarOnlyAuthorizedView, generic.View):
    """Loads all doctors with the selected specialization"""
    def get(self, request, *args, **kwargs):
        return self.load_doctors(request, **kwargs)

    def load_doctors(self, request, **kwargs):
        """Reads a list of doctors in a particular specialty. Returns as an option for the <select> field."""

        specialization_id = request.GET.get('specialization')
        doctor_specializations = DoctorSpecialization.objects.filter(specialization=specialization_id)
        doctors = [doctor.doctorid for doctor in doctor_specializations]
        return render(request, 'registrar/hr/doctors_dropdown_list_options.html', {'doctors': doctors})


class CreateVisitView(RegistrarOnlyAuthorizedView, generic.View):
    """This view creates a new visit"""
    def get(self, request, *args, **kwargs):
        return self.create_visit(request, **kwargs)

    def create_visit(self, request, **kwargs):
        """Creates a new visit record in the database"""
        new_id = 0
        last_object = Visit.objects.all().last()
        if last_object:
            new_id = last_object.id + 1

        start_date = kwargs['start_date']
        room = kwargs['doctor_room']
        doctor = get_object_or_404(Doctor, id=kwargs['doctor_id'])
        patient = get_object_or_404(Patient, id=kwargs['patient_id'])

        Visit.objects.create(id=new_id, doctor=doctor, patient=patient, date=start_date, took_place=False, room=room)
        return HttpResponse("Visit added to db")


class DeleteVisitView(RegistrarOnlyAuthorizedView, generic.View):
    """This view deletes selected visit"""
    def get(self, request, *args, **kwargs):
        return self.delete_visit(request, **kwargs)

    def delete_visit(self, request, **kwargs):
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