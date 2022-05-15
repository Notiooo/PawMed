from django.views.generic import CreateView
from rest_framework import viewsets

from .forms import CustomUserCreationForm
from .models import CustomUser
from .serializers import CustomUserSerializer

# Create your views here.


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer


class SignUpView(CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm


