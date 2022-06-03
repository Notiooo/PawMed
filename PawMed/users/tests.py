from django.test import TestCase
from django.urls import reverse

from users.models import CustomUser


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
