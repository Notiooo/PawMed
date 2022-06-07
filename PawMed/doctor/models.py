from django.db import models


class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    room = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=30)
    custom_user_id = models.IntegerField(blank=True, null=True)

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
    name = models.CharField(max_length=30, blank=True, null=True)
    drug_form = models.CharField(max_length=30, blank=True, null=True)
    num_of_packages = models.CharField(max_length=10, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    REFOUND=(
        (5, '5%'),
        (10, '10%'),
        (15, '15%'),
        (50, '50%'),
        (100, '100%')
    )
    refound_percentage = models.IntegerField(blank=True, null=True, choices=REFOUND)


    class Meta:
        managed = False
        db_table = 'prescription'


class Specialization(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'specialization'


