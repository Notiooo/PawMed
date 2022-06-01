from django.views.generic import TemplateView, ListView

from . import models

class SubmitResultView(TemplateView):
    """View where technician can add and then submit the result"""
    template_name = 'technician/submit_results.html'


class HeadTechnicianApprovalView(TemplateView):
    """View where technician can add and then submit the result"""
    template_name = 'technician/approval_view.html'

class TechnicianHomepageView(ListView):
    """View where technicians can see tests of all states """
    template_name = 'technician/technician_homepage.html'
    model = models.Test