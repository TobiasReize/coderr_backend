from rest_framework import viewsets
from coderr_app.models import Offer
from .serializers import OfferSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class OrderViewSet(viewsets.ModelViewSet):
    pass
