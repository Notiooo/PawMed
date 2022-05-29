# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey('UsersCustomuser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    room = models.IntegerField()
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
    room = models.IntegerField()
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
    zip_code = models.IntegerField()
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


class UsersCustomuser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    email = models.CharField(unique=True, max_length=254)
    phone_number = models.CharField(max_length=128)
    role = models.CharField(max_length=14, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_customuser'


class UsersCustomuserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_customuser_groups'
        unique_together = (('customuser', 'group'),)


class UsersCustomuserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    customuser = models.ForeignKey(UsersCustomuser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_customuser_user_permissions'
        unique_together = (('customuser', 'permission'),)


class Visit(models.Model):
    id = models.IntegerField(primary_key=True)
    doctor = models.ForeignKey(Doctor, models.DO_NOTHING, db_column='doctor')
    patient = models.ForeignKey(Patient, models.DO_NOTHING, db_column='patient')
    date = models.DateTimeField()
    room = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)
    diagnosis = models.TextField(blank=True, null=True)
    medical_interview = models.TextField(blank=True, null=True)
    examination = models.TextField(blank=True, null=True)
    recommendation = models.TextField(blank=True, null=True)
    tookplace = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'visit'
