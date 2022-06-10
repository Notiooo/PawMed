from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from datetime import datetime

from . import models
from registrar.models import Visit, Patient
from technician.models import Test

# Create your views here.

class DoctorHomepageView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """View where doctors seee all the patients appointed at given day, sorted by appointment hour """
    model = Visit
    template_name = 'doctor/doctor_homepage.html'
    login_url = 'login'

    def test_func(self):
        return self.request.user.role == 'DOCTOR'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        doctor = self.request.user.role_object()

        today = datetime.today()
        year = today.year
        month = today.month
        day = today.day

        # Define a query for visits that are scheduled today and haven't took place, order by time 
        self.query = Visit.objects.filter(took_place=False, doctor=doctor, date__year = year,
                                                date__month=month, date__day=day).order_by('date__time')

        #current patient is the first query result
        if(self.query.__len__() > 0):
            context['current_patient'] = self.query[0]
            #Next visits are the rest of queries
            context['visit_list'] = self.query[1:]
        else:
            context['visit_list'] = None
        return context

class DoctorEndVisitView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View where doctor can simply mark that the visit has taken place """
    model = Visit
    template_name = 'doctor/doctor_endvisit.html'
    fields=['took_place']
    success_url = reverse_lazy('doctor_homepage')

    def test_func(self):
        return self.request.user.role == 'DOCTOR'

    def form_valid(self, form):
        form.instance.took_place = True
        return super(DoctorEndVisitView, self).form_valid(form)

class DoctorAppointmentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View where doctor can write informations about patients """
    template_name = 'doctor/doctor_visit_exam.html'
    model = Visit
    fields=['medical_interview', 'diagnosis', 'examination', 'remarks', 'recommendation', 'took_place']
    success_url = reverse_lazy('doctor_homepage')

    def test_func(self):
        return self.request.user.role == 'DOCTOR'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # visit = get_object_or_404(Visit, pk=self.kwargs['pk'])
        # visit = Visit.objects.get(pk=self.kwargs['pk'])

        visit = self.get_object()
        context["visit"] = visit
        context["prev_visits"] = Visit.objects.filter(took_place=True, patient=visit.patient).order_by('date')
        context["prev_lab_tests"] = Test.objects.filter(status='a', visit__patient = visit.patient).order_by('execution_date')
        return context
    

    def form_valid(self, form):
        #This thing dosen't work as it should
        #But we'll worry 'bout it later!
        form.instance.took_place = True
        return super(DoctorAppointmentView, self).form_valid(form)



class DoctorOrderTestView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """View where doctors can order different types of tests """
    model = Test
    template_name = 'doctor/doctor_visit_test.html'
    fields = ['type', 'remarks']
    success_url = reverse_lazy('doctor_homepage')

    def test_func(self):
        return self.request.user.role == 'DOCTOR'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.query = Visit.objects.get(pk=self.kwargs['pk'])
        context['visit'] = self.query
        return context

    def form_valid(self, form):
        # for some reaseon negative indexing is not supported
        # so that's why it is done this way
        lastTest = Test.objects.all().order_by('id').reverse()
        if (len(lastTest) != 0):
            form.instance.id = lastTest[0].id + 1
        else:
            form.instance.id = 1
        form.instance.visit = Visit.objects.get(id=self.kwargs.get('pk'))
        form.instance.status = 'p'
        return super(DoctorOrderTestView, self).form_valid(form)

class DoctorPatientHistoryView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """View where doctors can see all the previous visits of a given patient """
    model = Visit
    template_name = 'doctor/doctor_visit_history.html'

    def test_func(self):
        return self.request.user.role == 'DOCTOR'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currentVisit = Visit.objects.get(id=self.kwargs['pk'])
        context["visit"] = currentVisit
        context["prev_visits"] = Visit.objects.filter(took_place=True, patient=currentVisit.patient).order_by('date') 
        return context
    
class DoctorCreatePrescriptionView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = models.Prescription
    template_name = 'doctor/doctor_visit_prescription.html'
    success_url = reverse_lazy('doctor_homepage')
    fields = ['name', 'drug_form', 
            'num_of_packages', 'refound_percentage', 'remarks']

    def test_func(self):
        return self.request.user.role == 'DOCTOR'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.query = Visit.objects.get(pk=self.kwargs['pk'])
        context['visit'] = self.query
        context['prev_presc'] = models.Prescription.objects.filter(visit__patient=self.query.patient).order_by('date_of_issue')
        return context

    def form_valid(self, form):
        expirationDate = datetime.today()
        expirationDate.replace(year = expirationDate.year + 1)

        form.instance.date_of_issue = datetime.today()
        form.instance.expiration_date = expirationDate

        lastPresc = models.Prescription.objects.all().order_by('id').reverse()
        if len(lastPresc) != 0:
            form.instance.id = lastPresc[0].id + 1
        else:
            form.instance.id = 0

        form.instance.visit = Visit.objects.get(id=self.kwargs.get('pk'))
        return super(DoctorCreatePrescriptionView, self).form_valid(form)

    
