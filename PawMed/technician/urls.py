from django.urls import path

from .views import SubmitResultView, HeadTechnicianApprovalView, TechnicianHomepageView, HeadTechnicianHomepageView

urlpatterns = [
    path('<int:pk>/submit/', SubmitResultView.as_view(), name="technician_submit_result"),
    path('<int:pk>/approval/', HeadTechnicianApprovalView.as_view(), name="head_technician_approval_view"),
    path('home/', TechnicianHomepageView.as_view(), name='technician_home'),
    path('head/', HeadTechnicianHomepageView.as_view(), name='head_home'),
]