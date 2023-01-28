"""Serializers for mycard APIs"""

from rest_framework import serializers

from core.models import MyCards


class MycardsSerializer(serializers.ModelSerializer):
    """Serializer for MyCards."""

    class Meta:
        model = MyCards
        fields = ['id', 'shopper', 'card', 'updated', 'created']
        read_only_fields = ['id', 'created']


class MycardsDetailSerializer(MycardsSerializer):
    """Serializer for MyCard detail view."""

    class Meta(MycardsSerializer.Meta):
        fields = '__all__'
