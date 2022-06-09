from django.test import TestCase
from django.urls import reverse
from django.utils.datetime_safe import datetime
from registrar.models import Visit, Patient
from .models import Doctor, DoctorSpecialization, Specialization

from users.models import CustomUser


class DoctorTest(TestCase):
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
        user = CustomUser.objects.create_user(username='username', password='password', role='DOCTOR')
        self.client.login(username='username', password='password')

class DoctorHomepageViewTest(DoctorTest):
    def testHomepageStatusCode(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def testHomepageUrlByName(self):
        response = self.client.get(reverse('doctor_homepage'))
        self.assertEqual(response.status_code, 200)

    def testHomepageCorrectTemplate(self):
        response = self.client.get(reverse('doctor_homepage'))
        self.assertTemplateUsed(response, 'doctor/doctor_homepage.html')

class DoctorAppointmentViewTest(DoctorTest):
    def testAppointmentViewStatusCode(self):
        response = self.client.get('/doctor/1/visit/')
        self.assertEqual(response.status_code, 200)

    def testAppointmentViewUrlByName(self):
        response = self.client.get(reverse('doctor_visit', args=[1]))
        self.assertEqual(response.status_code, 200)

    def testAppointmentViewCorrectTemplate(self):
        response = self.client.get('/doctor/2/visit/')
        self.assertTemplateUsed(response, 'doctor/doctor_visit_exam.html')

class DoctorOrderTestViewTest(DoctorTest):
    def testOrderViewStatusCode(self):
        response = self.client.get('/doctor/2/test/')
        self.assertEqual(response.status_code, 200)

    def testOrderViewUrlByName(self):
        response = self.client.get(reverse('doctor_order_test', args=[2]))
        self.assertEqual(response.status_code, 200)

    def testOrderViewCorrectTemplate(self):
        response = self.client.get(reverse('doctor_order_test', args=[2]))
        self.assertTemplateUsed(response, 'doctor/doctor_visit_test.html')

class DoctorPatientHistoryViewTest(DoctorTest):
    def testHistoryViewStatusCode(self):
        response = self.client.get('/doctor/2/history/')
        self.assertEqual(response.status_code, 200)

    def testHistoryViewUrlByName(self):
        response = self.client.get(reverse('doctor_patient_history', args=[2]))
        self.assertAlmostEqual(response.status_code, 200)

    def testHistoryViewCorrectTemplate(self):
        response = self.client.get('/doctor/2/history/')
        self.assertTemplateUsed(response, 'doctor/doctor_visit_history.html')

class DoctorCreatePrescriptionViewTest(DoctorTest):
    def testCreatePresciptionViewStatusCode(self):
        response = self.client.get('/doctor/2/prescription/')
        self.assertEqual(response.status_code, 200)

    def testCreatePrescriptionViewUrlByName(self):
        response = self.client.get(reverse('doctor_prescription', args=[2]))
        self.assertEqual(response.status_code, 200)

    def testCreatePresciptionViewCorrectTemplate(self):
        response = self.client.get('/doctor/2/prescription/')
        self.assertTemplateUsed(response, 'doctor/doctor_visit_prescription.html')