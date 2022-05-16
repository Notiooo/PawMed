from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('DOCTOR', 'Doctor'),
        ('LAB_TECHNICIAN', 'Lab technician'),
        ('LAB_MANAGER', 'Lab manager'),
        ('REGISTRAR', 'Registrar'),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')
    role = models.CharField(max_length=14, choices=ROLE_CHOICES,  blank=True, null=True)
