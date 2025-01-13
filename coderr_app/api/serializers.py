from rest_framework import serializers
from coderr_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = '__all__'


class OfferDetailLinkSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailLinkSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = '__all__'

    def get_user_details(self, obj):
        user = obj.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }

    def get_min_price(self, obj):
        details = obj.details.all()
        if not details.exists():
            return None
        return min(detail.price for detail in details)

    def get_min_delivery_time(self, obj):
        details = obj.details.all()
        if not details.exists():
            return None
        return min(detail.delivery_time_in_days for detail in details)
