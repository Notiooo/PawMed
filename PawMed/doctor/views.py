from django.shortcuts import render, get_object_or_404

from django.views.generic import ListView, DetailView, UpdateView
from datetime import datetime

from registrar.models import Visit
from . import models


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
