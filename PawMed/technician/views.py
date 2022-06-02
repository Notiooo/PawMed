from django.views.generic import TemplateView, ListView, UpdateView, FormView
from django.urls import reverse_lazy
from datetime import datetime
from django.template.response import TemplateResponse

from . import models
from registrar.models import Visit, Patient
from doctor.models import Doctor

class SubmitResultView(UpdateView):
    """View where technician can add and then submit the result"""
    model = models.Test
    template_name = 'technician/submit_results.html'
    fields = ['status']
    success_url = reverse_lazy('technician_home')


    def testdex(request, template_name = 'technician/patient_information.html'):
        args = {}
        args["patient"] = self.get_object().visit.patient
        return TemplateResponse(request, template_name, args)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["test"] = self.get_object()
        context["visit"] = self.get_object().visit
        context["doctor"] = self.get_object().visit.doctor
        return context

    def form_valid(self, form):
        #now this for some reason doesn't work
        #I suspect it has something to do with the choise choosing
        # cus otherwiese the form doesn't get validation on sending
        # form.instance.status = ('c', 'Closed')
        # form.instance.execution_date = datetime.today()
        return super(SubmitResultView, self).form_valid(form)


class HeadTechnicianApprovalView(UpdateView):
    """View where technician can add and then submit the result"""
    template_name = 'technician/approval_view.html'
    fields = ['status']
    model = models.Test

    def testdex(request, template_name = 'technician/patient_information.html'):
        args = {}
        args["patient"] = self.get_object().visit.patient
        return TemplateResponse(request, template_name, args)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["test"] = self.get_object()
        context["visit"] = self.get_object().visit
        context["doctor"] = self.get_object().visit.doctor
        return context

class TechnicianHomepageView(ListView):
    """View where technicians can see tests of all states """
    template_name = 'technician/technician_homepage.html'
    model = models.Test

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pending_tests"] = models.Test.objects.filter(status='p')
        context["recently_closed"] = models.Test.objects.filter(status='c')[:10]
        return context
    


class HeadTechnicianHomepageView(ListView):
    """ view where technician head can see all closed but not approved tests """
    template_name = 'technician/technician_head_homepage.html'
    model = models.Test

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["closed_tests"] = models.Test.objects.filter(status='c')
        return context