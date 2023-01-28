"""Serializers for card APIs"""

from rest_framework import serializers

from core.models import Card


class CardSerializer(serializers.ModelSerializer):
    """Serializer for cards."""

    class Meta:
        model = Card
        fields = ['id', 'company', 'title', 'description', 'points_needed']
        read_only_fields = ['id', 'created']


class CardDetailSerializer(CardSerializer):
    """Serializer for card detail view."""

    class Meta(CardSerializer.Meta):
        fields = CardSerializer.Meta.fields + [
            'created', 'updated', 'active']
