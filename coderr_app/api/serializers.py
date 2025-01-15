from rest_framework import serializers
from coderr_app.models import Offer, OfferDetail


class DetailedOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def validate_features(self, data):
        amount = len(data)
        if amount < 1:
            raise serializers.ValidationError('At least one feature is required!')
        return data


class DetailedOfferUrlSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferGetAdditionalFieldsSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField(read_only=True)
    min_price = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()

    class Meta:
        model = Offer
        fields = ['min_price', 'min_delivery_time', 'user_details']

    def get_user_details(self, obj):
        user = obj.user
        return {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username
        }


class OfferListSerializer(OfferGetAdditionalFieldsSerializer, serializers.ModelSerializer):
    details = DetailedOfferUrlSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']


class OfferDetailSerializer(OfferGetAdditionalFieldsSerializer, serializers.ModelSerializer):
    details = DetailedOfferSerializer(many=True, read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']


class OfferCreateSerializer(serializers.ModelSerializer):
    details = DetailedOfferSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def validate_details(self, data):
        if len(data) != 3:
            raise serializers.ValidationError('Need 3 details!')
        
        offer_types = [offer_detail['offer_type'] for offer_detail in data]
        if 'basic' not in offer_types:
            raise serializers.ValidationError('basic is not available!')
        if 'standard' not in offer_types:
            raise serializers.ValidationError('standard is not available!')
        if 'premium' not in offer_types:
            raise serializers.ValidationError('premium is not available!')
        return data

    def create(self, validated_data):
        print('validated_data:', validated_data)
        offer_details_list = validated_data.pop('details')
        offer_details = [OfferDetail(**item) for item in offer_details_list]
        offer = Offer.objects.create(**validated_data)
        offer.details.set(offer_details, bulk=False)
        return offer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        fields_to_remove = ['user', 'created_at', 'updated_at']
        for field in fields_to_remove:
            representation.pop(field, None)
        return representation
