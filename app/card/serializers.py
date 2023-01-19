"""Serializers for card APIs"""

from rest_framework import serializers

from core.models import Card


class CardSerializer(serializers.ModelSerializer):
    """Serializer for cards."""

    class Meta:
        model = Card
        fields = ['id', 'title', 'slug', 'business_name']
        read_only_fields = ['id', 'created']


class CardDetailSerializer(CardSerializer):
    """Serializer for card detail view."""

    class Meta(CardSerializer.Meta):
        fields = CardSerializer.Meta.fields + [
            'description', 'points_needed', 'created', 'updated', 'active']
