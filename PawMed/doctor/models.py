from django.db import models

# Create your models here.

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


class Laboratory(models.Model):
    id = models.IntegerField(primary_key=True)
    room = models.CharField(max_length=10)
    type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'laboratory'


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


class Prescription(models.Model):
    id = models.IntegerField(primary_key=True)
    visit = models.ForeignKey('Visit', models.DO_NOTHING, db_column='visit')
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


class Technician(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'technician'


class Test(models.Model):
    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=50)
    execution_date = models.DateTimeField()
    executive = models.ForeignKey(Technician, models.DO_NOTHING, db_column='executive')
    remarks = models.TextField(blank=True, null=True)
    laboratory_room = models.ForeignKey(Laboratory, models.DO_NOTHING, db_column='laboratory_room', blank=True, null=True)
    visit = models.ForeignKey('Visit', models.DO_NOTHING, db_column='visit')

    class Meta:
        managed = False
        db_table = 'test'


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
    tookplace = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'visit'