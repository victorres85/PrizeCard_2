'''     Test for Models     '''

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def create_user():
    """Create and return a new user"""
    user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test123',
        )
    return user


def create_company(**params):
    """Create abd return a sample company."""
    user = create_user()
    defaults = {
        'company_name': 'Company Sample',
        'address': 'Addres Sample',
        'city': 'City Sample',
        'post_code': 'n146hb',
        'country': 'GB',
        'phone_number': '07518946014',
    }
    defaults.update(params)

    company = models.Company.objects.create(user=user, **defaults)
    return company


class ModelTests(TestCase):
    '''Test models.'''

    def test_create_user_email_successful(self):
        '''Test creating a user with an email is successful.'''
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''Test email is normalized for new users.'''
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@EXAMPLE.com', 'Test2@example.com'],
            ['TEST3@example.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        '''Test that creating a user without an email raises a ValueError'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        '''Test creating a supersuser.'''
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_company(self):
        '''Test creating a company is sucessful.'''
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        company = models.Company.objects.create(
            user=user,
            company_name='Company Sample',
            address='Addres Sample',
            city='City Sample',
            post_code='n146hb',
            country='GB',
            phone_number='07518946014',
        )

        self.assertEqual(str(company), company.company_name)

    def test_create_card(self):
        '''Test creating a card is sucessful.'''
        company = create_company()
        card = models.Card.objects.create(
            company=company,
            title="Costa Southgate",
            points_needed=10,
            description="Every 10 coffees you get one for free",
        )

        self.assertEqual(str(card), card.title)
