"""Serializer for company APIs."""

from rest_framework import serializers
from core.models import Company, CompanyLogo
from card.serializers import CardDetailSerializer


class CompanyImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to companies."""

    class Meta:
        model = CompanyLogo
        fields = ['id', 'company', 'logo']
        read_only_fields = ['id']
        extra_kwargs = {'logo': {'required': 'True'}}


class RestrictiveImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to companies."""

    class Meta:
        model = CompanyLogo
        fields = ['logo']


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for companies."""
    card = CardDetailSerializer(many=True, read_only=True)
    image = RestrictiveImageSerializer(many=True, read_only=True)
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            'id', 'company_name', 'lat', 'long', 'distance', 'card', 'image'
            ]
        read_only_fields = ['id', 'lat', 'long', 'distance']

    def get_distance(self, company):
        """Return context"""
        if self.context['distances'][company.pk]:
            return self.context['distances'][company.pk]
        else:
            raise 'Distance could not be loaded'


class CompanyDetailSerializer(CompanySerializer):
    """Serializer for card detail view."""

    class Meta(CompanySerializer.Meta):

        fields = [
                 'id', 'company_name', 'lat', 'long',
                 'address', 'address2', 'city', 'region',
                 'post_code', 'country', 'phone_number', 'active',
                 ]
