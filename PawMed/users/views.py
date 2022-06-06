from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import generic, View
from rest_framework import viewsets

from .forms import CustomUserCreationForm, CustomUserAssignRole
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.contrib.auth.decorators import login_required

from doctor.models import Doctor, Technician


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
            return HttpResponseRedirect(reverse('doctor'))
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


class AdminAssigningRolesListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    """Displays a list of users without a role to whom the admin can assign a role."""
    model = CustomUser
    template_name = 'users/admin.html'
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        return CustomUser.objects.filter(role__isnull=True, is_superuser=False)


class AdminAssigningRolesUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    """View allowing to assign a role to particular user"""
    model = CustomUser
    template_name = 'users/admin_update_role.html'
    form_class = CustomUserAssignRole
    login_url = 'login'

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy('admin_roles')

    def form_valid(self, form):
        """Additionally, it removes the old role object and creates a new one"""
        form_user_pk = self.kwargs['pk']
        form_user = CustomUser.objects.get(id=form_user_pk)
        selected_new_role = form.cleaned_data.get('role')

        self.delete_role_object_if_user_has_role(form_user, form_user_pk)

        all_role_name_to_object = {
            "DOCTOR": Doctor,
            "LAB_TECHNICIAN": Technician,
            "LAB_MANAGER": Technician
        }

        for any_role_name, any_role_object in all_role_name_to_object.items():
            if selected_new_role == any_role_name:
                self.create_role_object(any_role_object, form_user)

        return super().form_valid(form)

    def delete_role_object_if_user_has_role(self, form_user, pk):
        """Deletes the role object this user was previously associated with"""

        user_have_object = {
            "DOCTOR": Doctor.objects.filter(custom_user_id=pk),
            "LAB_TECHNICIAN": Technician.objects.filter(custom_user_id=pk),
            "LAB_MANAGER": Technician.objects.filter(custom_user_id=pk)
        }
        found_object = user_have_object.get(form_user.role, [])
        if found_object:
            found_object.delete()

    def create_role_object(self, new_role_object, user):
        """Creates a role object corresponding to the currently newly selected role."""

        new_id = 0
        last_object = new_role_object.objects.all().last()

        if last_object:
            new_id = last_object.id + 1

        created = new_role_object.objects.create(
            id=new_id,
            name=user.first_name,
            surname=user.last_name,
            custom_user_id=user.id
        )
        created.save()


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = CustomUserSerializer
