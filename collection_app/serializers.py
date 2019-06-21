from rest_framework import serializers

from collection_app.models import Card


class CardSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Card
        fields = '__all__'