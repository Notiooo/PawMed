from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

from doctor.models import Doctor, Technician


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('DOCTOR', 'Doctor'),
        ('LAB_TECHNICIAN', 'Lab technician'),
        ('LAB_MANAGER', 'Lab manager'),
        ('REGISTRAR', 'Registrar'),
    )

    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True, help_text='Contact phone number')
    role = models.CharField(max_length=14, choices=ROLE_CHOICES, blank=True, null=True)

    def role_object(self):
        switcher = {
            "DOCTOR": Doctor.objects.filter(custom_user_id=self.id).first(),
            "LAB_TECHNICIAN": Technician.objects.filter(custom_user_id=self.id).first(),
            "LAB_MANAGER": Technician.objects.filter(custom_user_id=self.id).first(),
            "REGISTRAR": self
        }
        return switcher.get(self.role, [])