from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.Test)
admin.site.register(models.Laboratory)
admin.site.register(models.Technician)