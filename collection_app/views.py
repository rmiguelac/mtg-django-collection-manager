from django.contrib.auth.models import User
from django_filters.rest_framework import FilterSet, NumberFilter
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from collection_app.cards import CardScryfallImpl
from collection_app.models import Card
from collection_app.serializers import CardSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class CardFilter(FilterSet):
    """
    Filter which enables search using name, expansion or value
    """

    min_value = NumberFilter(field_name='value', lookup_expr='gte')
    max_value = NumberFilter(field_name='value', lookup_expr='lte')

    class Meta:
        model = Card
        fields = {
            'name': ['icontains'],
            'expansion': ['icontains'],
        }


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cards to viewed or edited
    """
    queryset = Card.objects.all().order_by('-value')
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = CardFilter

    def perform_create(self, serializer):
        """
        Override the default perform_create to pass the owner as well
        """
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Card.objects.filter(owner=self.request.user)


class UpdateCollectionView(viewsets.ViewSet):

    def list(self, request, format=None):
        cards = Card.objects.filter(owner=request.user)
        for card in cards:
            tmp_card = CardScryfallImpl(name=card.name, expansion=card.expansion, foil=card.foil)
            tmp_card_value = tmp_card.value
            card.value = tmp_card_value
            card.save()

        return Response('Collection value updated')
