from django.urls import path, include
from rest_framework import routers
from .views import OfferDetailView, OfferListCreateView, DetailedOfferView, OrderViewSet


# router = routers.DefaultRouter()
# router.register(r'offers', OfferViewSet, basename='offer')
# router.register(r'orders', OrderViewSet)


urlpatterns = [
    # path('', include(router.urls)),
    path('offers/', OfferListCreateView.as_view(), name='offer'),
    path('offers/<int:pk>/', OfferDetailView.as_view(), name='offer-detail'),
    path('offerdetails/<int:pk>/', DetailedOfferView.as_view(), name='detailed-offer'),
    # path('order-count/<int:pk>/'),
    # path('completed-order-count/<int:pk>/'),
    # path('base-info/'),
]
