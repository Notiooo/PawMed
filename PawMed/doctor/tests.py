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

