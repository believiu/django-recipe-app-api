from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="sample@user.com", password="parola17buna"):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class TestModelClass(TestCase):
    def test_create_user_with_email_success(self):
        """Test creating an user works"""
        email = "test@test.test"
        password = "test123test"
        user = get_user_model().objects.create_user(
            email=email,
            password=password

        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Tests that email is normalized"""
        email = "test@TESTTEST.TEST"
        user = get_user_model().objects.create_user(
            email=email,
            password="password"

        )

        self.assertEqual(user.email, email.lower())

    def test_user_invalid_email(self):
        """Tests passing an user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email=None, password="11")

    def test_create_superuser_success(self):
        """Tests creating a superuser works"""
        user = get_user_model().objects.create_superuser(
            email="superman", password="super")

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name="Vegan"
        )

        self.assertEqual(str(tag), tag.name)
