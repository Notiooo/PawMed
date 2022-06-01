from django.shortcuts import render, get_object_or_404
<<<<<<< HEAD
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from datetime import datetime

from . import models

# Create your views here.

class DoctorHomepageView(ListView):
    model = models.Visit
=======

from django.views.generic import ListView, DetailView, UpdateView
from datetime import datetime

from registrar.models import Visit
from . import models


class DoctorHomepageView(ListView):
    model = Visit
>>>>>>> master
    template_name = 'doctor/doctor_homepage.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        today = datetime.today()
        year = today.year
        month = today.month
        day = today.day

        # Define a query for visits that are scheduled today and haven't took place, order by time 
<<<<<<< HEAD
        self.query = models.Visit.objects.filter(tookplace=False, date__year = year,
=======
        self.query = Visit.objects.filter(took_place=False, date__year = year,
>>>>>>> master
                                                date__month=month, date__day=day).order_by('date__time')

        #current patient is the first query result
        if(self.query.__len__() > 0):
            context['current_patient'] = self.query[0]
            #Next visits are the rest of queries
            context['visit_list'] = self.query[1:]
<<<<<<< HEAD
        else:
            context['visit_list'] = None
        return context

class DoctorEndVisitView(UpdateView):
    model = models.Visit
    template_name = 'doctor/doctor_endvisit.html'
    fields=['tookplace']
    success_url = reverse_lazy('doctor_homepage')

    def form_valid(self, form):
        form.instance.tookplace = True
        return super(DoctorEndVisitView, self).form_valid(form)

class DoctorAppointmentView(UpdateView):
    model = models.Visit
    template_name = 'doctor/doctor_visit.html'
    fields=['medical_interview', 'examination', 'remarks', 'recommendation', 'tookplace']
    success_url = reverse_lazy('doctor_homepage')

    def form_valid(self, form):
        form.instance.tookplace = True
        return super(DoctorAppointmentView, self).form_valid(form)


class DoctorOrderTestView(CreateView):
    #There probably has to be some changes to test model
    #for now execution date and executive are in the form
    model = models.Test
    template_name = 'doctor/doctor_order_test.html'
    fields = ['type', 'remarks', 'execution_date', 'executive']
    success_url = reverse_lazy('doctor_homepage')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.query = models.Visit.objects.get(pk=self.kwargs['pk'])
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
        form.instance.visit = models.Visit.objects.get(id=self.kwargs.get('pk'))
        return super(DoctorOrderTestView, self).form_valid(form)

class DoctorPatienHistoryView(ListView):
    model = models.Visit
    template_name = 'doctor/doctor_patient_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        currentVisit = models.Visit.objects.get(id=self.kwargs['pk'])
        context["prev_visits"] = models.Visit.objects.filter(tookplace=True, patient=currentVisit.patient).order_by('date') 
        return context
    
=======
        return context

class DoctorEndVisitView(UpdateView):
    model = Visit
    template_name = 'doctor/doctor_endvisit.html'
    fields=['took_place']

    # No way for getting back form this view now as get_absolute_url is not defined
    # but it makes the neccessary change in database

class DoctorAppointmentView(UpdateView):
    model = Visit
    template_name = 'doctor/doctor_visit.html'
    fields=['medical_interview', 'examination', 'remarks', 'recommendation', 'took_place']
>>>>>>> master
