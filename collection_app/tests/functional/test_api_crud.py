from unittest.mock import patch

from django.contrib.auth.models import User
import pytest
from django.db.models import Sum
from requests import HTTPError
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse

from collection_app.cards import CardScryfallImpl
from collection_app.tests import constants
from collection_app.models import Card


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
            url = reverse('card-list')
            payload = constants.MOX_PAYLOAD.copy()
            response = self.client.post(url, payload, format='json')

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @pytest.mark.django_db
    def test_post_invalid_card(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', side_effect=HTTPError):
            url = reverse('card-list')
            payload = constants.MOX_PAYLOAD.copy()
            payload['name'] = 'Mx Pl'
            response = self.client.post(url, payload, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_post_invalid_expansion_card(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', side_effect=HTTPError):
            url = reverse('card-list')
            payload = constants.MOX_PAYLOAD.copy()
            payload['expansion'] = 'Wrong'
            response = self.client.post(url, payload, format='json')

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_post_unique_constraint_status_code(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            url = reverse('card-list')
            payload = constants.MOX_PAYLOAD.copy()
            self.client.post(url, payload, format='json')
            second_post_response = self.client.post(url, payload, format='json')

            self.assertEqual(second_post_response.status_code, status.HTTP_400_BAD_REQUEST)

    # UPDATE methods
    @pytest.mark.django_db
    def test_update_valid(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            create_url = reverse('card-list')
            payload = constants.MOX_PAYLOAD.copy()
            self.client.post(create_url, payload, format='json')
            update_payload = constants.MOX_PAYLOAD.copy()
            update_payload['quantity'] = 3
            card_id = self.client.get(path='/api/cards/').data[0]['url'][-2:]
            update_response = self.client.put(f'/api/cards/{card_id}', update_payload, format='json')

            self.assertEqual(update_response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db
    def test_update_invalid_card(self):
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.GOOD_RESPONSE):
            create_url = reverse('card-list')
            payload = constants.MOX_PAYLOAD.copy()
            self.client.post(create_url, payload, format='json')
            update_payload = constants.MOX_PAYLOAD.copy()
            update_payload['name'] = 'Mx Pl'
        with patch('collection_app.cards_api.ScryfallAPI._get_card', return_value=constants.BAD_RESPONSE):
            with patch('collection_app.cards_api.ScryfallAPI.validate', return_value=False):
                card_id = self.client.get(path='/api/cards/').data[0]['url'][-2:]
                update_response = self.client.put(f'/api/cards/{card_id}', update_payload, format='json')

                self.assertEqual(update_response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.django_db
    def test_update_collection_value(self):
        """
        For each card that there is in the DB, get its id and perform an update against the API
        """
        collection_value_pre_update = Card.objects.all().aggregate(Sum(('value')))
        self.client.get('/api/re-evaluate/')
        collection_value_post_update = Card.objects.all().aggregate(Sum('value'))
        self.assertNotEqual(collection_value_pre_update, collection_value_post_update)

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

