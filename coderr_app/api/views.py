from rest_framework import viewsets, generics, filters
from django_filters.rest_framework import DjangoFilterBackend

from coderr_app.models import Offer, OfferDetail
from .serializers import OfferSerializer, OfferDetailSerializer, OfferListSerializer
from .permissions import IsOwnerOrAdmin
from .filters import CustomOfferFilter


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CustomOfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

    def list(self, request, *args, **kwargs):
        self.serializer_class = OfferListSerializer
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferDetailView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = OfferDetailSerializer


class OrderViewSet(viewsets.ModelViewSet):
    pass
