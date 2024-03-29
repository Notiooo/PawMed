import pytz
from django.db import models
from django.urls import reverse
from doctor.models import Doctor


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    registration_date = models.DateTimeField(auto_now_add=True, blank=True)
    phone_number = models.CharField(max_length=30)
    birth_date = models.DateField()
    city = models.CharField(max_length=85)
    zip_code = models.CharField(max_length=10)
    personid = models.CharField(max_length=50)

    GENDER = (
        ('f', 'Female'),
        ('m', 'Male')
    )

    gender = models.CharField(max_length=1, choices=GENDER)

    def get_absolute_url(self):
        return reverse('registrar_patient', args=[str(self.id)])

    def __str__(self):
        return self.name + " " + self.surname

    class Meta:
        managed = False
        db_table = 'patient'


class Visit(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='doctor')
    patient = models.ForeignKey(Patient, models.DO_NOTHING, db_column='patient')
    date = models.DateTimeField()
    room = models.CharField(max_length=10)
    remarks = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    medical_interview = models.TextField(blank=True, null=True)
    examination = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    took_place = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'visit'

    def __str__(self):
        return str(self.date) + " at " + self.room