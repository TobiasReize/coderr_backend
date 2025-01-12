from django.urls import path, include
from rest_framework import routers
from .views import OfferViewSet, OrderViewSet


router = routers.DefaultRouter()
router.register(r'offers', OfferViewSet)
router.register(r'orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
