from unittest.mock import patch

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

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name="Lamb"
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title="Prajitura",
            time_minutes=5,
            price=5.0

        )

        self.assertEqual(str(recipe), recipe.title)

    @patch("uuid.uud4")
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that the image is stored correctly"""
        uuid = "test-uuid"
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, "myimage.jpg")
        exp_path = f"uploads/recipe/{uuid}.jpg"
        self.assertEqual(file_path, exp_path)
