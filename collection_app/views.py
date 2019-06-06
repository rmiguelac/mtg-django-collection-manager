import logging

from django.http import HttpResponse
from django.shortcuts import render

from .models import Cards
from .cards import Card
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
            info = {'name': form.cleaned_data['name'],
                    'set': form.cleaned_data['set_name'],
                    'condition': form.cleaned_data['condition'],
                    'foil': form.cleaned_data['is_foil'],
                    'quantity': form.cleaned_data['quantity']}
            card_is_valid = Card(name=info['name'])
            info['price'] = card_is_valid.value
            if card_is_valid:
                card_is_in_db = Cards.objects.filter(
                    name=info['name']
                ).filter(
                    set=info['set']
                ).filter(
                    condition=info['condition']
                ).filter(
                    foil=info['foil']
                )
                card = card_is_in_db
                if card_is_in_db:
                    already_have_quantity = int(card.values()[0].get('quantity'))
                    card.update(quantity=already_have_quantity + int(info['quantity']))
                    return HttpResponse(f"{info['name']} updated on your collection")
                else:
                    c = Cards(name=info['name'], set=info['set'], condition=info['condition'],
                              foil=info['foil'], quantity=info['quantity'], value=info['price'])
                    c.save()
                    return HttpResponse(f"{info['name']} added to you collection!")

    else:
        form = AddCardForm()

    return render(request, 'collection_app/add_card.html', {'form': form})


def remove_card(request):
    return render(request, 'collection_app/remove_card.html')
