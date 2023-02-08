"""Views for the mycards APIs."""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import MyCardsHistory, Shopper
from mycardshistory import serializers


class MycardsHistoryViewSet(viewsets.ModelViewSet):
    """View for manage card APIs."""

    serializer_class = serializers.MycardsHistoryDetailSerializer
    queryset = MyCardsHistory.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve Myards for authenticated user."""
        shoppers = list(Shopper.objects.all().filter(
            user=self.request.user).values_list('id'))

        return self.queryset.filter(shopper=shoppers[0]).order_by('-id')

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save()
