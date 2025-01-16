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
        if obj.user:
            return {
                'first_name': obj.user.first_name,
                'last_name': obj.user.last_name,
                'username': obj.user.username
            }


class OfferListSerializer(OfferGetAdditionalFieldsSerializer, serializers.ModelSerializer):
    details = DetailedOfferUrlSerializer(many=True, read_only=True)

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


class OfferRetrieveDeleteSerializer(OfferGetAdditionalFieldsSerializer, serializers.ModelSerializer):
    details = DetailedOfferSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time', 'user_details']
        read_only_fields = ['user', 'created_at', 'updated_at']


class OfferUpdateSerializer(serializers.ModelSerializer):
    details = DetailedOfferSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'title', 'description', 'details']
    
    def update(self, instance, validated_data):
        data = {}
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        data['id'] = instance.id
        data['title'] = instance.title
        data['description'] = instance.description

        if 'details' in validated_data:
            offer_details_data = validated_data.pop('details')
            for detail_data in offer_details_data:
                type = detail_data.get('offer_type')
                detail_instance = instance.details.get(offer_type=type)
                detail_instance.title = detail_data.get('title', detail_instance.title)
                detail_instance.revisions = detail_data.get('revisions', detail_instance.revisions)
                detail_instance.delivery_time_in_days = detail_data.get('delivery_time_in_days', detail_instance.delivery_time_in_days)
                detail_instance.price = detail_data.get('price', detail_instance.price)
                detail_instance.features = detail_data.get('features', detail_instance.features)
                detail_instance.save()
                
                data['details'] = [
                    {
                        'id': detail_instance.id,
                        'title': detail_instance.title,
                        'revisions': detail_instance.revisions,
                        'delivery_time_in_days': detail_instance.delivery_time_in_days,
                        'price': detail_instance.price,
                        'features': detail_instance.features,
                        'offer_type': detail_instance.offer_type
                    }
                ]

        instance.save()
        return data
    
    # def to_representation(self, instance):
    #     request_method = self.context['request'].method
    #     if request_method == 'PATCH':
    #         return self.handle_patch_representation(instance)
    #     else:
    #         return super().to_representation(instance)
