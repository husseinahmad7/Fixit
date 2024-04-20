from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from django.contrib.auth.models import User as AuthUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import Group
from .models import User, Staff
from Ticket.models import Service, ServiceCategory


with open('tests/test_image.jpg', 'rb') as file:
    data = file.read()

# a SimpleUploadedFile instance
uploaded_file = SimpleUploadedFile('test_image.jpg', data)

class UserModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            full_name='Test User',
            mobile='1234567890',
        )

    def test_user_str(self):
        self.assertEqual(str(self.user), 'Test User')

    def test_user_email(self):
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_user_full_name(self):
        self.assertEqual(self.user.full_name, 'Test User')

    def test_user_mobile(self):
        self.assertEqual(self.user.mobile, '1234567890')

    def test_user_is_staff(self):
        self.assertEqual(self.user.is_staff, False)

    def test_user_is_superuser(self):
        self.assertEqual(self.user.is_superuser, False)

    def test_user_groups(self):
        self.assertEqual(len(self.user.groups.all()), 0)

    def test_user_permissions(self):
        self.assertEqual(len(self.user.user_permissions.all()), 0)

    def test_user_is_active(self):
        self.assertEqual(self.user.is_active, True)

    # def test_user_username(self):
    #     self.assertEqual(self.user.username, 'testuser@example.com')

    def test_user_full_name(self):
        self.assertEqual(self.user.full_name, 'Test User')

    def test_user_mobile(self):
        self.assertEqual(self.user.mobile, '1234567890')

    def test_user_device_reg_id(self):
        self.assertEqual(self.user.device_reg_id, None)

class StaffModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            full_name='Test User',
            mobile='1234567890',
        )
        self.staff = Staff.objects.create(
            user=self.user,
            department='IT',
            salary=1000,
            availability=True,
            is_supervisor=False,
        )

    def test_staff_str(self):
        self.assertEqual(str(self.staff), 'Test User')

    def test_staff_user(self):
        self.assertEqual(self.staff.user, self.user)

    def test_staff_department(self):
        self.assertEqual(self.staff.department, 'IT')

    def test_staff_salary(self):
        self.assertEqual(self.staff.salary, 1000)

    def test_staff_availability(self):
        self.assertEqual(self.staff.availability, True)

    def test_staff_services(self):
        self.assertEqual(len(self.staff.services.all()), 0)

    def test_staff_is_supervisor(self):
        self.assertEqual(self.staff.is_supervisor, False)

    def test_staff_get_absolute_url(self):
        self.assertEqual(self.staff.get_absolute_url(), f'/st/staff/{self.staff.pk}/')



# class TestViews(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(
#             email='test@example.com',
#             password='testpassword',
#             full_name='Test User',
#             mobile='1234567890',
#         )
#         self.staff = Staff.objects.create(
#             user=self.user,
#             department='IT',
#             salary=1000,
#             availability=True,
#             is_supervisor=False,
#         )
#         # self.cat =ServiceCategory.objects.create(title='Category 1')
#         self.service = Service.objects.create(title='Test Service',initial_price=3000, service_category=ServiceCategory.objects.create(title='Test Category', icon=uploaded_file), picture=uploaded_file)

#         # self.service = Service.objects.create(title='Service 1',)
#         self.api_client = APIRequestFactory()

#     def test_users_list_create_view(self):
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('users:list'))
#         self.assertEqual(response.status_code, 200)

#         response = self.client.post(reverse('users:list'), {
#             'email': 'newuser@example.com',
#             'password': 'newpassword',
#             'full_name': 'New User',
#             'mobile': '0987654321',
#         })
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(User.objects.count(), 2)

#     def test_users_retrieve_delete_update_view(self):
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('users:retrieve-update-delete', args=[self.user.pk]))
#         self.assertEqual(response.status_code, 200)

#         response = self.client.put(reverse('users:retrieve-update-delete', args=[self.user.pk]), {
#             'email': 'updateduser@example.com',
#             'password': 'updatedpassword',
#             'full_name': 'Updated User',
#             'mobile': '1111111111',
#         })
#         self.assertEqual(response.status_code, 200)
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.email, 'updateduser@example.com')

#         response = self.client.delete(reverse('users:retrieve-update-delete', args=[self.user.pk]))
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(User.objects.count(), 1)

#     def test_user_retrieve_update_api_view(self):
#         self.client.force_login(self.user)
#         request = self.api_client.get(reverse('users:retrieve-update', args=[self.user.pk]))
#         self.assertEqual(request.status_code, 200)

#         request = self.api_client.put(reverse('users:retrieve-update', args=[self.user.pk]), {
#             'email': 'updateduser@example.com',
#             'password': 'updatedpassword',
#             'full_name': 'Updated User',
#             'mobile': '1111111111',
#         })
#         self.assertEqual(request.status_code, 200)
#         self.user.refresh_from_db()
#         self.assertEqual(self.user.email, 'updateduser@example.com')

#     def test_staff_list_api_view(self):
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('users:staff-list'))
#         self.assertEqual(response.status_code, 200)

#     def test_staffs_retrieve_delete_update_view(self):
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('users:staff-retrieve-update-delete', args=[self.staff.pk]))
#         self.assertEqual(response.status_code, 200)

#         response = self.client.put(reverse('users:staff-retrieve-update-delete', args=[self.staff.pk]), {
#             'department': 'Updated Department',
#             'salary': 1001,
#             'availability': False,
#             'is_supervisor': True,
#         })
#         self.assertEqual(response.status_code, 200)
#         self.staff.refresh_from_db()
#         self.assertEqual(self.staff.department, 'Updated Department')

#         response = self.client.delete(reverse('users:staff-retrieve-update-delete', args=[self.staff.pk]))
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(Staff.objects.count(), 0)

#     def test_add_service_for_staff_view(self):
#         self.client.force_login(self.user)
#         response = self.client.post(reverse('users:add-service', args=[self.staff.pk]), {
#             'service': self.service.pk,
#         })
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(self.staff.services.count(), 1)

#     def test_delete_service_for_staff_view(self):
#         self.client.force_login(self.user)
#         self.staff.services.add(self.service)
#         response = self.client.delete(reverse('users:delete-service', args=[self.staff.pk, self.service.pk]))
#         self.assertEqual(response.status_code, 204)
#         self.assertEqual(self.staff.services.count(), 0)

#     def test_user_registration_api_view(self):
#         request = self.api_client.post(reverse('register'), {
#             'email': 'newuser@example.com',
#             'password': 'newpassword',
#             'full_name': 'New User',
#             'mobile': '0987654321',
#         })
#         self.assertEqual(request.status_code, 201)
#         self.assertEqual(User.objects.count(), 2)

#     def test_activate_user_api_view(self):
#         request = self.api_client.post(reverse('register-activate'), {
#             'activation_code': 'activationcode',
#         })
#         self.assertEqual(request.status_code, 200)

#     def test_staff_registration_view(self):
#         self.client.force_login(self.user)
#         response = self.client.post(reverse('staff-registration'), {
#             'department': 'IT',
#             'salary': 1000,
#             'availability': True,
#             'is_supervisor': False,
#         })
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Staff.objects.count(), 2)

#     def test_login_view(self):
#         response = self.client.post(reverse('users:login'), {
#             'email': 'test@example.com',
#             'password': 'testpassword',
#         })
#         self.assertEqual(response.status_code, 200)

#     def test_logout_view(self):
#         self.client.force_login(self.user)
#         response = self.client.post(reverse('users:logout'))
#         self.assertEqual(response.status_code, 204)