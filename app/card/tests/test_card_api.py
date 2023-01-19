"""Test for Card APIs."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Card

from card.serializers import (
    CardSerializer,
    CardDetailSerializer,
)


CARDS_URL = reverse('card:card-list')


def detail_url(card_id):
    """Create and return a card detail URL"""
    return reverse('card:card-detail', args=[card_id])


def create_card(user, **params):
    """Create and return a sample card."""
    defaults = {
        'title': "Sample card title",
        'business_name': "Sample Business Name",
        'description': 'Get a free coffee for every 10 coffee you buy',
        'points_needed': 10,
    }
    defaults.update(params)

    card = Card.objects.create(user=user, **defaults)
    return card


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


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

    def test_retrieve_cards(self):
        """Test retrieving a list of cards."""
        create_card(user=self.user)
        create_card(user=self.user)

        res = self.client.get(CARDS_URL)

        cards = Card.objects.all().order_by('-id')
        serializer = CardSerializer(cards, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_card_list_limited_to_user(self):
        """Test list of cards is limited to authenticated user."""
        other_user = create_user(
            email='other@example.com', password='password123'
            )
        create_card(user=other_user)
        create_card(user=self.user)

        res = self.client.get(CARDS_URL)

        cards = Card.objects.filter(user=self.user)
        serializer = CardSerializer(cards, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ger_card_detail(self):
        """Test get card detail."""
        card = create_card(user=self.user)

        url = detail_url(card.id)
        res = self.client.get(url)

        serializer = CardDetailSerializer(card)
        self.assertEqual(res.data, serializer.data)

    def test_create_card(self):
        """Test creating a card"""
        payload = {
            'title': "Sample card title",
            'business_name': "Sample Business Name",
            'description': 'Get a free coffee for every 10 coffee you buy',
            'points_needed': 10,
        }
        res = self.client.post(CARDS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        card = Card.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(card, k), v)
        self.assertEqual(card.user, self.user)

    def test_partial_update(self):
        """Test partial update of a card."""
        original_business_name = "original business name"

        card = create_card(
            user=self.user,
            title="Sample card title",
            business_name=original_business_name,
        )

        payload = {'title': 'New card title'}
        url = detail_url(card.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        self.assertEqual(card.title, payload['title'])
        self.assertEqual(card.business_name, original_business_name)
        self.assertEqual(card.user, self.user)

    def test_full_update(self):
        """Test full update of card."""
        card = create_card(
            user=self.user,
            title="Sample card title",
            business_name="Sample card business name",
            description='Sample card description',
        )

        payload = {
            'title': 'New card title',
            'business_name': 'New card business name',
            'description': 'New sample card description',
            'points_needed': 5,
        }
        url = detail_url(card.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        card.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(card, k), v)
        self.assertEqual(card.user, self.user)

    def test_update_user_returns_error(self):
        """Test changin the card user results in an error."""
        new_user = create_user(email='user3@example.com', password='test123')
        card = create_card(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(card.id)
        self.client.patch(url, payload)

        card.refresh_from_db()
        self.assertEqual(card.user, self.user)

    def test_delete_card(self):
        """Test deleting a card successful"""
        card = create_card(user=self.user)

        url = detail_url(card.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Card.objects.filter(id=card.id).exists())

    def test_card_other_users_card_error(self):
        """Test trying to delete another users recipe gives error."""
        new_user = create_user(email='user3@example.com', password='test123')
        card = create_card(user=new_user)

        url = detail_url(card.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Card.objects.filter(id=card.id).exists())
