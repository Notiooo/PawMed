from django.test import TestCase
from django.urls import reverse
from django.utils.datetime_safe import datetime
from .models import Visit, Patient
from doctor.models import Doctor, Specialization

from users.models import CustomUser


class RegistrarTest(TestCase):
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
        self.assertEqual(response.status_code, 403)


class AddAppointmenViewLoggedOutTest(TestCase):
    def testAppointmentViewStatusCode(self):
        response = self.client.get('/registrar/appointment/1/')
        self.assertEqual(response.status_code, 302)

    def testAppointmentViewUrlByName(self):
        response = self.client.get(reverse('registrar_add_appointment', kwargs={'patient_pk': 1}))
        self.assertEqual(response.status_code, 302)


class AddAppointmentViewLoggedInTest(RegistrarTest):
    def setUp(self):
        super(AddAppointmentViewLoggedInTest, self).setUp()
        user = CustomUser.objects.create_user(username='username', password='password', role='REGISTRAR')
        self.client.login(username='username', password='password')

    def testAppointmentViewStatusCode(self):
        response = self.client.get('/registrar/appointment/1/')
        self.assertEqual(response.status_code, 200)

    def testAppointmentViewUrlByName(self):
        response = self.client.get(reverse('registrar_add_appointment', kwargs={'patient_pk': 1}))
        self.assertEqual(response.status_code, 200)


class AppointmentDoctorFreeVisitsLoggedOutTest(TestCase):
    def testAppointmentViewStatusCode(self):
        response = self.client.get('/registrar/appointment/doctor_list/')
        self.assertEqual(response.status_code, 302)

    def testAppointmentViewUrlByName(self):
        response = self.client.get(reverse('registrar_appointment_doctor_list'))
        self.assertEqual(response.status_code, 302)


class AppointmentDoctorFreeVisitsLoggedInTest(RegistrarTest):
    def setUp(self):
        super(AppointmentDoctorFreeVisitsLoggedInTest, self).setUp()
        user = CustomUser.objects.create_user(username='username', password='password', role='REGISTRAR')
        self.client.login(username='username', password='password')

    def testAppointmentViewStatusCode(self):
        response = self.client.get('/registrar/appointment/doctor_list/')
        self.assertEqual(response.status_code, 403)

    def testAppointmentViewUrlByName(self):
        response = self.client.get(reverse('registrar_appointment_doctor_list'))
        self.assertEqual(response.status_code, 403)

    def testAppointmentCorrectSession(self):
        Specialization.objects.create(
            id=1,
            name="TestSpec"
        )

        session = self.client.session
        session["specialization_id"] = 1
        session["patient-submitted-id"] = 1
        session["patient_pk"] = 1
        session["earliest_date"] = datetime(year=2022, month=1, day=1).strftime('%Y-%m-%d')
        session["latest_date"] = datetime(year=2022, month=1, day=28).strftime('%Y-%m-%d')
        session.save()

        response = self.client.get(reverse('registrar_appointment_doctor_list'))
        self.assertEqual(response.status_code, 200)


class AddPatientCreateViewLoggedIn(TestCase):
    def setUp(self):
        super(AddPatientCreateViewLoggedIn, self).setUp()
        user = CustomUser.objects.create_user(username='username', password='password', role='REGISTRAR')
        self.client.login(username='username', password='password')

    def testAddPatientViewStatusCode(self):
        response = self.client.get('/registrar/add_patient/')
        self.assertEqual(response.status_code, 200)

    def testAddPatientViewUrlByName(self):
        response = self.client.get(reverse('registrar_patient_board'))
        self.assertEqual(response.status_code, 200)


class AddPatientCreateViewNotLoggedIn(TestCase):
    def setUp(self):
        super(AddPatientCreateViewNotLoggedIn, self).setUp()

    def testAddPatientViewStatusCode(self):
        response = self.client.get('/registrar/add_patient/')
        self.assertEqual(response.status_code, 302)

    def testAddPatientViewUrlByName(self):
        response = self.client.get(reverse('registrar_patient_board'))
        self.assertEqual(response.status_code, 302)


class EditPatientUpdateViewLoggedInWithoutSession(RegistrarTest):
    def setUp(self):
        super(EditPatientUpdateViewLoggedInWithoutSession, self).setUp()
        user = CustomUser.objects.create_user(username='username', password='password', role='REGISTRAR')
        self.client.login(username='username', password='password')

    def testAddPatientViewStatusCode(self):
        response = self.client.get('/registrar/edit_patient/1/')
        self.assertEqual(response.status_code, 403)

    def testAddPatientViewUrlByName(self):
        response = self.client.get(reverse('registrar_patient', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)


class EditPatientUpdateViewLoggedInWithSession(RegistrarTest):
    def setUp(self):
        super(EditPatientUpdateViewLoggedInWithSession, self).setUp()
        user = CustomUser.objects.create_user(username='username', password='password', role='REGISTRAR')
        self.client.login(username='username', password='password')

    def testEditPatientViewStatusCode(self):
        session = self.client.session
        session['patient-submitted-id'] = 1
        session["patient_pk"] = 1
        session.save()

        response = self.client.get('/registrar/edit_patient/1/')
        self.assertEqual(response.status_code, 200)

    def testEditPatientViewUrlByName(self):
        session = self.client.session
        session['patient-submitted-id'] = 1
        session["patient_pk"] = 1
        session.save()

        response = self.client.get(reverse('registrar_patient', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)


class CreateVisitTestLoggedIn(RegistrarTest):
    def setUp(self):
        super(CreateVisitTestLoggedIn, self).setUp()
        user = CustomUser.objects.create_user(username='username', password='password', role='REGISTRAR')
        self.client.login(username='username', password='password')

        Specialization.objects.create(
            id=1,
            name="TestSpec"
        )
        session = self.client.session
        session["specialization_id"] = 1
        session["patient-submitted-id"] = 1
        session["patient_pk"] = 1
        session["earliest_date"] = datetime(year=2022, month=1, day=1).strftime('%Y-%m-%d')
        session["latest_date"] = datetime(year=2022, month=1, day=28).strftime('%Y-%m-%d')
        session.save()

    def testCreateVisitUrlByName(self):
        response = self.client.get(reverse(
            'ajax_create_visit',
            kwargs={'doctor_id': 1, 'patient_id': 1,
                    'start_date': datetime(year=2022, month=1, day=1).strftime('%Y-%m-%d'),
                    'doctor_room': '59'}))
        self.assertEqual(response.status_code, 200)