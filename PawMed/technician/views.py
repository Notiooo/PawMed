from django.views.generic import TemplateView, ListView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from datetime import datetime
from django.template.response import TemplateResponse

from . import models
from registrar.models import Visit, Patient
from doctor.models import Doctor

class SubmitResultView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View where technician can add and then submit the result"""
    model = models.Test
    template_name = 'technician/submit_results.html'
    fields = ['lab_remarks']
    success_url = reverse_lazy('technician_home')

    def test_func(self):
        return self.request.user.role == 'LAB_TECHNICIAN' or self.request.user.role == 'LAB_MANAGER'

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
        #now it works too good, even with back button
        form.instance.status = 'c'
        form.instance.execution_date = datetime.today()
        return super(SubmitResultView, self).form_valid(form)


class HeadTechnicianApprovalView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View where technician can add and then submit the result"""
    template_name = 'technician/approval_view.html'
    fields = ['status']
    model = models.Test
    success_url = reverse_lazy('head_home')

    def test_func(self):
        return self.request.user.role == 'LAB_MANAGER'

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


class TechnicianHomepageView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """View where technicians can see tests of all states """
    template_name = 'technician/technician_homepage.html'
    model = models.Test

    def test_func(self):
        return self.request.user.role == 'LAB_TECHNICIAN' or self.request.user.role == 'LAB_MANAGER'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pending_tests"] = models.Test.objects.filter(status='p')
        context["recently_closed"] = models.Test.objects.filter(status='c')[:10]
        return context
    


class HeadTechnicianHomepageView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """ view where technician head can see all closed but not approved tests """
    template_name = 'technician/technician_head_homepage.html'
    model = models.Test

    def test_func(self):
        return self.request.user.role == 'LAB_MANAGER'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["closed_tests"] = models.Test.objects.filter(status='c')
        context["recent_tests"] = models.Test.objects.filter().order_by("execution_date")
        return context