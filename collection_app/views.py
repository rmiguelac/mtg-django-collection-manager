from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Override the default perform_create to pass the owner as well
        """
        serializer.save(owner=self.request.user)
