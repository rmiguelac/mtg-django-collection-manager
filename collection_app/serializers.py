from rest_framework import serializers

from collection_app.models import Card
from collection_app.cards import CardScryfallImpl


class CardSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Card
        fields = '__all__'
        read_only_fields = ('value',)

    @staticmethod
    def validate_name(value):
        """
        Custom validator on name field
        If name is not validated against external API, return exception

        :param value: Card name
        :return: value in case validated, exception otherwise
        """

        card = CardScryfallImpl(name=value)
        if card.is_valid:
            return value
        raise serializers.ValidationError('There is no such Card {name}'.format(name=value))

    @staticmethod
    def validate_expansion(value):
        """
        Custom validator on expansion field
        If expansion is not valid against external API, return exception

        :param value: Card expansion (set)
        :return: value
        """

        pass

    def create(self, validated_data):
        """
        Create and return new 'Card' instance, given the validated data
        """
        args = {
            'name': validated_data['name'],
            'expansion': validated_data['expansion'],
            'condition': validated_data['condition'],
            'foil': validated_data['foil'],
        }

        card = CardScryfallImpl(**args)
        validated_data['value'] = card.value

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

    """
    
    On adding a card, if unique is not violated, add it
    If unique already exists, update the card quantity and value    
    
    """
