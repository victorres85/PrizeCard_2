"""Views for the card APIs."""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Card
from card import serializers


class CardViewSet(viewsets.ModelViewSet):
    """View for manage card APIs."""

    serializer_class = serializers.CardDetailSerializer
    queryset = Card.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve cards for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serrializer class for request."""
        if self.action == 'list':
            return serializers.CardSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)
