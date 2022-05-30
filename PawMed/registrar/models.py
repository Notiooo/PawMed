from django.db import models
from doctor.models import Doctor


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    registration_date = models.DateTimeField()
    age = models.IntegerField()
    phone_number = models.CharField(max_length=30)
    birth_date = models.DateTimeField()
    city = models.CharField(max_length=85)
    zip_code = models.CharField(max_length=10)
    gender = models.CharField(max_length=1)
    personid = models.CharField(max_length=50)

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