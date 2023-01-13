from django.test import TestCase
from django.contrib.auth import get_user_model


class TestCoreModels(TestCase):
    """Test core models"""

    def test_create_user_with_email_is_successful(self):
        email = "test@example.com"
        password = "1341235"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))