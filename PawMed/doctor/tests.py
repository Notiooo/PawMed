from django.test import TestCase
from django.urls import reverse
from django.utils.datetime_safe import datetime
from registrar.models import Visit, Patient
from .models import Doctor


class DoctorTest(TestCase):
    def setUp(self):
        patient = Patient.objects.create(
            id=1,
            name="Name",
            surname="Surname",
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

class DoctorHomepageViewTest(TestCase):
    def testHomepageStatusCode(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def testHomepageUrlByName(self):
        response = self.client.get(reverse('doctor_homepage'))
        self.assertEqual(response.status_code, 200)

    def testHomepageCorrectTemplate(self):
        response = self.client.get(reverse('doctor_homepage'))
        self.assertTemplateUsed(response, 'doctor/doctor_homepage.html')


class DoctorEndVisitViewTest(DoctorTest):
    def testEndVisitStatusCode(self):
        response = self.client.get('/doctor/1/end/')
        self.assertEqual(response.status_code, 200)

    def testEndVisitUrlByName(self):
        response = self.client.get(reverse('doctor_endvisit', args=[1]))
        self.assertEqual(response.status_code, 200)

    def testEndVisitCorrectTemplate(self):
        response = self.client.get('/doctor/1/end/')
        self.assertTemplateUsed(response, 'doctor/doctor_endvisit.html')


class DoctorAppointmentViewTest(DoctorTest):
    def testAppointmentViewStatusCode(self):
        response = self.client.get('/doctor/1/visit/')
        self.assertEqual(response.status_code, 200)

    def testAppointmentViewUrlByName(self):
        response = self.client.get(reverse('doctor_visit', args=[1]))
        self.assertEqual(response.status_code, 200)

    def testAppointmentViewCorrectTemplate(self):
        response = self.client.get('/doctor/1/visit/')
        self.assertTemplateUsed(response, 'doctor/doctor_visit.html')
