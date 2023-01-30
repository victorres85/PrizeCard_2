"""Test for Company APIs."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.management.commands import creating


def image_upload_url(company_id):
    """Create and return an image upload URL."""
    return reverse('logo-company-list', args=[company_id])


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            'user2@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)
        self.company = creating.create_company(self.user)
        self.logo = creating.create_logo(company=self.company)

    def tearDown(self):
        self.logo.delete()

    def test_uploading_image_bad_request(self):
        """Test uploading invalid image"""
        url = image_upload_url(self.company.pk)
        payload = {
            'company': self.company.pk,
            "logo": "notanimage"}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
