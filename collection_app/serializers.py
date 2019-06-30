from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from collection_app.models import Card
from collection_app.cards import CardScryfallImpl


class CardSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Card
        fields = '__all__'
        read_only_fields = ('value',)

    def validate(self, data):
        """
        Custom validator on whole request data
        If data is not valid against external API, return exception

        :param data: dict with whole Card model fields
        :return: value
        """

        card = CardScryfallImpl(name=data['name'])

        if card.is_valid and data['expansion'] in card.sets:
            data['value'] = card.value
            return data
        raise serializers.ValidationError(
            'There is no such card {card} in {exp} set'.format(card=data['name'], exp=data['expansion'])
        )

    def create(self, validated_data):
        """
        Create and return new 'Card' instance, given the validated data
        """
        return Card.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return existing 'Card' class
        """
        instance.name = validated_data.get('name', instance.name)
        instance.expansion = validated_data.get('set', instance.expansion)
        instance.condition = validated_data.get('condition', instance.condition)
        instance.foil = validated_data.get('foil', instance.foil)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance
