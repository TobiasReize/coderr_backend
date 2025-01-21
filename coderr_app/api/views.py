from rest_framework import generics, filters, status, viewsets
from rest_framework.views import APIView, Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Min, Avg

from coderr_app.models import Offer, OfferDetail, Order, Review
from user_auth_app.models import UserProfile
from shared.permissions import IsOwnerOrAdmin
from .serializers import OfferCreateSerializer, DetailedOfferSerializer, OfferListSerializer, OfferRetrieveDeleteSerializer, OfferUpdateSerializer, OrderSerializer, ReviewSerializer
from .permissions import IsProviderOrAdmin, OrderIsOwnerOrAdmin, IsCustomerOrAdmin, ReviewIsOwner
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
    serializer_class = OrderSerializer
    permission_classes = [IsCustomerOrAdmin]

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
    serializer_class = OrderSerializer
    http_method_names = ['options', 'get', 'patch', 'delete']
    permission_classes = [OrderIsOwnerOrAdmin]

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


class OrderCountView(APIView):
    def get(self, request, pk, *args, **kwargs):
        business_user = UserProfile.objects.filter(user=pk)
        if business_user:
            queryset = Order.objects.filter(business_user_id=pk, status='in_progress')
            order_count = queryset.count()
            return Response({'order_count': order_count}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Business user not found.'}, status=status.HTTP_404_NOT_FOUND)


class CompletedOrderCountView(APIView):
    def get(self, request, pk, *args, **kwargs):
        business_user = UserProfile.objects.filter(user=pk)
        if business_user:
            queryset = Order.objects.filter(business_user_id=pk, status='completed')
            order_count = queryset.count()
            return Response({'completed_order_count': order_count}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Business user not found.'}, status=status.HTTP_404_NOT_FOUND)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsCustomerOrAdmin | ReviewIsOwner]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user_id', 'reviewer_id']
    ordering_fields = ['updated_at', 'rating']
    http_method_names = ['options', 'get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)


class BaseInfoView(APIView):
    def get(self, request):
        review_count = Review.objects.all().count()
        average_rating = round(Review.objects.aggregate(Avg('rating', default=0))['rating__avg'], 1)
        business_profile_count = UserProfile.objects.filter(type='business').count()
        offer_count = Offer.objects.all().count()

        data = {
            'review_count': review_count,
            'average_rating': average_rating,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count
        }
        return Response(data, status=status.HTTP_200_OK)
