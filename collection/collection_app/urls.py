from django.urls import path

from . import views

urlpatterns = [
    path(route='', view=views.collection, name='collection'),
    path(route='manage/', view=views.manage, name='manage'),
    path(route='manage/add', view=views.add_card, name='add_card'),
    path(route='manage/remove', view=views.remove_card, name='remove_card'),
]
