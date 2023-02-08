"""Serializers for mycard APIs"""

from rest_framework import serializers

from core.models import MyCardsHistory


class MycardsHistorySerializer(serializers.ModelSerializer):
    """Serializer for MyCards."""

    class Meta:
        model = MyCardsHistory
        fields = ['id', 'shopper', 'company']
        read_only_fields = ['id', 'created']


class MycardsHistoryDetailSerializer(MycardsHistorySerializer):
    """Serializer for MyCard detail view."""

    class Meta(MycardsHistorySerializer.Meta):
        fields = MycardsHistorySerializer.Meta.fields + [
            'code', 'finalized'
        ]
