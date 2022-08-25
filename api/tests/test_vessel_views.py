from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from api.models import Vessel, User
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from django.forms.models import model_to_dict


class VesselViewsTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # Setup urls
        self.retrieveVessels = reverse('retrieve-all-vessels')
        self.retrieveUserVessels = reverse('retrieve-user-vessels')
        self.retriveUserVessel = ''
        self.addVessel = reverse('add-vessel')
        self.updateVessel = ''
        self.deleteVessel = ''
        self.getToken = reverse('token')

        self.user1 = User.objects.create_user(
            username='testuser', password='12345')
        self.user2 = User.objects.create_user(
            username='testuser2', password='12345')

        self.addPayload = {
            "name": get_random_string(length=5),
            "naccs_code": get_random_string(length=5),
        }
        self.uppercaseAddPayload = {k: v.upper()
                                    for k, v in self.addPayload.items()}

    def tearDown(self):
        self.user1.delete()
        self.user2.delete()

    ################ Add Vessels ################
    def test_add_vessel(self):
        self.user_login(self.user1)
        res = self.client.post(self.addVessel, self.addPayload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.uppercaseAddPayload.items()
                        <= res.data['data'].items())

    def test_add_existing_vessel(self):
        self.user_login(self.user1)
        vessel = self.addRandomVessel(self.user1)
        payload = self.getPayloatFromVessel(vessel)

        res = self.client.post(self.addVessel, payload)

        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)

    def test_add_vessel_unauthorized(self):
        res = self.client.post(self.addVessel, self.addPayload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    ################ Update Vessels ################
    def test_name_update_vessel(self):
        partialPayload = {'name': self.addPayload.get('name')}
        testPartialPayload = {'name': self.uppercaseAddPayload['name']}

        self.user_login(self.user1)
        vessel = self.addRandomVessel(self.user1)
        self.updateURLWithId(vessel.id, 'update')
        res = self.client.put(self.updateVessel, partialPayload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(testPartialPayload.items()
                        <= res.data['data'].items())

    def test_naccs_update_vessel(self):
        partialPayload = {'naccs_code': self.addPayload.get('naccs_code')}
        testPartialPayload = {
            'naccs_code': self.uppercaseAddPayload['naccs_code']}
        self.user_login(self.user1)
        vessel = self.addRandomVessel(self.user1)

        self.updateURLWithId(vessel.id, 'update')
        res = self.client.put(self.updateVessel, partialPayload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(testPartialPayload.items() <= res.data['data'].items())

    def test_update_vessel(self):
        self.user_login(self.user1)
        vessel = self.addRandomVessel(self.user1)
        self.updateURLWithId(vessel.id, 'update')
        res = self.client.put(self.updateVessel, self.addPayload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(self.uppercaseAddPayload.items()
                        <= res.data['data'].items())

    def test_update_vessel(self):
        self.user_login(self.user1)
        vessel = self.addRandomVessel(self.user1)
        payload = self.getPayloatFromVessel(vessel)
        self.updateURLWithId(vessel.id, 'update')
        res = self.client.put(self.updateVessel, payload)

        self.assertEqual(res.status_code, status.HTTP_409_CONFLICT)

    def test_update_vessel_forbidden(self):
        self.user_login(self.user1)
        vessel = self.addRandomVessel(self.user1)

        self.user_login(self.user2)

        self.updateURLWithId(vessel.id, 'update')
        res = self.client.put(self.updateVessel, self.addPayload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_vessel_unauthorized(self):
        self.user_login(self.user1)
        vessel = self.addRandomVessel(self.user1)
        self.logout()

        self.updateURLWithId(vessel.id, 'update')
        res = self.client.put(self.addVessel, self.addPayload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    ################ Delete Vessels ################
    def test_delete_vessel(self):
        self.user_login(self.user1)
        vessel = self.addRandomVessel(self.user1)

        self.updateURLWithId(vessel.id, 'delete')
        res = self.client.delete(self.deleteVessel, self.addPayload)

        self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)

    def test_delete_vessel_forbidden(self):
        self.user_login(self.user1)
        vessel = self.addRandomVessel(self.user1)

        self.user_login(self.user2)

        self.updateURLWithId(vessel.id, 'delete')
        res = self.client.delete(self.deleteVessel, self.addPayload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_vessel_unauthorized(self):
        self.updateURLWithId(get_random_string(length=10), 'delete')
        res = self.client.delete(self.addVessel, self.addPayload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    ################ Get Vessels ################

    def test_get_all_vessel_list(self):
        res = self.client.get(self.retrieveVessels)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_get_user_vessel(self):
        self.user_login(self.user1)
        self.addRandomVessel(self.user1)

        self.user_login(self.user2)
        self.addRandomVessel(self.user2)

        res = self.client.get(self.retrieveUserVessels)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)

    def test_lookuo_a_vessel_from_user_vessel(self):
        self.user_login(self.user1)
        self.addRandomVessel(self.user1)
        vessel = self.addRandomVessel(self.user1)
        self.addRandomVessel(self.user1)

        self.updateURLWithId(vessel.id, 'get')
        res = self.client.get(self.retrieveUserVessel)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(model_to_dict(vessel).items()
                        <= res.data['data'].items())

    def test_lookuo_a_vessel_from_user_vessel_not_found(self):
        self.user_login(self.user1)
        vessel = self.addRandomVessel(self.user1)
        self.logout()

        self.user_login(self.user2)

        self.updateURLWithId(vessel.id, 'get')
        res = self.client.get(self.retrieveUserVessel)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_lookuo_a_vessel_from_user_vessel_unauthorized(self):
        self.user_login(self.user1)
        vessel = self.addRandomVessel(self.user1)
        self.logout()

        self.updateURLWithId(vessel.id, 'get')
        res = self.client.get(self.retrieveUserVessel)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def user_login(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer {}'.format(refresh.access_token))

    def logout(self):
        self.client.credentials()

    def addRandomVessel(self, user):
        return Vessel.objects.create(
            name=get_random_string(length=5),
            naccs_code=get_random_string(length=5),
            owner=user
        )

    def getPayloatFromVessel(self, vessel):
        return {
            "name": vessel.name,
            "naccs_code": vessel.naccs_code
        }

    def updateURLWithId(self, id, method):
        if method == 'get':
            self.retrieveUserVessel = reverse('retrieve-vessel', args=(id,))
        elif method == 'update':
            self.updateVessel = reverse('update-vessel', args=(id,))
        elif method == 'delete':
            self.deleteVessel = reverse('remove-vessel', args=(id,))
