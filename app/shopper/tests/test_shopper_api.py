"""Test for Shopper APIs"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Shopper
from shopper.serializers import ShopperSerializer, ShopperDetailSerializer

SHOPPER_URL = reverse('shopper-list')


def create_shopper(user, **params):
    defaults = {
        'first_name': 'First Name Sample',
        'last_name': 'Last Name Sample',
        'address': 'Addres Sample',
        'city': 'City Sample',
        'post_code': 'n146hb',
        'country': 'GB',
        'phone_number': '07518946014',
    }
    defaults.update(params)

    shopper = Shopper.objects.create(user=user, **defaults)

    return shopper


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


def detail_url(shopper_id):
    """Create and return a shopper detail URL"""
    return reverse('shopper-detail', args=[shopper_id])


class PublicShopperAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(SHOPPER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateShopperAPITests(TestCase):
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

    def test_retrieve_shopper(self):
        """Test retrieving a list of shoppers."""
        create_shopper(user=self.user)
        create_shopper(user=self.user)

        res = self.client.get(SHOPPER_URL)

        shoppers = Shopper.objects.all().order_by('-id')
        serializer = ShopperSerializer(shoppers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_shopper_list_limited_to_user(self):
        """Test list of shoppers is limited to authenticated user."""
        other_user = create_user(
            email='other@example.com', password='password123'
        )
        create_shopper(user=other_user)
        create_shopper(user=self.user)

        res = self.client.get(SHOPPER_URL)

        shoppers = Shopper.objects.filter(user=self.user)
        serializer = ShopperSerializer(shoppers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_shopper_detail(self):
        """Test get shopper detail."""
        shopper = create_shopper(user=self.user)

        url = detail_url(shopper.pk)
        res = self.client.get(url)

        serializer = ShopperDetailSerializer(shopper)
        self.assertEqual(res.data, serializer.data)

    def test_create_shopper(self):
        """Test creating a shopper"""
        payload = {
            'first_name': 'Shopper Sample',
            'last_name': 'Shopper Sample',
            'address': 'Addres Sample',
            'city': 'City Sample',
            'post_code': 'n146hb',
            'country': 'GB',
            'phone_number': '07518946014',
        }
        res = self.client.post(SHOPPER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        shopper = Shopper.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(shopper, k), v)
        self.assertEqual(shopper.user, self.user)
        self.assertEqual(shopper.country.name, 'United Kingdom')
        self.assertEqual(shopper.phone_number.country_code, 44)

    def test_partial_update(self):
        """Test partial update of a shopper."""
        original_first_name = "original shopper name"

        shopper = create_shopper(
            user=self.user,
            first_name=original_first_name,
            address='New Sample Address'
        )

        payload = {'address': 'New shopper address'}
        url = detail_url(shopper.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        shopper.refresh_from_db()
        self.assertEqual(shopper.first_name, original_first_name)
        self.assertEqual(shopper.user, self.user)
        self.assertEqual(shopper.address, payload['address'])

    def test_full_update(self):
        """Test full update of shopper."""
        shopper = create_shopper(
            user=self.user,
            first_name="Sample shopper shopper name",
            address='Sample shopper address',
        )

        payload = {
            'first_name': 'NEW Shopper Sample',
            'last_name': 'NEW Shopper Sample',
            'address': 'NEW Addres Sample',
            'city': 'NEW City Sample',
            'post_code': 'n146hb',
            'country': 'BR',
            'phone_number': '00551141620947',
        }
        url = detail_url(shopper.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        shopper.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(shopper, k), v)
        self.assertEqual(shopper.user, self.user)
        self.assertEqual(shopper.phone_number.country_code, 55)

    def test_update_user_returns_error(self):
        """Test changing the shopper user results in an error."""
        new_user = create_user(email='user3@example.com', password='test123')
        shopper = create_shopper(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(shopper.id)
        self.client.patch(url, payload)

        shopper.refresh_from_db()
        self.assertEqual(shopper.user, self.user)

    def test_delete_shopper(self):
        """Test deleting a shopper successful"""
        shopper = create_shopper(user=self.user)

        url = detail_url(shopper.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Shopper.objects.filter(id=shopper.id).exists())

    def test_delete_other_users_shopper_error(self):
        """Test trying to delete another users recipe gives error."""
        new_user = create_user(email='user3@example.com', password='test123')
        shopper = create_shopper(user=new_user)

        url = detail_url(shopper.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Shopper.objects.filter(id=shopper.id).exists())
