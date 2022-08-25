from django.test import TestCase
from api.models import Vessel, User
from django.utils.crypto import get_random_string


class VesselTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.name = get_random_string(length=10)
        self.naccs_code = get_random_string(length=5)

    def tearDown(self):
        self.user.delete()

    def test_vessel_name(self):
        vessel = self.createVessel()
        self.assertEqual(vessel.name, self.name.upper())

    def test_vessel_naccs_code(self):
        vessel = self.createVessel()
        self.assertEqual(vessel.naccs_code, self.naccs_code.upper())

    def test_vessel_user(self):
        vessel = self.createVessel()
        self.assertEqual(vessel.owner, self.user)

    def createVessel(self):
        return Vessel.objects.create(
            name=self.name,
            naccs_code=self.naccs_code,
            owner=self.user
        )
