from django.urls import path

from .views import SubmitResultView

urlpatterns = [
    path('', SubmitResultView.as_view(), name="technician_submit_result")
]