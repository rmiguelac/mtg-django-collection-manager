from django.urls import path

from . import views

urlpatterns = [
    path('', views.collection, name='collection'),
    #path('manage', views.manage, name='manage'),
]
