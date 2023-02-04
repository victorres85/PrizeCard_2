"""Commands to create different objects"""

from core.models import Company, Card, MyCards, Shopper, CompanyLogo
from django.contrib.auth import get_user_model

from PIL import Image, ImageDraw

import tempfile


def create_user(email, password='Test123'):
    """Create and return a new user"""
    return get_user_model().objects.create_user(email=email, password=password)


def create_staff(email, password='Test123'):
    """Create and return a new user"""
    return get_user_model().objects.create_superuser(
        email=email, password=password)


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


def create_shopper(user, **params):
    """Create and return a new shopper"""
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


def create_image(content, name):
    """Create an image with a text and return it"""
    canva = Image.new('RGB', (350, 150), color='white')
    image = ImageDraw.Draw(canva)
    image.text((10, 10), content, fill=(0, 0, 0))
    image_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    canva.save(image_file, 'jpeg')
    image_file.seek(0)
    image_file.name = name

    return image_file


def create_mycards(shopper, card, image, points=1):
    """Create and return a new MyCards objects."""
    print(image)
    return MyCards.objects.create(
        shopper=shopper, card=card, image=image, points=points)


def create_logo(company, **params):
    """Create and return a new CompanyLogo"""
    return CompanyLogo.objects.create(company=company, **params)
