from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path(route='admin/', view=admin.site.urls, name='admin'),
    path(route='collection/', view=include('collection_app.urls'), name='collection'),
    path(route='collection/manage/', view=include('collection_app.urls'), name='manage'),
]
