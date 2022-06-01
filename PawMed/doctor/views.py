from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from datetime import datetime

from . import models
from registrar.models import Visit, Patient

# Create your views here.

class DoctorHomepageView(ListView):
    model = Visit
    template_name = 'doctor/doctor_homepage.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        today = datetime.today()
        year = today.year
        month = today.month
        day = today.day

        # Define a query for visits that are scheduled today and haven't took place, order by time 
        self.query = Visit.objects.filter(took_place=False, date__year = year,
                                                date__month=month, date__day=day).order_by('date__time')

        #current patient is the first query result
        if(self.query.__len__() > 0):
            context['current_patient'] = self.query[0]
            #Next visits are the rest of queries
            context['visit_list'] = self.query[1:]
        else:
            context['visit_list'] = None
        return context

class DoctorEndVisitView(UpdateView):
    model = Visit
    template_name = 'doctor/doctor_endvisit.html'
    fields=['took_place']
    success_url = reverse_lazy('doctor_homepage')

    def form_valid(self, form):
        form.instance.took_place = True
        return super(DoctorEndVisitView, self).form_valid(form)

class DoctorAppointmentView(UpdateView):
    model = Visit
    template_name = 'doctor/doctor_visit.html'
    fields=['medical_interview', 'examination', 'remarks', 'recommendation', 'took_place']
    success_url = reverse_lazy('doctor_homepage')

    def form_valid(self, form):
        form.instance.took_place = True
        return super(DoctorAppointmentView, self).form_valid(form)


class DoctorOrderTestView(CreateView):
    #There probably has to be some changes to test model
    #for now execution date and executive are in the form
    model = models.Test
    template_name = 'doctor/doctor_order_test.html'
    fields = ['type', 'remarks']
    success_url = reverse_lazy('doctor_homepage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.query = Visit.objects.get(pk=self.kwargs['pk'])
        context['visit'] = self.query
        return context

    def form_valid(self, form):
        # for some reaseon negative indexing is not supported
        # so that's why it is done this way
        lastTest = models.Test.objects.all().order_by('id').reverse()
        if (len(lastTest) != 0):
            form.instance.id = lastTest[0].id + 1
        else:
            form.instance.id = 1
        form.instance.visit = Visit.objects.get(id=self.kwargs.get('pk'))
        return super(DoctorOrderTestView, self).form_valid(form)

class DoctorPatienHistoryView(ListView):
    model = Visit
    template_name = 'doctor/doctor_patient_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currentVisit = Visit.objects.get(id=self.kwargs['pk'])
        context["prev_visits"] = Visit.objects.filter(took_place=True, patient=currentVisit.patient).order_by('date') 
        return context
    
