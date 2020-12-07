from unittest import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")


def create_user(**params):
    return get_user_model().objects.create(**params)


class PublicUserApiTests(TestCase):
    """Test the user API public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """test that creating a user works"""
        payload = dict(
            email="das.sample@email.com",
            password="pass1234",
            name="vasile")

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertNotIn("password", res.data)
        # self.assertTrue(user.check_password(payload["password"]))

    def test_user_exists(self):
        """Test that creating a user with duplicate email fails"""
        payload = dict(
            email="sam.sample@email.com",
            password="passwort",
            name="strengarul"
        )
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that creating a user with a bad password fails"""
        email = "sample@email.com"
        payload = dict(
            email=email,
            password="x",
            name="tudor"
        )

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=email,
        ).exists()
        self.assertFalse(user_exists)
