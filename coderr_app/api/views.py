from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min

from coderr_app.models import Offer, OfferDetail, Order
from shared.permissions import IsOwnerOrAdmin
from .serializers import OfferCreateSerializer, DetailedOfferSerializer, OfferListSerializer, OfferRetrieveDeleteSerializer, OfferUpdateSerializer, OrderListCreateSerializer
from .permissions import IsProviderOrAdmin
from .filters import CustomOfferFilter
from .pagination import OfferPageNumberPagination


class OfferListCreateView(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CustomOfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    pagination_class = OfferPageNumberPagination
    permission_classes = [IsProviderOrAdmin]

    def get_queryset(self):
        return Offer.objects.annotate(min_price=Min('details__price'), min_delivery_time=Min('details__delivery_time_in_days'))

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        else:
            return OfferListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        return Offer.objects.annotate(min_price=Min('details__price'), min_delivery_time=Min('details__delivery_time_in_days'))
    
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return OfferUpdateSerializer
        else:
            return OfferRetrieveDeleteSerializer


class DetailedOfferView(generics.RetrieveAPIView):
    queryset = OfferDetail.objects.all()
    serializer_class = DetailedOfferSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListCreateSerializer

    def get_queryset(self):
        try:
            if self.request.user.userprofile.type == 'customer':
                return Order.objects.filter(customer_user=self.request.user)
            elif self.request.user.userprofile.type == 'business':
                return Order.objects.filter(business_user=self.request.user)
        except:
            if self.request.user.is_superuser:
                return Order.objects.all()
            else:
                return Order.objects.none()

    def perform_create(self, serializer):
        offer_detail = serializer.validated_data['offer_detail']
        serializer.save(customer_user=self.request.user, business_user=offer_detail.offer.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    pass
