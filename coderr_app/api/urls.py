from django.urls import path, include
from rest_framework import routers
from .views import OfferDetailView, OfferListCreateView, DetailedOfferView, OrderListCreateView, OrderDetailView


urlpatterns = [
    path('offers/', OfferListCreateView.as_view(), name='offer'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', DetailedOfferView.as_view(), name='detailed-offer'),
    path('orders/', OrderListCreateView.as_view(), name='order'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    # path('order-count/<int:pk>/'),
    # path('completed-order-count/<int:pk>/'),
    # path('base-info/'),
]
