from django.contrib import admin
from django.urls import include, path

from rest_framework import routers

from collection_app import views

router = routers.DefaultRouter()
router.register(r'collection', views.CardViewSet)


urlpatterns = [
    path(route='', view=include(router.urls)),
    path(route='api-auth/', view=include('rest_framework.urls'), name='rest_framework'),
    #path(route='admin/', view=admin.site.urls, name='admin'),
]
