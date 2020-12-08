from unittest import skip

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")


def create_user(**params):
    return get_user_model().objects.create(**params)


class PublicUserApiTests(TestCase):
    """Test the user API public"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """test that creating a user works"""
        payload = dict(
            email="sample@email.com",
            password="parola17ahuiosufegcac347946",
            name="vasile")

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertNotIn("password", res.data)
        # self.assertTrue(user.check_password(payload["password"]))

    def test_user_exists(self):
        """Test that creating a user with duplicate email fails"""
        payload = dict(
            email="sample@email.com",
            password="parola17ahuiosufegcac347946",
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
            password="1234",
            name="tudor"
        )
        user_exists = get_user_model().objects.filter(
            email=email,
        ).exists()
        self.assertFalse(user_exists)
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    @skip
    def test_create_token_for_user(self):
        """Test that a token is created"""
        payload = dict(
            email="sample@email.com",
            password="parola17ahuiosufegcac347946",
            name="Test",
        )
        create_user(**payload)
        payload.pop("name")
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        payload = dict(
            email="sample@email.com",
            password="parola17ahuiosufegcac347946"
        )
        create_user(**payload)
        payload["password"] = "wrong"
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_not_existent_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = dict(
            email="sample@email.com",
            password="parola17ahuiosufegcac347946"
        )

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        payload = dict(
            email="sample@email.com",
            password="parola17ahuiosufegcac347946"
        )
        create_user(**payload)
        payload.pop("password")
        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unautharized(self):
        """Test that auth is required"""

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API request that require auth"""

    def setUp(self):
        self.user = create_user(
            email="sample@email.com",
            password="parola17ahuiosufegcac347946",
            name="Nico"
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test that profile data is returned"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            "name": self.user.name,
            "email": self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on ME url"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user profile for authed user"""
        payload = dict(
            password="parola17nouaschimbata",
            name="New Nico"
        )

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        # self.assertTrue(self.user.check_password("parola17nouaschimbata"))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
