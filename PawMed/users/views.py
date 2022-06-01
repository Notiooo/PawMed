from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic, View
from rest_framework import viewsets

from .forms import CustomUserCreationForm
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.contrib.auth.decorators import login_required


class RegisterView(generic.CreateView):
    template_name = 'users/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')


@method_decorator([login_required], name='dispatch')
class RedirectView(View):
    """ The class responsible for redirecting the authenticated user to the
        appropriate application upon login. The application is selected based
        on his current role assigned by the administrator."""

    def dispatch(self, request, *args, **kwargs):
        role = CustomUser.objects.filter(username=request.user.username).get().role
        if role == 'DOCTOR':
            return HttpResponseRedirect(reverse('doctor_homepage'))
        elif role == 'LAB_TECHNICIAN':
            return HttpResponseRedirect(reverse('lab_technician'))
        elif role == 'LAB_MANAGER':
            return HttpResponseRedirect(reverse('lab_manager'))
        elif role == 'REGISTRAR':
            return HttpResponseRedirect(reverse('homepage'))

        return HttpResponseRedirect(reverse('no_role'))


@method_decorator([login_required], name='dispatch')
class NoRoleView(generic.TemplateView):
    """The class responsible for redirecting a user who has not been assigned a role."""

    template_name = 'users/no_role.html'

    def dispatch(self, request, *args, **kwargs):
        role = CustomUser.objects.filter(username=request.user.username).get().role
        if role:
            return HttpResponseRedirect(reverse('redirect'))
        return super().dispatch(request, args, kwargs)



class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer

