from django.test import TestCase
from django.urls import reverse
from django.utils.datetime_safe import datetime
from doctor.models import Doctor, DoctorSpecialization, Specialization
from registrar.models import Visit, Patient
from users.models import CustomUser

from .models import Test, Technician, Laboratory

# Create your tests here.

class TechnicianTest(TestCase):
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

        technician = Technician.objects.create(
            id=1,
            name="Name",
            surname="Surname"
        )

        laboratory = Laboratory.objects.create(
            id=1,
            room='123a',
            type='Lab Type'
        )

        visit1 = Visit.objects.create(
            id=1,
            doctor=doctor,
            patient=patient,
            date=datetime.now(),
            room="123a",
            took_place=False
        )

        visit2 = Visit.objects.create(
            id=2,
            doctor=doctor,
            patient=patient,
            date=datetime.now(),
            room="123a",
            took_place=False
        )

        Test.objects.create(
            id=1,
            type="Test type",
            execution_date=datetime.now(),
            executive=technician,
            remarks="Remarks",
            laboratory_room=laboratory,
            visit= visit1,
            status='p'   
        )

        Test.objects.create(
            id=2,
            type="Test type",
            execution_date=datetime.now(),
            executive=technician,
            remarks="Remarks",
            laboratory_room=laboratory,
            visit= visit2,
            status='c'   
        )

        user = CustomUser.objects.create_user(username='username1', password='password1', email='user1@user.com', role='LAB_TECHNICIAN')
        CustomUser.objects.create_user(username='username2', password='password2', email='user2@user.com', role='LAB_MANAGER')
        self.client.login(username='username1', password='password')


class TechnicianHomepageViewTest(TechnicianTest):
    def testHomepageViewStatusCode(self):
        response = self.client.get('/technician/home/')
        self.assertEqual(response.status_code, 200)

    def testHomepageViewUrlByName(self):
        response = self.client.get(reverse('technician_home'))
        self.assertEqual(response.status_code, 200)

    def testHomepageViewTemplateUsed(self):
        response = self.client.get(reverse('technician_home'))
        self.assertTemplateUsed(response, 'technician/technician_homepage.html')

class TechnicianSubmitResultViewTest(TechnicianTest):
    def testSubmitResultViewStatusCode(self):
        response = self.client.get('/technician/1/submit')
        self.assertEqual(response.status_code, 301)

    def testSubmitResultViewUrlByName(self):
        response = self.client.get(reverse("technician_submit_result", args=[1]))
        self.assertEqual(response.status_code, 200)

    def testSubmitViewTemplateUsed(self):
        response = self.client.get(reverse("technician_submit_result", args=[1]))
        self.assertTemplateUsed(response, 'technician/submit_results.html')

class HeadHomepageViewTest(TechnicianTest):
    def testHomepageViewStatusCode(self):
        self.client.login(username='username2', password='password')
        response = self.client.get('/technician/head/')
        self.assertAlmostEqual(response.status_code, 200)

    def testHomepageViewUrlByName(self):
        response = self.client.get(reverse('head_home'))
        self.assertEqual(response.status_code, 200)

    def testHomepageViewTemplateUsed(self):
        response = self.client.get('/technician/head/')
        self.assertTemplateUsed(response, 'technician/technician_head_homepage.html')

class HeadApprovalViewTest(TechnicianTest):
    def testApprovalViewStatusCode(self):
        response = self.client.get('/technician/1/approval')
        self.assertEqual(response.status_code, 301)

    def testApprovalViewUrlByName(self):
        response = self.client.get(reverse("head_technician_approval_view", args=[1]))
        self.assertEqual(response.status_code, 200)

    def testApprovalViewTemplateUsed(self):
        response = self.client.get(reverse("head_technician_approval_view", args=[1]))
        self.assertTemplateUsed(response, 'technician/approval_view.html')