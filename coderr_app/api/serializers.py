from rest_framework import serializers
from django.contrib.auth.models import User
from coderr_app.models import Offer, OfferDetail, Order, Review
from user_auth_app.models import UserProfile


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
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class OfferGetAdditionalFieldsSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
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
        fields = ['id', 'title', 'image', 'description', 'created_at', 'updated_at', 'details']
    
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
        fields = ['id', 'title', 'description', 'image', 'details']
    
    def update(self, instance, validated_data):
        response_data = {}
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)

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

                response_data = {
                    'id': instance.id,
                    'title': instance.title,
                    'description': instance.description,
                    'image': instance.image,
                    'details': [
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
                }

        instance.save()
        return response_data


class OrderSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.PrimaryKeyRelatedField(queryset=OfferDetail.objects.all(), write_only=True, source='offer_detail')
    title = serializers.CharField(source='offer_detail.title', max_length=100, read_only=True)
    revisions = serializers.IntegerField(source='offer_detail.revisions', read_only=True)
    delivery_time_in_days = serializers.IntegerField(source='offer_detail.delivery_time_in_days', read_only=True)
    price = serializers.DecimalField(source='offer_detail.price', max_digits=10, decimal_places=2, read_only=True)
    features = serializers.ListField(source='offer_detail.features', child=serializers.CharField(max_length=100), read_only=True)
    offer_type = serializers.ChoiceField(source='offer_detail.offer_type', choices=['basic', 'standard', 'premium'], read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type', 'status', 'created_at', 'updated_at', 'offer_detail_id']
        read_only_fields = ['customer_user', 'business_user', 'status' 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        if len(validated_data) > 1 or 'status' not in validated_data:
            raise serializers.ValidationError("Only the 'status' field can be updated.")
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description', 'created_at', 'updated_at']
        read_only_fields = ['reviewer', 'created_at', 'updated_at']

    def validate(self, data):
        user = self.context['request'].user
        business_user = data.get('business_user')
        
        if business_user and Review.objects.filter(reviewer=user, business_user=business_user).exists():
            raise serializers.ValidationError("You have already reviewed this business user.")
        return data

    def validate_business_user(self, data):
        if UserProfile.objects.get(user=data).type != 'business':
            raise serializers.ValidationError("User is not a business user.")
        else:
            return data

    def update(self, instance, validated_data):
        if len(validated_data) > 2:
            raise serializers.ValidationError("Only the 'rating' and 'description' field can be updated.")
        elif ('rating' not in validated_data) and ('description' not in validated_data):
            raise serializers.ValidationError("Only the 'rating' and 'description' field can be updated.")
        
        instance.rating = validated_data.get('rating', instance.rating)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance
