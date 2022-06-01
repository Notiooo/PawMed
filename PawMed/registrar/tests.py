from django.test import TestCase
from django.urls import reverse
from django.utils.datetime_safe import datetime
from .models import Visit, Patient
from doctor.models import Doctor

from users.models import CustomUser


class RegistrarTest(TestCase):
    def setUp(self):
        patient = Patient.objects.create(
            id=1,
            name="Name",
            surname="Surname",
            age=22,
            phone_number="511722711",
            birth_date=datetime.now(),
            city="Chrzanow",
            zip_code="21-100",
            gender="f",
            personid="5111"
        )

        doctor = Doctor.objects.create(
            id=1,
            name="Name",
            surname="Surname",
            room="123a",
            phone_number="511722711"
        )

        Visit.objects.create(
            id=1,
            doctor=doctor,
            patient=patient,
            date=datetime.now(),
            room="123a",
            took_place=False
        )

        Visit.objects.create(
            id=2,
            doctor=doctor,
            patient=patient,
            date=datetime.now(),
            room="123a",
            took_place=False
        )


class RegistrarHomepageViewLoggedInTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username='username', password='password', role='REGISTRAR')
        self.client.login(username='username', password='password')

    def testPatientBoardStatusCode(self):
        response = self.client.get('/registrar/')
        self.assertEqual(response.status_code, 200)

    def testPatientBoardUrlByName(self):
        response = self.client.get(reverse('registrar_patient_board'))
        self.assertEqual(response.status_code, 200)

    def testHomepageCorrectTemplate(self):
        response = self.client.get(reverse('registrar_patient_board'))
        self.assertTemplateUsed(response, 'registrar/patient_board.html')


class RegistrarHomepageViewLoggedOutTest(TestCase):
    def testPatientBoardStatusCode(self):
        response = self.client.get('/registrar/')
        self.assertEqual(response.status_code, 302)

    def testPatientBoardUrlByName(self):
        response = self.client.get(reverse('registrar_patient_board'))
        self.assertEqual(response.status_code, 302)


class RegistrarPatientViewLoggedInTest(RegistrarTest):
    def setUp(self):
        super(RegistrarPatientViewLoggedInTest, self).setUp()
        user = CustomUser.objects.create_user(username='username', password='password', role='REGISTRAR')
        self.client.login(username='username', password='password')

    def testCorrectPatientDisplayStatusCode(self):
        session = self.client.session
        session['patient-submitted-id'] = 1
        session.save()
        response = self.client.get('/registrar/patient/1/')
        self.assertEqual(response.status_code, 200)

    def testIncorrectPatientDisplayStatusCode(self):
        response = self.client.get('/registrar/patient/1/')
        self.assertEqual(response.status_code, 404)