from django.test import TestCase, override_settings
from django.urls import reverse, NoReverseMatch


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class AccessUrlsByName(TestCase):
    def test_access_login_url(self):
        try:
            self.assertEqual(reverse("login"), "/login/")
        except NoReverseMatch:
            self.fail("Reversal of url named 'login' failed with NoReverseMatch")

    def test_access_logout_url(self):
        try:
            self.assertEqual(reverse("logout"), "/logout/")
        except NoReverseMatch:
            self.fail("Reversal of url named 'logout' failed with NoReverseMatch")

    def test_access_signup_url(self):
        try:
            self.assertEqual(reverse("signup"), "/signup/")
        except NoReverseMatch:
            self.fail("Reversal of url named 'signup' failed with NoReverseMatch")
