from django.shortcuts import render
from .models import Cards

def collection(request):
    cards = Cards.objects.all()
    context = {'cards': cards,}
    return render(request, 'collection_app/collection.html', context)
