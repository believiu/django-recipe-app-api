from django.test import TestCase
from django.contrib.auth import get_user_model


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
