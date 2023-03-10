"""Databade models."""

import uuid
import os

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    )
from app import settings

from PIL import Image
import re
import pytesseract

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from geopy.geocoders import Nominatim


def company_image_file_path(instance, filename):
    """Generate file path for new company image."""

    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'company', filename)


def mycards_image_file_path(instance, filename):
    """Generate file path for new mycards image."""

    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'mycards', filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_field):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Company(models.Model):
    """Company object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    company_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50)
    region = models.CharField(max_length=50, blank=True)
    post_code = models.CharField(max_length=10)
    country = CountryField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True)
    lat = models.CharField(max_length=20, null=True, blank=True)
    long = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        geolocator = Nominatim(user_agent="home")
        location = geolocator.geocode(self.post_code)
        self.lat = location.latitude
        self.long = location.longitude

        return super().save(*args, **kwargs)


class CompanyLogo(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE)
    logo = models.ImageField(
        upload_to=company_image_file_path, null=True, blank=True)


class Card(models.Model):
    """Card object."""
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    points_needed = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Shopper(models.Model):
    """Shopper Object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=150)
    address = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)
    post_code = models.CharField(max_length=10)
    country = CountryField(null=True, blank=True)
    phone_number = PhoneNumberField(null=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
    active = models.BooleanField(default=True)
    lat = models.CharField(max_length=20, null=True, blank=True)
    long = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        geolocator = Nominatim(user_agent="home")
        location = geolocator.geocode(self.post_code)
        self.lat = location.latitude
        self.long = location.longitude

        return super().save(*args, **kwargs)


class MyCards(models.Model):
    """My_Cards Object"""
    shopper = models.ForeignKey(
        Shopper, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='mycards', null=True)
    points = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.card.company.company_name

    def save(self, *args, **kwargs):
        """Create Receipt object"""
        if self.image:
            img_txt = pytesseract.image_to_string(Image.open(self.image))
            date_pattern = r"\d{2}[/-]\d{2}[/-]\d{4}"
            hour_pattern = r"\d{2}[:]\d{2}[:]\d{2}"
            date = re.findall(date_pattern, img_txt)
            hour = re.findall(hour_pattern, img_txt)
            company = self.card.company.company_name
            key = company + str(date) + str(hour)
            Receipt.objects.create(
                receipt_key=key,
            )
        return super().save(*args, **kwargs)


class MyCardsHistory(models.Model):
    """My Cards History Object"""
    company = models.ForeignKey(
        Company,
        on_delete=models.DO_NOTHING,
        blank=True, null=True
        )
    shopper = models.ForeignKey(Shopper, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True)
    code = models.CharField(max_length=6, blank=True)
    finalized = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.shopper.user.email} - {self.card.company.company_name}"


class Receipt(models.Model):
    """Receipt Object"""
    receipt_key = models.CharField(max_length=300, unique=True)
