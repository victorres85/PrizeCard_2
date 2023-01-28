"""Views for Shopper APIs."""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Shopper
from shopper.serializers import ShopperDetailSerializer, ShopperSerializer


class ShopperViewset(viewsets.ModelViewSet):
    """Viewset for manage Shopper APIs."""

    serializer_class = ShopperDetailSerializer
    queryset = Shopper.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve shopper for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serrializer class for request."""
        if self.action == 'list':
            return ShopperSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)
