"""Test for MyCards APIs."""
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import MyCards, Shopper

from core.management.commands import creating

from mycards.serializers import (
    MycardsSerializer,
    MycardsDetailSerializer,
)

MYCARDS_URL = reverse('mycards-list', args=[1])


def detail_url(mycards_id):
    """create and return mycards URL."""
    return reverse('mycards-detail', args=[1, mycards_id])


class PublicCardAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(MYCARDS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCardAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = creating.create_user(email='user@example.com')
        self.user = get_user_model().objects.create_user(
            'user2@example.com',
            'testpass123',
        )

        self.client.force_authenticate(self.user)

        self.shopper = creating.create_shopper(user=self.user)
        self.staff = creating.create_staff(email="staff@example.com")
        self.company = creating.create_company(user=self.staff)
        self.card = creating.create_card(company=self.company)

        defaults = {
            'points': 0,
            'code': None,
        }

        self.mycards = MyCards.objects.create(
            shopper=self.shopper, card=self.card, **defaults)

    def test_retrieve_mycards(self):
        """Test retrieving a list of mycards."""
        creating.create_shopper(user=self.user)
        creating.create_shopper(user=self.user)

        res = self.client.get(MYCARDS_URL)

        mycards = MyCards.objects.all().order_by('-id')
        serializer = MycardsSerializer(mycards, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_mycards_list_limited_to_user(self):
        """Test list of mycards is limited to authenticated user."""
        user = creating.create_user(email='user3@example.com')

        defaults = {
            'first_name': "Other First Name",
            'last_name': "Other Last Name",
            'address': 'Other Address',
            'city': 'Other City',
            'post_code': 'N146HB',
            }

        other_shopper = Shopper.objects.create(user=user, **defaults)
        creating.create_mycards(shopper=self.shopper, card=self.card)
        creating.create_mycards(shopper=other_shopper, card=self.card)

        res = self.client.get(MYCARDS_URL)

        mycards = MyCards.objects.filter(shopper=self.shopper)
        serializer = MycardsSerializer(mycards, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(res.data, serializer.data)

    def test_get_mycards_detail(self):
        """Test get mycards detail."""
        mycards = creating.create_mycards(
            shopper=self.shopper, card=self.card)

        url = detail_url(mycards.id)
        res = self.client.get(url)

        serializer = MycardsDetailSerializer(mycards)
        self.assertEqual(res.data, serializer.data)

    def test_partial_update(self):
        """Test partial update of a mycards."""
        original_code = '8'

        mycards = creating.create_mycards(
            shopper=self.shopper,
            card=self.card,
            points=0,
            code=123,
        )

        payload = {'code': original_code}
        url = detail_url(mycards.pk)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        mycards.refresh_from_db()
        self.assertEqual(mycards.code, payload['code'])
        self.assertEqual(mycards.shopper.pk, self.shopper.pk)

    def test_full_update(self):
        """Test full update of mycards cause error."""
        mycards = creating.create_mycards(
            shopper=self.shopper,
            card=self.card,
            points=0,
            code='ABCD',
        )
        other_shopper = Shopper.objects.create(
            user=creating.create_user(email="fullupdateuser@example.com"),
            first_name='Other First Name Sample',
            last_name='Other Last Name Sample',
            address='Other Addres Sample',
            city='Other City Sample',
            post_code='cr01xx',
            country='BR',
            phone_number='00551141620947',
        )

        email = 'fullupdateofmycards@example.com'
        other_user = creating.create_staff(email)
        other_company = creating.create_company(user=other_user)
        other_card = creating.create_card(company=other_company)
        other_points = 1
        other_code = '45'

        payload = {
            'shopper': other_shopper,
            'card': other_card,
            'points': other_points,
            'code': other_code,
        }
        url = detail_url(mycards.pk)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        mycards.refresh_from_db()
        self.assertEqual(mycards.code, payload['code'])
        self.assertEqual(mycards.points, payload['points'])
        self.assertNotEqual(mycards.card.pk, payload['card'])
        self.assertNotEqual(mycards.shopper.pk, payload['shopper'])

    def test_update_shopper_returns_error(self):
        """Test changing the mycards's shopper results in an error."""
        defaults = {
            'first_name': 'First Name Sample',
            'last_name': 'Last Name Sample',
            'address': 'Addres Sample',
            'city': 'City Sample',
            'post_code': 'n146hb',
            'country': 'GB',
            'phone_number': '07518946014',
        }

        other_shopper = Shopper.objects.create(user=self.user, **defaults)

        mycards = creating.create_mycards(
            shopper=self.shopper, card=self.card)

        payload = {'shopper': other_shopper.pk}
        url = detail_url(mycards.id)
        self.client.patch(url, payload)

        mycards.refresh_from_db()
        self.assertEqual(mycards.shopper.pk, self.shopper.pk)

    def test_delete_mycards(self):
        """Test deleting a mycards successful"""
        mycards = creating.create_mycards(
            shopper=self.shopper, card=self.card)

        url = detail_url(mycards.pk)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MyCards.objects.filter(id=mycards.id).exists())
