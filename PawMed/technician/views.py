from django.views.generic import TemplateView


class SubmitResultView(TemplateView):
    """View where technician can add and then submit the result"""
    template_name = 'technician/submit_results.html'


class HeadTechnicianApprovalView(TemplateView):
    """View where technician can add and then submit the result"""
    template_name = 'technician/approval_view.html'