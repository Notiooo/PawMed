from django.test import TestCase
from django.urls import reverse
from .models import Visit, Patient, Doctor
# Create your tests here.

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

class DoctorEndVisitViewTest(TestCase):
    # @note: there have to be some entries in the database for the test to pass
    def testEndVisitStatusCode(self):
        response = self.client.get('/doctor/1/end/')
        self.assertEqual(response.status_code, 200)

    def testEndVisitUrlByName(self):
        response = self.client.get(reverse('doctor_endvisit', args=[1]))
        self.assertEqual(response.status_code, 200)

    def testEndVisitCorrectTemplate(self):
        response = self.client.get('/doctor/1/end/')
        self.assertTemplateUsed(response, 'doctor/doctor_endvisit.html')

class DoctorAppointmentViewTest(TestCase):
    def testAppointmentViewStatusCode(self):
        response = self.client.get('/doctor/1/visit/')
        self.assertEqual(response.status_code, 200)

    def testAppointmentViewUrlByName(self):
        response = self.client.get(reverse('doctor_visit', args=[1]))
        self.assertEqual(response.status_code, 200)

    def testAppointmentViewCorrectTemplate(self):
        response = self.client.get('/doctor/1/visit/')
        self.assertTemplateUsed(response, 'doctor/doctor_visit.html')

class DoctorOrderTestViewTest(TestCase):
    def testOrderViewStatusCode(self):
        response = self.client.get('/doctor/2/test/')
        self.assertEqual(response.status_code, 200)

    def testOrderViewUrlByName(self):
        response = self.client.get(reverse('doctor_order_test', args=[1]))
        self.assertEqual(response.status_code, 200)

    def testOrderViewCorrectTemplate(self):
        response = self.client.get(reverse('doctor_order_test', args=[1]))
        self.assertTemplateUsed(response, 'doctor/doctor_order_test.html')

