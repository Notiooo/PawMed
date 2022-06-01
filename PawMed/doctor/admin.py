from django.contrib import admin

from . import models
<<<<<<< HEAD
# Register your models here.

admin.site.register(models.Doctor)

admin.site.register(models.Specialization)

admin.site.register(models.DoctorSpecialization)

admin.site.register(models.Patient)

admin.site.register(models.Visit)

admin.site.register(models.Prescription)

admin.site.register(models.Test)

admin.site.register(models.Laboratory)

=======

admin.site.register(models.Doctor)
admin.site.register(models.Specialization)
admin.site.register(models.DoctorSpecialization)
admin.site.register(models.Prescription)
admin.site.register(models.Test)
admin.site.register(models.Laboratory)
>>>>>>> master
admin.site.register(models.Technician)
