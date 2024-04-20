from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .models import ServiceCategory, Service, Ticket, TicketPicture
from Users.models import User,Staff

with open('tests/test_image.jpg', 'rb') as file:
    data = file.read()

# a SimpleUploadedFile instance
uploaded_file = SimpleUploadedFile('test_image.jpg', data)

class TestServiceCategory(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(title='Test Category', icon=uploaded_file)

    def test_str(self):
        self.assertEqual(str(self.category), 'Test Category')

    # def test_icon_upload(self):
    #     self.assertEqual(self.category.icon.name, 'service_categories/test_image.jpg')

class TestService(TestCase):
    def setUp(self):
        self.category = ServiceCategory.objects.create(title='Test Category', icon=uploaded_file)
        self.service = Service.objects.create(title='Test Service',initial_price=3900, service_category=self.category, picture=uploaded_file)

    def test_str(self):
        self.assertEqual(str(self.service), 'Test Service')

    # def test_picture_upload(self):
    #     self.assertEqual(self.service.picture.name, 'serv_pictures/test_image.jpg')

class TestTicket(TestCase):
    def setUp(self):
        self.client = User.objects.create_user(email='hhd@dhd.vb', password='test_password')
        self.client2 = User.objects.create_user(email='eeeed@dhd.vb', password='test_password', is_staff=True)
        self.staff = Staff.objects.create(user=self.client2,department='tech')

        self.service = Service.objects.create(title='Test Service',initial_price=3900, service_category=ServiceCategory.objects.create(title='Test Category', icon=uploaded_file), picture=uploaded_file)
        self.ticket = Ticket.objects.create(client=self.client, service=self.service, assigned_to=self.staff,location={"2":"6"})

    def test_str(self):
        self.assertEqual(str(self.ticket), f'{self.ticket.pk} -- Open')

    def test_client_assignment(self):
        self.assertEqual(self.ticket.client, self.client)

    def test_service_assignment(self):
        self.assertEqual(self.ticket.service, self.service)

    def test_staff_assignment(self):
        self.assertEqual(self.ticket.assigned_to, self.staff)

    def test_status_default(self):
        self.assertEqual(self.ticket.status, 'Open')

# class TestTicketPicture(TestCase):
#     def setUp(self):
#         self.ticket = Ticket.objects.create(client=User.objects.create_user(username='test_client', password='test_password'), service=Service.objects.create(title='Test Service', service_category=ServiceCategory.objects.create(title='Test Category', icon=SimpleUploadedFile(open('tests/test_image.jpg', 'rb'))), picture=SimpleUploadedFile(open('tests/test_image.jpg', 'rb'))), assigned_to=User.objects.create_user(username='test_staff', password='test_password', is_staff=True))
#         self.picture = SimpleUploadedFile(open('tests/test_image.jpg', 'rb'))
#         self.ticket_picture = TicketPicture.objects.create(ticket=self.ticket, picture=self.picture)

#     def test_ticket_assignment(self):
#         self.assertEqual(self.ticket_picture.ticket, self.ticket)

#     def test_picture_upload(self):
#         self.assertEqual(self.ticket_picture.picture.name, 'attachments/test_image.jpg')

# class TestDeleteOldImage(TestCase):
#     def setUp(self):
#         self.category = ServiceCategory.objects.create(title='Test Category', icon=SimpleUploadedFile(open('tests/test_image.jpg', 'rb')))
#         self.service = Service.objects.create(title='Test Service', service_category=self.category, picture=SimpleUploadedFile(open('tests/test_image.jpg', 'rb')))
#         self.ticket = Ticket.objects.create(client=User.objects.create_user(username='test_client', password='test_password'), service=self.service, assigned_to=User.objects.create_user(username='test_staff', password='test_password', is_staff=True))
#         self.picture = SimpleUploadedFile(open('tests/test_image.jpg', 'rb'))
#         self.ticket_picture = TicketPicture.objects.create(ticket=self.ticket, picture=self.picture)

#     def test_delete_old_image(self):
#         old_image = self.ticket_picture.picture
#         new_image = SimpleUploadedFile(open('tests/test_image.jpg', 'rb'))
#         self.ticket_picture.picture = new_image
#         self.ticket_picture.save()
#         self.assertFalse(default_storage.exists(old_image.name))

#     def test_upload_new_image(self):
#         new_image = SimpleUploadedFile(open('tests/test_image.jpg', 'rb'))
#         self.ticket_picture.picture = new_image
#         self.ticket_picture.save()
#         self.assertTrue(default_storage.exists(self.ticket_picture.picture.name))

class TestTicketChangeStatus(TestCase):
    def setUp(self):
        self.client = User.objects.create_user(email='hhd@dhd.vb', password='test_password')
        self.client2 = User.objects.create_user(email='eeehhd@dhd.vb', password='test_password', is_staff=True)
        self.staff = Staff.objects.create(user=self.client2,department='tech')
        self.service = Service.objects.create(title='Test Service', initial_price=3900, service_category=ServiceCategory.objects.create(title='Test Category', icon=uploaded_file), picture=uploaded_file)
        self.ticket = Ticket.objects.create(client=self.client, service=self.service, assigned_to=self.staff,location={"2":"6"})

    def test_status_change(self):
        self.assertEqual(self.ticket.status, 'Open')
        self.ticket.status = 'In Progress'
        self.ticket.save()
        self.assertEqual(self.ticket.status, 'In Progress')

# class TestTicketAddNote(TestCase):
#     def setUp(self):
#         self.client = User.objects.create_user(username='test_client', password='test_password')
#         self.staff = User.objects.create_user(username='test_staff', password='test_password', is_staff=True)
#         self.service = Service.objects.create(title='Test Service', service_category=ServiceCategory.objects.create(title='Test Category', icon=SimpleUploadedFile(open('tests/test_image.jpg', 'rb'))), picture=SimpleUploadedFile(open('tests/test_image.jpg', 'rb')))
#         self.ticket = Ticket.objects.create(client=self.client, service=self.service, assigned_to=self.staff)
#         self.note = 'This is a test note.'
#         self.ticket.add_note(self.staff, self.note)

#     def test_note_added(self):
#         self.assertEqual(self.ticket.notes.latest('pk').note, self.note)

#     def test_note_user(self):
#         self.assertEqual(self.ticket.notes.latest('pk').user, self.staff)

#     def test_note_ticket(self):
#         self.assertEqual(self.ticket.notes.latest('pk').ticket, self.ticket)

# class TestTicketClose(TestCase):
#     def setUp(self):
#         self.client = User.objects.create_user(username='test_client', password='test_password')
#         self.staff = User.objects.create_user(username='test_staff', password='test_password', is_staff=True)
#         self.service = Service.objects.create(title='Test Service', service_category=ServiceCategory.objects.create(title='Test Category', icon=SimpleUploadedFile(open('tests/test_image.jpg', 'rb'))), picture=SimpleUploadedFile(open('tests/test_image.jpg', 'rb')))
#         self.ticket = Ticket.objects.create(client=self.client, service=self.service, assigned_to=self.staff)
#         self.note = 'This is a test note.'
#         self.ticket.add_note(self.staff, self.note)

#     def test_close_ticket(self):
#         self.assertEqual(self.ticket.status, 'Open')
#         self.ticket.close()
#         self.assertEqual(self.ticket.status, 'Closed')

#     def test_close_ticket_note(self):
#         self.ticket.close()
#         self.assertEqual(self.ticket.notes.latest('pk').note, 'Ticket closed by {0}.'.format(self.staff.username))

# class TestTicketReopen(TestCase):
#     def setUp(self):
#         self.client = User.objects.create_user(username='test_client', password='test_password')
#         self.staff = User.objects.create_user(username='test_staff', password='test_password', is_staff=True)
#         self.service = Service.objects.create(title='Test Service', service_category=ServiceCategory.objects.create(title='Test Category', icon=SimpleUploadedFile(open('tests/test_image.jpg', 'rb'))), picture=SimpleUploadedFile(open('tests/test_image.jpg', 'rb')))
#         self.ticket = Ticket.objects.create(client=self.client, service=self.service, assigned_to=self.staff)
#         self.note = 'This is a test note.'
#         self.ticket.add_note(self.staff, self.note)
#         self.ticket.close()

#     def test_reopen_ticket(self):
#         self.assertEqual(self.ticket.status, 'Closed')
#         self.ticket.reopen()
#         self.assertEqual(self.ticket.status, 'Open')

#     def test_reopen_ticket_note(self):
#         self.ticket.reopen()
#         self.assertEqual(self.ticket.notes.latest('pk').note, 'Ticket reopened by {0}.'.format(self.staff.username))