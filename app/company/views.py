"""Views for the company APIs."""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Company, CompanyLogo
from company import serializers


from geopy.distance import great_circle
import requests


class CompanyViewSet(viewsets.ModelViewSet):
    """View for manage card APIs."""

    serializer_class = serializers.CompanyDetailSerializer
    queryset = Company.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve cards for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def list(self, request, pk=None):
        """Return the serrializer class for request."""
        # Get IP info once
        ip_info = requests.get(
            'https://api64.ipify.org?format=json').json()
        ip_address = ip_info["ip"]
        response = requests.get(
            f'http://api.ipstack.com/{ip_address}?access_key='
            '8eba29fcae0bbc63c1e93b8c370e4bcf').json()
        latitude = response.get("latitude")
        longitude = response.get("longitude")

        if response['success'] is False:
            first = (51.633789, -0.125860)
            print('''
            IMPORTANT:
            usage_limit_reached
            Your monthly usage limit has been reached
            Please upgrade your Subscription Plan
            http://api.ipstack.com/
            ''')
        else:
            first = (float(latitude), float(longitude))
        # Calculate distances for all companies
        # and pass them as a context to our serializer
        companies = Company.objects.all()
        distances = {}
        for company in companies:
            second = (company.lat, company.long)
            distance = great_circle(first, second).miles
            distances[company.id] = distance

        # Sort by distance
        companies_processed = serializers.CompanySerializer(
            companies, many=True, context={'distances': distances}).data
        companies_processed.sort(key=lambda x: x['distance'])

        return Response(companies_processed, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """Create a new recipe."""
        if self.request.user.is_staff:
            serializer.save(user=self.request.user)
        else:
            raise 'only super user are allowed to create a company object'


class CompanyLogoViewSet(viewsets.ModelViewSet):
    """View for manage card APIs."""

    serializer_class = serializers.CompanyImageSerializer
    queryset = CompanyLogo.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (FormParser, MultiPartParser)

    def get_serializer_class(self):
        if self.action == 'upload-image':
            return self.serializer_class
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save()

    def post(self, request, pk=None):
        """Upload an image to company"""
        company = self.get_object()
        serializer = self.get_serializer(company, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
