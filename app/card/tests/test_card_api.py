"""Test for Card APIs."""

from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Card, Company

from card.serializers import (
    CardSerializer,
    CardDetailSerializer,
)

CARDS_URL = reverse('card:card-list')


def detail_url(card_id):
    """Create and return a card detail URL"""
    return reverse('card:card-detail', args=[card_id])


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


def create_company(user, **params):
    """Create and return a new user"""
    return Company.objects.create(user, **params)


def create_card(company, **params):
    """Create and return a sample card."""
    defaults = {
        'title': "Sample card title",
        'description': 'Get a free coffee for every 10 coffee you buy',
        'points_needed': 10,
    }
    defaults.update(params)

    card = Card.objects.create(company=company, **defaults)
    return card


class PublicCardAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(CARDS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCardAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email='user@example.com', password='password1234'
            )
        self.user = get_user_model().objects.create_user(
            'user2@example.com',
            'testpass123',
        )

        self.client.force_authenticate(self.user)

        defaults = {
            'company_name': "Sample Business Name",
            'address': 'Get a free coffee for every 10 coffee you buy',
            'city': 'Sample City',
            'post_code': 'N146HB',
        }

        self.company = Company.objects.create(user=self.user, **defaults)

    def test_retrieve_cards(self):
        """Test retrieving a list of cards."""
        create_card(company=self.company)
        create_card(company=self.company)

        res = self.client.get(CARDS_URL)

        cards = Card.objects.all().order_by('-id')
        serializer = CardSerializer(cards, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_card_list_limited_to_user(self):
        """Test list of cards is limited to authenticated user."""
        user = create_user(
            email='user3@example.com', password='password1234'
            )

        defaults = {
            'company_name': "Other Business Name",
            'address': 'Other Address',
            'city': 'Other City',
            'post_code': 'N146HB',
            }

        other_company = Company.objects.create(user=user, **defaults)
        create_card(company=self.company)
        create_card(company=other_company)

        res = self.client.get(CARDS_URL)

        cards = Card.objects.filter(company=self.company)
        serializer = CardSerializer(cards, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_card_detail(self):
        """Test get card detail."""
        card = create_card(company=self.company)

        url = detail_url(card.id)
        res = self.client.get(url)

        serializer = CardDetailSerializer(card)
        self.assertEqual(res.data, serializer.data)

    def test_create_card(self):
        """Test creating a card"""

        company = {'company': self.company.pk, }
        data = {
            'title': "Sample card title",
            'description': 'Get a free coffee for every 10 coffee you buy',
            'points_needed': 10,
        }
        payload = company | data
        res = self.client.post(CARDS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        card = Card.objects.get(id=res.data['id'])
        for k, v in data.items():
            self.assertEqual(getattr(card, k), v)
        self.assertEqual(card.company.pk, self.company.pk)

    def test_partial_update(self):
        """Test partial update of a card."""
        original_points_needed = 8

        card = create_card(
            company=self.company,
            title="Sample card title",
            description='Sample Description',
            points_needed=10,
        )

        payload = {'points_needed': original_points_needed}
        url = detail_url(card.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        self.assertEqual(card.points_needed, payload['points_needed'])
        self.assertEqual(card.company.pk, self.company.pk)

    def test_full_update(self):
        """Test full update of card."""
        card = create_card(
            company=self.company,
            title="Sample card title",
            description='Sample Description',
            points_needed=10,
        )

        defaults = {
            'company_name': "Other Business Name",
            'address': 'Other Address',
            'city': 'Other City',
            'post_code': 'N146HB',
            }

        other_company = Company.objects.create(user=self.user, **defaults)

        company = {'company': other_company.pk, }

        data = {
            'title': "NEW Sample card title",
            'description': 'NEW Sample Description',
            'points_needed': 8,
        }
        payload = company | data
        url = detail_url(card.pk)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        for k, v in data.items():
            self.assertEqual(getattr(card, k), v)
        self.assertNotEqual(card.company.pk, self.company.pk)

    def test_update_company_returns_error(self):
        """Test changing the card's company results in an error."""
        defaults = {
            'company_name': "Other Business Name",
            'address': 'Other Address',
            'city': 'Other City',
            'post_code': 'N146HB',
            }

        other_company = Company.objects.create(user=self.user, **defaults)

        card = create_card(company=self.company)

        payload = {'company': other_company.pk}
        url = detail_url(card.id)
        self.client.patch(url, payload)

        card.refresh_from_db()
        self.assertNotEqual(card.company.pk, self.company.pk)

    def test_delete_card(self):
        """Test deleting a card successful"""
        card = create_card(company=self.company)

        url = detail_url(card.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Card.objects.filter(id=card.id).exists())
