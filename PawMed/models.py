# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    surname = models.TextField()
    room = models.IntegerField()
    phone_number = models.TextField()

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


class Laboratory(models.Model):
    id = models.IntegerField(primary_key=True)
    room = models.IntegerField()
    type = models.TextField()

    class Meta:
        managed = False
        db_table = 'laboratory'


class Patient(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    surname = models.TextField()
    registration_date = models.DateTimeField()
    age = models.IntegerField()
    phone_number = models.TextField()
    birth_date = models.DateTimeField()
    city = models.TextField()
    zip_code = models.IntegerField()
    gender = models.CharField(max_length=1)
    personid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'patient'


class Prescription(models.Model):
    id = models.IntegerField(primary_key=True)
    visit = models.ForeignKey('Visit', models.DO_NOTHING, db_column='visit')
    date_of_issue = models.DateTimeField()
    expiration_date = models.DateTimeField()
    remarks = models.TextField()

    class Meta:
        managed = False
        db_table = 'prescription'


class Specialization(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'specialization'


class Technician(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    surname = models.TextField()

    class Meta:
        managed = False
        db_table = 'technician'


class Test(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.TextField()
    execution_date = models.DateTimeField()
    executive = models.ForeignKey(Technician, models.DO_NOTHING, db_column='executive')
    remarks = models.TextField()
    laboratory_room = models.ForeignKey(Laboratory, models.DO_NOTHING, db_column='laboratory_room')
    visit = models.ForeignKey('Visit', models.DO_NOTHING, db_column='visit')

    class Meta:
        managed = False
        db_table = 'test'


class Visit(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='doctor')
    patient = models.ForeignKey(Patient, models.DO_NOTHING, db_column='patient')
    date = models.DateTimeField()
    room = models.IntegerField()
    remarks = models.TextField()
    diagnosis = models.TextField()
    medical_interview = models.TextField()
    examination = models.TextField()
    recommendation = models.TextField()

    class Meta:
        managed = False
        db_table = 'visit'
