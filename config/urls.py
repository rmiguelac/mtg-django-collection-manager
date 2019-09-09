from django.urls import include, path
from django.contrib import admin
from django.views.generic import RedirectView

from rest_framework import routers

from collection_app import views


router = routers.DefaultRouter()
router.register(r'cards', views.CardViewSet)
router.register(r'users', views.UserViewSet)
router.register(r're-evalute', views.UpdateCollectionView, basename='re-evaluate')


urlpatterns = [
    path('', RedirectView.as_view(url='/api/')),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]


