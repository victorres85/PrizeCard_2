"""Views for the card APIs."""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Card, Company
from card import serializers


class CardViewSet(viewsets.ModelViewSet):
    """View for manage card APIs."""

    serializer_class = serializers.CardDetailSerializer
    queryset = Card.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve cards for authenticated user."""

        companies = list(Company.objects.all().filter(user=self.request.user).values_list('id'))

        return self.queryset.filter(company=companies[0]).order_by('-id')

    def get_serializer_class(self):
        """Return the serrializer class for request."""
        if self.action == 'list':
            return serializers.CardSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save()
