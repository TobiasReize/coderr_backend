from rest_framework import serializers
from coderr_app.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    # def to_representation(self, instance):        # Möglichkeit 2
    #     return f"/offerdetails/{instance.id}/"


class OfferSerializer(serializers.ModelSerializer):
    # details = serializers.StringRelatedField(many=True)     # nutzt die __str__ Methode des OfferDetail model
    details = OfferDetailSerializer(many=True)    # Möglichkeit 2
    user_details = serializers.SerializerMethodField(read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']
        read_only_fields = ['user']


    def get_user_details(self, obj):
        user = obj.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }


    def get_min_price(self, obj):
        print('min_price:', obj)
        details = obj.details.all()
        print('min_price_all:', details)
        if not details.exists():
            return None
        return min(detail.price for detail in details)


    def get_min_delivery_time(self, obj):
        details = obj.details.all()
        if not details.exists():
            return None
        return min(detail.delivery_time_in_days for detail in details)


    def create(self, validated_data):
        print('validated_data:', validated_data)
        offer_details_list = validated_data.pop('details')
        min_price = min([offer_details_item['price'] for offer_details_item in offer_details_list])
        print('min_price:', min_price)
        min_delivery_time = min([offer_details_item['delivery_time_in_days'] for offer_details_item in offer_details_list])
        print('min_delivery_time:', min_delivery_time)
        offer_details = [OfferDetail(**item) for item in offer_details_list]
        offer = Offer.objects.create(min_price=min_price, min_delivery_time=min_delivery_time, **validated_data)
        offer.details.set(offer_details, bulk=False)
        return offer
