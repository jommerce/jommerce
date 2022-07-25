from django.test import TestCase, override_settings
from django.urls import reverse, NoReverseMatch


@override_settings(ROOT_URLCONF="djplus.auth.urls")
class UrlPatternsTests(TestCase):
    def assertReverse(self, url, name, args=[], kwargs={}):
        try:
            self.assertEqual(url, reverse(name, args=args, kwargs=kwargs))
        except NoReverseMatch:
            self.fail(f"Reversal of url named '{name}' failed with NoReverseMatch")

    def test_reverse_login_name(self):
        self.assertReverse("/login/", "login")

    def test_reverse_logout_name(self):
        self.assertReverse("/logout/", "logout")

    def test_reverse_signup_name(self):
        self.assertReverse("/signup/", "signup")
