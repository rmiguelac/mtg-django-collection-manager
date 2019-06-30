from unittest.mock import MagicMock, patch

from django.contrib.auth.models import User
import pytest
from requests import HTTPError
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from collection_app.tests import constants


class TestCollection(APITestCase):

    @pytest.mark.django_db
    def setUp(self):
        # Create test user
        credentials = {'username': 'Eiganjo', 'password': 'Lord'}
        User.objects.create_user(**credentials)
        self.client.login(**credentials)

    # POST methods
    @pytest.mark.django_db
    def test_valid_post(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            with patch('collection_app.cards_api.ScryfallAPI.get_card_sets', return_value=constants.GOOD_RESPONSE_SETS):
                url = reverse('card-list')
                data = constants.GOOD_PAYLOAD
                response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @pytest.mark.django_db
    def test_post_invalid_card(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', side_effect=HTTPError):
            with patch('collection_app.cards_api.ScryfallAPI.validate', return_value=False):
                with patch('collection_app.cards_api.ScryfallAPI.get_card_sets', return_value=constants.GOOD_RESPONSE_SETS):
                    url = reverse('card-list')
                    data = constants.GOOD_PAYLOAD
                    data['name'] = 'Mx Pl'
                    response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_post_invalid_expansion_card(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', side_effect=constants.GOOD_RESPONSE):
            with patch('collection_app.cards_api.ScryfallAPI.validate', return_value=True):
                with patch('collection_app.cards_api.ScryfallAPI.get_card_sets', return_value=constants.GOOD_RESPONSE_SETS):
                    url = reverse('card-list')
                    data = constants.GOOD_PAYLOAD
                    data['expansion'] = 'Wrong Set Name'
                    response = self.client.post(url, data, format='json')

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

    #@pytest.mark.django_db
    #def test_post_forbidden(self):
    #    self.client.logout()
    #    response = self.client.post('/collection/', json.dumps(self.PAYLOAD), format='json')
    #    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    ## DELETE methods
    #@pytest.mark.django_db
    #def test_valid_delete(self, factory):
    #    pass
