from django.test import TestCase
from django.contrib.auth import get_user_model
from faker import Faker, providers

fake = Faker()
fake.add_provider(providers.internet)
fake.add_provider(providers.misc)


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
