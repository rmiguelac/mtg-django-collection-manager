from django.urls import path

from . import views

urlpatterns = [
    path(route='', view=views.collection, name='collection'),
    path(route='manage/', view=views.manage, name='manage'),
]
