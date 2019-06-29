import pytest

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

"""

TODO: Mock the external API - Scryfall

The validators under the serializerrs use them and should not consume it directly on 
the tests.

"""


class TestCollection(APITestCase):

    @pytest.mark.django_db
    def setUp(self):
        credentials = {'username': 'test_user', 'password': 'password'}
        User.objects.create_user(**credentials)
        self.client.login(**credentials)

        self.PAYLOAD = {
            'name': 'Mox Opal',
            'expansion': 'Scars of Mirrodin',
            'condition': 'NM',
            'foil': False,
            'quantity': 4,
        }

    # POST methods
    @pytest.mark.django_db
    def test_valid_post(self):
        url = reverse('card-list')
        request = self.client.post(url, self.PAYLOAD, format='json')
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    #@pytest.mark.django_db
    #def test_post_forbidden(self):
    #    self.client.logout()
    #    response = self.client.post('/collection/', json.dumps(self.PAYLOAD), format='json')
    #    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @pytest.mark.django_db
    def test_post_invalid_card(self):
        url = reverse('card-list')
        self.PAYLOAD['name'] = 'Mx Pl'
        response = self.client.post(url, self.PAYLOAD, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_post_invalid_expansion_card(self):
        url = reverse('card-list')
        self.PAYLOAD['expansion'] = 'Wrong Set Name'
        response = self.client.post(url, self.PAYLOAD, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #@pytest.mark.django_db
    #def test_post_unique_constraint(self, factory):
    #    pass

    ## UPDATE methods
    #@pytest.mark.django_db
    #def test_valid_update(self, factory):
    #    pass

    #@pytest.mark.django_db
    #def test_update_to_invalid_card(self, factory):
    #    pass

    #@pytest.mark.django_db
    #def test_update_to_invalid_expansion_card(self, factory):
    #    pass

    #@pytest.mark.django_db
    #def test_update_unique_constraint(self, factory):
    #    pass

    #@pytest.mark.django_db
    #def test_update_invalid_value(self, factory):
    #    pass

    ## DELETE methods
    #@pytest.mark.django_db
    #def test_valid_delete(self, factory):
    #    pass
