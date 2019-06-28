from django.urls import include, path
from django.contrib import admin

from rest_framework import routers

from collection_app import views


router = routers.DefaultRouter()
router.register(r'cards', views.CardViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
