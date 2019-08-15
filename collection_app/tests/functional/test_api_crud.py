from unittest.mock import patch

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
                payload = constants.GOOD_PAYLOAD.copy()
                response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @pytest.mark.django_db
    def test_post_invalid_card(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', side_effect=HTTPError):
            with patch('collection_app.cards_api.ScryfallAPI.validate', return_value=False):
                with patch('collection_app.cards_api.ScryfallAPI.get_card_sets', return_value=constants.GOOD_RESPONSE_SETS):
                    url = reverse('card-list')
                    payload = constants.GOOD_PAYLOAD.copy()
                    payload['name'] = 'Mx Pl'
                    response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_post_invalid_expansion_card(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', side_effect=constants.GOOD_RESPONSE):
            with patch('collection_app.cards_api.ScryfallAPI.get_card_sets', return_value=constants.GOOD_RESPONSE_SETS):
                url = reverse('card-list')
                payload = constants.GOOD_PAYLOAD.copy()
                payload['expansion'] = 'Wrong Set Name'
                response = self.client.post(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_post_unique_constraint_status_code(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            with patch('collection_app.cards_api.ScryfallAPI.get_card_sets', return_value=constants.GOOD_RESPONSE_SETS):
                url = reverse('card-list')
                payload = constants.GOOD_PAYLOAD.copy()
                self.client.post(url, payload, format='json')
                second_post_response = self.client.post(url, payload, format='json')

        self.assertEqual(second_post_response.status_code, status.HTTP_400_BAD_REQUEST)

    ## UPDATE methods
    @pytest.mark.django_db
    def test_update_valid(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            with patch('collection_app.cards_api.ScryfallAPI.get_card_sets', return_value=constants.GOOD_RESPONSE_SETS):
                create_url = reverse('card-list')
                payload = constants.GOOD_PAYLOAD.copy()
                self.client.post(create_url, payload, format='json')
                update_payload = constants.GOOD_PAYLOAD.copy()
                update_payload['quantity'] = 3
                card_id = self.client.get(path='/api/cards/').data[0]['url'][-2:]
                update_response = self.client.put(f'/api/cards/{card_id}', update_payload, format='json')

        self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_update_invalid_card(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            with patch('collection_app.cards_api.ScryfallAPI.get_card_sets', return_value=constants.GOOD_RESPONSE_SETS):
                create_url = reverse('card-list')
                payload = constants.GOOD_PAYLOAD.copy()
                self.client.post(create_url, payload, format='json')
                update_payload = constants.GOOD_PAYLOAD.copy()
                update_payload['name'] = 'Mx Pl'
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.BAD_RESPONSE):
            with patch('collection_app.cards_api.ScryfallAPI.validate', return_value=False):
                card_id = self.client.get(path='/api/cards/').data[0]['url'][-2:]
                update_response = self.client.put(f'/api/cards/{card_id}', update_payload, format='json')

        self.assertEqual(update_response.status_code, status.HTTP_400_BAD_REQUEST)

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

