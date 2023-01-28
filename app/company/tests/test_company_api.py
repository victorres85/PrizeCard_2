"""Test for Company APIs."""

import tempfile
import os

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Company

from company.serializers import CompanyDetailSerializer


COMPANY_URL = reverse('company-list')


def create_company(user, **params):
    """Create abd return a sample company."""
    defaults = {
        'company_name': 'Company Sample',
        'address': 'Addres Sample',
        'city': 'City Sample',
        'post_code': 'n146hb',
        'country': 'GB',
        'phone_number': '07518946014',
    }
    defaults.update(params)

    company = Company.objects.create(user=user, **defaults)
    return company


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_superuser(**params)


def detail_url(company_id):
    """Create and return a company detail URL"""
    return reverse('company-detail', args=[company_id])


def image_upload_url(company_id):
    """Create and return an image upload URL."""
    return reverse('company-upload-image', args=[company_id])


class PublicCardAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(COMPANY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCompanyAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        # self.user = create_user(
        #     email='user@example.com', password='password1234'
        #     )
        self.user = get_user_model().objects.create_superuser(
            'user2@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_company(self):
        """Test retrieving a list of companies."""
        create_company(user=self.user)
        create_company(user=self.user)

        res = self.client.get(COMPANY_URL)

        # companies = Company.objects.all().order_by('-id')
        # serializer = CompanySerializer(companies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        #  self.assertEqual(res.data, serializer.data)

    def test_company_list_limited_to_user(self):
        """Test list of companies is limited to authenticated user."""
        other_user = create_user(
            email='other@example.com', password='password123'
        )
        create_company(user=other_user)
        create_company(user=self.user)

        res = self.client.get(COMPANY_URL)

        # companies = Company.objects.filter(user=self.user)
        # serializer = CompanySerializer(companies, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)

    def test_ger_company_detail(self):
        """Test get company detail."""
        company = create_company(user=self.user)

        url = detail_url(company.pk)
        res = self.client.get(url)

        serializer = CompanyDetailSerializer(company)
        self.assertEqual(res.data, serializer.data)

    def test_create_company(self):
        """Test creating a company"""
        payload = {
            'company_name': 'Company Sample',
            'address': 'Addres Sample',
            'city': 'City Sample',
            'post_code': 'n146hb',
            'country': 'GB',
            'phone_number': '07518946014',
        }
        res = self.client.post(COMPANY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        company = Company.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(company, k), v)
        self.assertEqual(company.user, self.user)
        self.assertEqual(company.country.name, 'United Kingdom')
        self.assertEqual(company.phone_number.country_code, 44)

    def test_partial_update(self):
        """Test partial update of a company."""
        original_company_name = "original company name"

        company = create_company(
            user=self.user,
            company_name=original_company_name,
            address='New Sample Address'
        )

        payload = {'address': 'New company address'}
        url = detail_url(company.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        company.refresh_from_db()
        self.assertEqual(company.company_name, original_company_name)
        self.assertEqual(company.user, self.user)
        self.assertEqual(company.address, payload['address'])

    def test_full_update(self):
        """Test full update of company."""
        company = create_company(
            user=self.user,
            company_name="Sample company company name",
            address='Sample company address',
        )

        payload = {
            'company_name': 'NEW Company Sample',
            'address': 'NEW Addres Sample',
            'city': 'NEW City Sample',
            'post_code': 'n146hb',
            'country': 'BR',
            'phone_number': '00551141620947',
        }
        url = detail_url(company.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        company.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(company, k), v)
        self.assertEqual(company.user, self.user)
        self.assertEqual(company.phone_number.country_code, 55)

    def test_update_user_returns_error(self):
        """Test changing the company user results in an error."""
        new_user = create_user(email='user3@example.com', password='test123')
        company = create_company(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(company.id)
        self.client.patch(url, payload)

        company.refresh_from_db()
        self.assertEqual(company.user, self.user)

    def test_delete_company(self):
        """Test deleting a company successful"""
        company = create_company(user=self.user)

        url = detail_url(company.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Company.objects.filter(id=company.id).exists())

    def test_delete_other_users_company_error(self):
        """Test trying to delete another users recipe gives error."""
        new_user = create_user(email='user3@example.com', password='test123')
        company = create_company(user=new_user)

        url = detail_url(company.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Company.objects.filter(id=company.id).exists())


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            'user2@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)
        self.company = create_company(self.user)

    def tearDown(self):
        self.company.logo.delete()

    def test_upload_image(self):
        """Test uploading an image to a recipe."""
        url = image_upload_url(self.company.id)
        with tempfile.NamedTemporaryFile(suffix='jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='jpeg')
            image_file.seek(0)
            payload = {'logo': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.company.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('logo', res.data)
        self.assertTrue(os.path.exists(self.company.logo.path))

    def test_uploading_image_bad_request(self):
        """Test uploading invalid image"""
        url = image_upload_url(self.company.pk)
        payload = {"logo": "notanimage"}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)