from django.test import TestCase
from django.contrib.auth import get_user_model
from parameterized import parameterized

class TestUseModel(TestCase):
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

    @parameterized.expand([
        ("test1@EXAMPLE.com", "test1@example.com"),
        ("test2@Example.com", "test2@example.com"),
        ("TEST3@EXAMPLE.COM", "TEST3@example.com"),
        ("test4@example.COM", "test4@example.com"),
    ])
    def test_new_user_email_normalized(self, inputed_email, expected):
        """Test email is normalized for new users"""

        user = get_user_model().objects.create_user(inputed_email, "12345")
        self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Creating an user without an email raises a ValueError"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password="12345")

    def test_create_superuser(self):
        """Test creating a super user"""
        user = get_user_model().objects.create_superuser(
            email="test@example.com",
            password="12345"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
