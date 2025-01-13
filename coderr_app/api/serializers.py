from rest_framework import serializers
from coderr_app.models import Offer


class OfferSerializer(serializers.ModelSerializer):
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = '__all__'

    def get_min_price(self, objects):
        pass

    def get_min_delivery_time(self, objects):
        pass
    