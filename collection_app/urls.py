from django.urls import path

app_name = 'collection_app'

urlpatterns = [
    path('cards/', name='card-list'),
    path('cards/{pk}/', name='card-details'),
    path('update-collection/', name='update-collection'),
]
