from django.test import TestCase
from .models import User

# Create your tests here.
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

class ExampleTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='hussein',
            password='11qq22ww'
        )
        self.token = Token.objects.create(user=self.user)

    def test_example_view(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 200)
