from django.test import TestCase
from django.contrib.auth import get_user_model
from faker import Faker, providers

from core import models

fake = Faker()
fake.add_provider(providers.internet)
fake.add_provider(providers.misc)


def sample_user(email=fake.email(), password=fake.password()):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test createing a new user with a successful email"""

        email = fake.email()
        password = fake.password(length=10)
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Tests that a new email for a new user is normalized"""

        email = fake.user_name()+"@"+(fake.free_email_domain().upper())
        user = get_user_model().objects.create_user(email, fake.password())

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Tests creating user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, fake.password())

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            fake.email(),
            fake.password()
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
