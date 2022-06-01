from django.contrib import admin

from . import models

admin.site.register(models.Doctor)
admin.site.register(models.Specialization)
admin.site.register(models.DoctorSpecialization)
admin.site.register(models.Prescription)

