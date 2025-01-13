from django.urls import path, include
from rest_framework import routers
from .views import OfferViewSet, OfferDetailView, OrderViewSet


router = routers.DefaultRouter()
router.register(r'offers', OfferViewSet, basename='offer')
# router.register(r'orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('offerdetails/<int:pk>/', OfferDetailView.as_view(), name='offer-details'),
    # path('order-count/<int:pk>/'),
    # path('completed-order-count/<int:pk>/'),
    # path('base-info/'),
]
