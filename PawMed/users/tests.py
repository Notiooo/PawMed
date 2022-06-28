from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser
from doctor.models import Doctor, Specialization, DoctorSpecialization


class AssignRolesListViewLoggedSuperUserTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username='username', password='password', is_superuser='True')
        user.save()
        self.client.login(username='username', password='password')

    def testStatusCode(self):
        response = self.client.get('/users/admin/')
        self.assertEqual(response.status_code, 200)

    def testUrlByName(self):
        response = self.client.get(reverse('admin_roles'))
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplate(self):
        response = self.client.get(reverse('admin_roles'))
        self.assertTemplateUsed(response, 'users/admin.html')


class AssignRolesListViewLoggedInTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username='username', password='password')
        user.save()
        self.client.login(username='username', password='password')

    def testStatusCode(self):
        response = self.client.get('/users/admin/')
        self.assertEqual(response.status_code, 403)

    def testUrlByName(self):
        response = self.client.get(reverse('admin_roles'))
        self.assertEqual(response.status_code, 403)


class AssignRolesListViewLoggedOutTest(TestCase):
    def testStatusCode(self):
        response = self.client.get('/users/admin/')
        self.assertEqual(response.status_code, 302)

    def testViewUrlByName(self):
        response = self.client.get(reverse('admin_roles'))
        self.assertEqual(response.status_code, 302)


class AssignRolesUpdateViewLoggedSuperUserTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(id=1, username='username', password='password', is_superuser='True')
        user.save()
        self.client.login(username='username', password='password')

    def testStatusCode(self):
        response = self.client.get('/users/admin/1/')
        self.assertEqual(response.status_code, 200)

    def testUrlByName(self):
        response = self.client.get(reverse('admin_roles_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplate(self):
        response = self.client.get(reverse('admin_roles_update', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'users/admin_update_role.html')


class AssignRolesUpdateViewLoggedInTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username='username', password='password')
        user.save()
        self.client.login(username='username', password='password')

    def testStatusCode(self):
        response = self.client.get('/users/admin/1/')
        self.assertEqual(response.status_code, 403)

    def testUrlByName(self):
        response = self.client.get(reverse('admin_roles_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)


class AssignRolesUpdateViewLoggedOutTest(TestCase):
    def testStatusCode(self):
        response = self.client.get('/users/admin/1/')
        self.assertEqual(response.status_code, 302)

    def testViewUrlByName(self):
        response = self.client.get(reverse('admin_roles_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)


class AdminDoctorListViewLoggedSuperUserTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(id=1, username='username', password='password', is_superuser='True')
        user.save()
        self.client.login(username='username', password='password')

    def testStatusCode(self):
        response = self.client.get('/users/admin-doctor/')
        self.assertEqual(response.status_code, 200)

    def testUrlByName(self):
        response = self.client.get(reverse('admin_doctors'))
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplate(self):
        response = self.client.get(reverse('admin_doctors'))
        self.assertTemplateUsed(response, 'users/admin-doctor.html')


class AdminDoctorListViewLoggedInTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username='username', password='password')
        user.save()
        self.client.login(username='username', password='password')

    def testStatusCode(self):
        response = self.client.get('/users/admin-doctor/')
        self.assertEqual(response.status_code, 403)

    def testUrlByName(self):
        response = self.client.get(reverse('admin_doctors'))
        self.assertEqual(response.status_code, 403)


class AdminDoctorListViewLoggedOutTest(TestCase):
    def testStatusCode(self):
        response = self.client.get('/users/admin-doctor/')
        self.assertEqual(response.status_code, 302)

    def testViewUrlByName(self):
        response = self.client.get(reverse('admin_doctors'))
        self.assertEqual(response.status_code, 302)


class AdminDoctorUpdateViewLoggedSuperUserTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(id=1, username='username', password='password', is_superuser='True')
        user.save()
        doctor = Doctor.objects.create(
            id=1,
            name="Name",
            surname="Surname",
            room="123a",
            phone_number="511722711"
        )
        self.client.login(username='username', password='password')

    def testStatusCode(self):
        response = self.client.get('/users/admin-doctor-update/1/')
        self.assertEqual(response.status_code, 200)

    def testUrlByName(self):
        response = self.client.get(reverse('admin_doctor_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplate(self):
        response = self.client.get(reverse('admin_doctor_update', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'users/admin-doctor-update.html')


class AdminDoctorUpdateViewLoggedInTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username='username', password='password')
        user.save()
        self.client.login(username='username', password='password')

    def testStatusCode(self):
        response = self.client.get('/users/admin-doctor-update/1/')
        self.assertEqual(response.status_code, 403)

    def testUrlByName(self):
        response = self.client.get(reverse('admin_doctor_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)


class AdminDoctorUpdateViewLoggedOutTest(TestCase):
    def testStatusCode(self):
        response = self.client.get('/users/admin-doctor-update/1/')
        self.assertEqual(response.status_code, 302)

    def testViewUrlByName(self):
        response = self.client.get(reverse('admin_doctor_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)


class AdminDoctorSpecializationUpdateSuperUserTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(id=1, username='username', password='password', is_superuser='True')
        user.save()
        self.client.login(username='username', password='password')
        doctor = Doctor.objects.create(
            id=1,
            name="Name",
            surname="Surname",
            room="123a",
            phone_number="511722711"
        )

    def testStatusCode(self):
        response = self.client.get('/users/admin-doctor-specialization-update/1/')
        self.assertEqual(response.status_code, 200)

    def testUrlByName(self):
        response = self.client.get(reverse('admin_doctor_specialization_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def testCorrectTemplate(self):
        response = self.client.get(reverse('admin_doctor_specialization_update', kwargs={'pk': 1}))
        self.assertTemplateUsed(response, 'users/admin-doctor-specialization-update.html')


class AdminDoctorSpecializationUpdateLoggedInTest(TestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username='username', password='password')
        user.save()
        self.client.login(username='username', password='password')

    def testStatusCode(self):
        response = self.client.get('/users/admin-doctor-specialization-update/1/')
        self.assertEqual(response.status_code, 403)

    def testUrlByName(self):
        response = self.client.get(reverse('admin_doctor_specialization_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)


class AdminDoctorSpecializationUpdateLoggedOutTest(TestCase):
    def testStatusCode(self):
        response = self.client.get('/users/admin-doctor-specialization-update/1/')
        self.assertEqual(response.status_code, 302)

    def testViewUrlByName(self):
        response = self.client.get(reverse('admin_doctor_specialization_update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)


class DoctorSpecializationSetup(TestCase):
    def setUp(self):
        doctor = Doctor.objects.create(
            id=1,
            name="Name",
            surname="Surname",
            room="123a",
            phone_number="511722711"
        )
        spec = Specialization.objects.create(
            id=1,
            name="TestSpec"
        )
        DoctorSpecialization.objects.create(
            doctorid=doctor,
            specialization=spec,
            id=1
        )


class AdminDeleteDoctorSpecializationSuperUserTest(DoctorSpecializationSetup):
    def setUp(self):
        super(AdminDeleteDoctorSpecializationSuperUserTest, self).setUp()
        user = CustomUser.objects.create_user(id=1, username='username', password='password', is_superuser='True')
        user.save()
        self.client.login(username='username', password='password')

    def testStatusCode(self):
        response = self.client.get('/users/ajax/delete-doctor-specialization/1/')
        self.assertEqual(response.status_code, 200)

    def testUrlByName(self):
        response = self.client.get(reverse('ajax_doctor_specialization_delete', kwargs={'doctor_specialization_id': 1}))
        self.assertEqual(response.status_code, 200)


class AdminDeleteDoctorSpecializationLoggedInTest(DoctorSpecializationSetup):
    def setUp(self):
        super(AdminDeleteDoctorSpecializationLoggedInTest, self).setUp()
        user = CustomUser.objects.create_user(username='username', password='password')
        user.save()
        self.client.login(username='username', password='password')

    def testStatusCode(self):
        response = self.client.get('/users/ajax/delete-doctor-specialization/1/')
        self.assertEqual(response.status_code, 403)

    def testUrlByName(self):
        response = self.client.get(reverse('ajax_doctor_specialization_delete', kwargs={'doctor_specialization_id': 1}))
        self.assertEqual(response.status_code, 403)


class AdminDeleteDoctorSpecializationLoggedOutTest(DoctorSpecializationSetup):
    def setUp(self):
        super(AdminDeleteDoctorSpecializationLoggedOutTest, self).setUp()

    def testStatusCode(self):
        response = self.client.get('/users/ajax/delete-doctor-specialization/1/')
        self.assertEqual(response.status_code, 302)

    def testViewUrlByName(self):
        response = self.client.get(reverse('ajax_doctor_specialization_delete', kwargs={'doctor_specialization_id': 1}))
        self.assertEqual(response.status_code, 302)


class AdminAddDoctorSpecializationSuperUserTest(DoctorSpecializationSetup):
    def setUp(self):
        super(AdminAddDoctorSpecializationSuperUserTest, self).setUp()
        user = CustomUser.objects.create_user(id=1, username='username', password='password', is_superuser='True')
        user.save()
        self.client.login(username='username', password='password')

    def testStatusCode(self):
        response = self.client.get('/users/ajax/add-doctor-specialization/1/1/')
        self.assertEqual(response.status_code, 200)

    def testUrlByName(self):
        response = self.client.get(reverse('ajax_doctor_specialization_add',
                                           kwargs={'doctor_id': 1, 'specialization_id': 1}))
        self.assertEqual(response.status_code, 200)


class AdminAddDoctorSpecializationLoggedInTest(DoctorSpecializationSetup):
    def setUp(self):
        super(AdminAddDoctorSpecializationLoggedInTest, self).setUp()
        user = CustomUser.objects.create_user(username='username', password='password')
        user.save()
        self.client.login(username='username', password='password')

    def testStatusCode(self):
        response = self.client.get('/users/ajax/add-doctor-specialization/1/1/')
        self.assertEqual(response.status_code, 403)

    def testUrlByName(self):
        response = self.client.get(reverse('ajax_doctor_specialization_add',
                                           kwargs={'doctor_id': 1, 'specialization_id': 1}))
        self.assertEqual(response.status_code, 403)


class AdminAddDoctorSpecializationLoggedOutTest(DoctorSpecializationSetup):
    def setUp(self):
        super(AdminAddDoctorSpecializationLoggedOutTest, self).setUp()

    def testStatusCode(self):
        response = self.client.get('/users/ajax/add-doctor-specialization/1/1/')
        self.assertEqual(response.status_code, 302)

    def testViewUrlByName(self):
        response = self.client.get(reverse('ajax_doctor_specialization_add',
                                           kwargs={'doctor_id': 1, 'specialization_id': 1}))
        self.assertEqual(response.status_code, 302)
