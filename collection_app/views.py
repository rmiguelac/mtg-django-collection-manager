import logging

from django.http import HttpResponse
from django.shortcuts import render

from rest_framework import viewsets

from collection_app.models import Card
from collection_app.serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cards to be viewed or edited.
    """

    queryset = Card.objects.all().order_by('value')
    serializer_class = CardSerializer