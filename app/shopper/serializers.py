"""Serializer for shopper APIs"""

from rest_framework import serializers

from core.models import Shopper


class ShopperSerializer(serializers.ModelSerializer):
    """Serializer for shoppers."""

    class Meta:
        model = Shopper
        fields = ['id', 'first_name', 'last_name',
                  'lat', 'long']


class ShopperDetailSerializer(ShopperSerializer):

    class Meta(ShopperSerializer.Meta):
        fields = ShopperSerializer.Meta.fields + [
            'address', 'address2', 'city', 'region', 'post_code', 'country',
            'phone_number', 'updated', 'active']
