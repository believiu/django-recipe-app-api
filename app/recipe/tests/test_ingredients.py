from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse("recipe:ingredient-list")


class PublicIngredientsApiTests(TestCase):
    """Test public ingredients"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login required for retrieving ingredients"""

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "sample_user2901@gmail.com",
            "parola17pas"
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving ingredients"""
        Ingredient.objects.create(user=self.user, name="Vegan")
        Ingredient.objects.create(user=self.user, name="Dessert")

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients returned are for the authed user"""

        user2 = get_user_model().objects.create_user(
            "other@user.com",
            "testparols12"
        )

        Ingredient.objects.create(user=user2, name="Meat")
        ingredient = Ingredient.objects.create(user=self.user, name="Icecream")

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], ingredient.name)

    def test_create_ingredient_successful(self, ingredient_name="New"):
        """Test creating a new ingredient"""
        exists = Ingredient.objects.filter(
            user=self.user,
            name=ingredient_name
        ).exists()

        self.assertFalse(exists)

        payload = {"name": ingredient_name}
        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=ingredient_name
        ).exists()

        self.assertTrue(exists)

    def test_create_ingredient_failure(self, ingredient_name=""):
        """Test creating a ingredient with invalid name fails"""
        payload = {"name": ingredient_name}
        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
