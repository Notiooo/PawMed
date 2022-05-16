from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    list_display = ['username', 'first_name', 'last_name', 'email', 'role', 'phone_number']
    list_editable = ['role']
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin) 