"""Serializer for company APIs."""

from rest_framework import serializers
from core.models import Company


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for companies."""
    distance = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'company_name', 'lat', 'long', 'logo', 'distance']

    def get_distance(self, company):
        """Return context"""
        return self.context['distances'][company.pk]


class CompanyDetailSerializer(CompanySerializer):
    """Serializer for card detail view."""

    class Meta:
        model = Company
        fields = ['id', 'company_name', 'lat', 'long', 'logo',
                  'address', 'address2', 'city', 'region',
                  'post_code', 'country', 'phone_number', 'active'
                  ]
