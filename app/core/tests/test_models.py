'''     Test for Models     '''

from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models

from unittest.mock import patch
from core.management.commands import creating


def create_user(**params):
    """Create and return a new user"""
    user = get_user_model().objects.create_user(
            email='testcreateuser@example.com',
            password='test123',
        )
    return user


def create_staff(**params):
    """Create and return a new user"""
    user = get_user_model().objects.create_user(
            email='test_super@example.com',
            password='test123',
            is_staff=True,
        )
    return user


def create_company(user, **params):
    """Create abd return a sample company."""
    user = get_user_model().objects.create_user(
        email='testcreatecompany@example.com',
        password='test123',
    )
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


def create_shopper():
    """Create and return shopper"""
    email = 'testcreateshopper@example.com'
    user = create_user(email=email)
    shopper = models.Shopper.objects.create(
            user=user,
            first_name="Sample First Name",
            last_name="Sample Last Name",
            address="Sample Addres",
            city="Sample City",
            post_code="N146HB"
        )

    return shopper


def create_card():
    """Create and return card."""
    user = get_user_model().objects.create_user(
            email='testcreatcard@example.com',
            password='testpass123',
            is_staff=True,
        )
    company = create_company(user=user)
    card = models.Card.objects.create(
            company=company,
            title="Costa Southgate",
            points_needed=10,
            description="Every 10 coffees you get one for free",
        )

    return card


class ModelTests(TestCase):
    '''Test models.'''

    def test_create_user_email_successful(self):
        '''Test creating a user with an email is successful.'''
        email = 'testuser@example.com'
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
        user = get_user_model().objects.create_user(
            email='testsuperuser@example.com',
            password='test123',
            is_staff=True
        )

        # self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_company(self):
        '''Test creating a company is sucessful.'''
        user = get_user_model().objects.create_user(
            email='testcompany@example.com',
            password='testpass123',
            is_staff=True
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
        email = 'test_create_card@example.com',
        user = create_staff(email=email)
        company = create_company(user=user)
        card = models.Card.objects.create(
            company=company,
            title="Costa Southgate",
            points_needed=10,
            description="Every 10 coffees you get one for free",
        )

        self.assertEqual(str(card), card.title)

    def test_create_shopper(self):
        '''Test creating a shooper is sucessful.'''
        user = get_user_model().objects.create_user(
            email='testcreateshopper@example.com',
            password='test123',
        )
        shooper = models.Shopper.objects.create(
            user=user,
            first_name="Sample First Name",
            last_name="Sample Last Name",
            address="Sample Addres",
            city="Sample City",
            post_code="N146HB"
        )

        self.assertEqual(
            str(shooper), f'{shooper.first_name} {shooper.last_name}')

    def test_create_my_cards(self):
        """Test creating a MyCards is successful. """
        card = create_card()
        shopper = create_shopper()

        mycards = models.MyCards.objects.create(
            shopper=shopper,
            card=card,
            points=1,
        )

        self.assertEqual(str(mycards.card.company.company_name),
                         mycards.card.company.company_name)

    def test_create_my_cards_history(self):
        """Test creating a MyCards is successful. """
        user = creating.create_user(email='usermycardshistory@example.com')
        shopper = creating.create_shopper(user=user)
        staff = creating.create_staff(email="mycardhistory@example.com")
        company = creating.create_company(user=staff)
        card = creating.create_card(company=company)

        mycards = models.MyCards.objects.create(
            shopper=shopper,
            card=card,
            points=1,
        )

        self.assertEqual(str(mycards.card.company.company_name),
                         mycards.card.company.company_name)

    def test_create_Receipt(self):
        """Test creating a MyCards is successful. """
        staff = creating.create_staff(email="receipt@example.com")
        company = creating.create_company(user=staff)
        card = creating.create_card(company=company)
        user = creating.create_user(email='userreceipt@example.com')
        shopper = creating.create_shopper(user=user)

        mycards = models.MyCards.objects.create(
            shopper=shopper,
            card=card,
            points=1,
        )

        self.assertEqual(str(mycards.card.company.company_name),
                         mycards.card.company.company_name)

@patch('core.models.uuid.uuid4')
def test_company_file_name_uuid(self, mock_uuid):
    """Test generating image path"""
    uuid = 'test-uuid'
    mock_uuid.return_value = uuid
    file_path = models.recipe_company_image_file_path(None, 'example.jpg')

    self.assetEqual(file_path, f'uploads/company/{uuid}.jpg')