from django.contrib.auth.models import User
from rest_framework import viewsets

from collection_app.models import Card
from collection_app.serializers import CardSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cards to viewed or edited
    """
    queryset = Card.objects.all().order_by('-value')
    serializer_class = CardSerializer
