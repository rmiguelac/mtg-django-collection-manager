from django.urls import path
from collection_app import views

urlpatterns = [
    path('cards/', views.collection_list),
    path('cards/<int:pk>/', views.collection_detail),
]
