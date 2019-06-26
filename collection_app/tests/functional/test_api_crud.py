import pytest
import json

from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase, force_authenticate
from rest_framework import status


class TestCollection(APITestCase):

    PAYLOAD = {
        'name': 'Mox Opal',
        'expansion': 'Scars of Mirrodin',
        'condition': 'NM',
        'foil': False,
        'quantity': 4,
        'value': 94.00,
    }

    """
    TODO: Check why API functional tests are not working with user
    """

    @pytest.fixture
    @pytest.mark.django_db
    def user(self):
        user = User.objects.create_user(username='user', password='user')
        user.save()

    # POST methods
    @pytest.mark.django_db
    def test_valid_post(self):
        request = self.client.post('/collection/', json.dumps(self.PAYLOAD), format='json')
        force_authenticate(request=request, user=self.user)
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    @pytest.mark.django_db
    def test_post_forbidden(self):
        response = self.client.post('/collection/', json.dumps(self.PAYLOAD), format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @pytest.mark.django_db
    def test_post_invalid_card(self):
        data = self.PAYLOAD
        data['name'] = 'Mx Pl'
        response = self.client.post('/collection/', json.dumps(data), format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #@pytest.mark.django_db
    #def test_post_invalid_expansion_card(self, factory):
    #    pass

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
