"""Serializer for shopper APIs"""

from rest_framework import serializers

from core.models import Shopper
from mycards.serializers import MycardsDetailSerializer
from mycardshistory.serializers import MycardsHistoryDetailSerializer

class ShopperSerializer(serializers.ModelSerializer):
    """Serializer for shoppers."""
    # my_cards = MycardsDetailSerializer(many=True, read_only=True)
    # finalized_cards = MycardsHistoryDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Shopper
        fields = ['id', 'first_name', 'last_name',
                  'address', 'city', 'post_code',
                  'lat', 'long']
        read_only_fields = ['id']


class ShopperDetailSerializer(ShopperSerializer):

    class Meta(ShopperSerializer.Meta):
        fields = ShopperSerializer.Meta.fields + [
            'address', 'address2', 'city', 'region', 'post_code', 'country',
            'phone_number', 'updated', 'active']
