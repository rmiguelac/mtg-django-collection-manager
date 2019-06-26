import pytest
from rest_framework.test import APIRequestFactory


@pytest.fixture
def factory():
    return APIRequestFactory()


class TestCard:

    # POST methods
    @pytest.mark.django_db
    def test_post_invalid_card(self, factory):
        pass

    @pytest.mark.django_db
    def test_post_invalid_expansion_card(self, factory):
        pass

    @pytest.mark.django_db
    def test_post_unique_constraint(self, factory):
        pass

    @pytest.mark.django_db
    def test_post(self, factory):
        pass

    # UPDATE methods
    @pytest.mark.django_db
    def test_update_to_invalid_card(self, factory):
        pass

    @pytest.mark.django_db
    def test_update_to_invalid_expansion_card(self, factory):
        pass

    @pytest.mark.django_db
    def test_update_unique_constraint(self, factory):
        pass

    @pytest.mark.django_db
    def test_update_invalid_value(self, factory):
        pass

    @pytest.mark.django_db
    def test_update(self, factory):
        pass

    # DELETE methods
    @pytest.mark.django_db
    def test_delete(self, factory):
        pass
