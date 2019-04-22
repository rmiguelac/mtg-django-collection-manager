from django.http import HttpResponse
from django.template import loader
from .models import Cards

def collection(request):
    cards = Cards.objects.all()
    template = loader.get_template('collection_app/collection.html')
    context = {'cards': cards,}
    return HttpResponse(template.render(context, request))
