from django.test import TestCase
from api.models import User
import uuid


class ModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')

    def tearDown(self):
        self.user.delete()

    def test_user_uuid(self):
        self.assertEqual(
            uuid.UUID(str(self.user.id), version=4), self.user.id)
