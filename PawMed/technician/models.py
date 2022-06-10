from django.db import models

# Create your models here.

class Laboratory(models.Model):
    id = models.IntegerField(primary_key=True)
    room = models.CharField(max_length=10)
    type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'laboratory'

class Technician(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    custom_user_id = models.IntegerField(blank=True, null=True)

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
    visit = models.ForeignKey('registrar.Visit', models.DO_NOTHING, db_column='visit')

    STATUS = (
        ('p', 'Pending'),
        ('c', 'Closed'),
        ('r', 'Rejected'),
        ('a', 'Approved')
    )

    status = models.CharField(max_length=1, choices=STATUS)

    class Meta:
        managed = False
        db_table = 'test'


