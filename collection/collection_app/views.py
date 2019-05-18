from django.shortcuts import render
from .models import Cards

def collection(request):
    cards = Cards.objects.all()
    context = {'cards': cards,}
    return render(request, 'collection_app/collection.html', context)

def manage(request):
    return render(request, 'collection_app/manage.html')

def add_card(request):
    return render(request, 'collection_app/add_card.html')

def remove_card(request):
    return render(request, 'collection_app/remove_card.html')
