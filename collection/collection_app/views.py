from django.http import HttpResponse
from django.shortcuts import render

import logging

from .models import Cards
from .validator import validate
from .pricer import CardPricer
from .forms import AddCardForm


logger = logging.getLogger(__name__)


def collection(request):
    cards = Cards.objects.all()
    context = {'cards': cards,}
    return render(request, 'collection.html', context)


def manage(request):
    return render(request, 'manage.html')


def add_card(request):

    if request.method == 'POST':

        card_info = {'name': request.POST.get('card_name'),
                     'set': request.POST.get('card_set_name'),
                     'condition': request.POST.get('card_condition'),
                     'foil': request.POST.get('card_is_foil'),
                     'quantity': request.POST.get('card_quantity')}

        form = AddCardForm(request.POST)

        if form.is_valid():

            card = Cards.objects.filter(name=card_info['name']).filter(set=card_info['set']).filter(condition=card_info['condition'])

            if not card:
                card_exists = validate(card_name=card_info['name'], card_set_name=card_info['set'])

                if card_exists:

                    card_price = CardPricer(name=card_info['name'], set_name=card_info['set']).price

                    c = Cards(name=card_info['name'], set=card_info['set'], condition=card_info['condition'],
                                 foil=card_info['foil'], quantity=card_info['quantity'], value=card_price)
                    c.save()

                    return HttpResponse(f"{card_info['name']} added to you collection!")
                else:
                    return HttpResponse(f"Card {card_info['name']} does not seem to exist!")

            else:
                card_price = CardPricer(name=card_info['name'], set_name=card_info['set']).price
                already_have_quantity = int(card.values()[0].get('quantity'))
                card.update(quantity=already_have_quantity + int(card_info['quantity']))
                card.update(value=card_price)
                return HttpResponse(f"{card_info['name']} updated on your collection")


    else:
        form = AddCardForm()

    return render(request, 'collection_app/add_card.html', {'form': form})


def remove_card(request):
    return render(request, 'remove_card.html')
