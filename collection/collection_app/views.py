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
    return render(request, 'collection_app/collection.html', context)


def manage(request):
    return render(request, 'collection_app/manage.html')


def add_card(request):

    if request.method == 'POST':

        form = AddCardForm(request.POST)
        if form.is_valid():

            valid_card = validate(card_name=request.POST.get('card_name'),
                                  card_set_name=request.POST.get('card_set_name'))
            card_price = CardPricer(name=request.POST.get('card_name'),
                                    set_name=request.POST.get('card_set_name')).price
            if valid_card:

                card = Cards(name=request.POST.get('card_name'),
                             set=request.POST.get('card_set_name'),
                             condition=request.POST.get('card_condition'),
                             foil=request.POST.get('card_is_foil'),
                             quantity=request.POST.get('card_quantity'),
                             value=card_price)
                card.save()

                return HttpResponse("Added, i guess...")
            else:
                return HttpResponse("Something went wrong")

    else:
        form = AddCardForm()

    return render(request, 'collection_app/add_card.html', {'form': form})


def remove_card(request):
    return render(request, 'collection_app/remove_card.html')
