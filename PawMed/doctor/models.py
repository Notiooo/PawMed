from django.db import models


class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    room = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'doctor'


class DoctorSpecialization(models.Model):
    id = models.IntegerField(primary_key=True)
    doctorid = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='doctorid')
    specialization = models.ForeignKey('Specialization', models.DO_NOTHING, db_column='specialization')

    class Meta:
        managed = False
        db_table = 'doctor_specialization'


class Prescription(models.Model):
    id = models.IntegerField(primary_key=True)
    visit = models.ForeignKey('registrar.Visit', models.DO_NOTHING, db_column='visit')
    date_of_issue = models.DateTimeField()
    expiration_date = models.DateTimeField()
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prescription'


class Specialization(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'specialization'


