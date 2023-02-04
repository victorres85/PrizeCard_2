"""Test for MyCards APIs."""
from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import MyCards

from core.management.commands import creating

import datetime


def mycards_url(shopper_pk):
    """create and return mycards url"""
    return reverse('mycards-list', args=[shopper_pk])


def detail_url(shopper_id, mycards_id):
    """create and return mycards detailed URL."""
    return reverse('mycards-detail', args=[shopper_id, mycards_id])


class PublicCardAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(mycards_url(1))

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

    def test_create_mycards(self):
        """Test creating a mycards"""

        content = f'''
             Costa
             {datetime.datetime.now() - datetime.timedelta(hours=1)}
             Total  £2.00
             '''

        url = mycards_url(self.shopper.pk)

        image_file = creating.create_image(content=content, name='teste2.jpg')

        payload = {
            'image': image_file,
            'shopper': self.shopper.pk,
            'card': self.card.pk,
        }

        res = self.client.post(url, payload, format='multipart')


        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        print(res.data)
        mycards = MyCards.objects.get(id=res.data['id'])
        self.assertEqual(mycards.points, 1)
        self.assertEqual(mycards.shopper.pk, self.shopper.pk)
