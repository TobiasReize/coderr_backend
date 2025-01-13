from rest_framework import viewsets, generics

from coderr_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class OfferDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer


class OrderViewSet(viewsets.ModelViewSet):
    pass
