from django.test import TestCase, override_settings
from django.urls import reverse, NoReverseMatch


@override_settings(ROOT_URLCONF="djplus.blog.urls")
class UrlPatternsTests(TestCase):
    def assertReverse(self, url, name, args=[], kwargs={}):
        try:
            self.assertEqual(url, reverse(name, args=args, kwargs=kwargs))
        except NoReverseMatch:
            self.fail(f"Reversal of url named '{name}' failed with NoReverseMatch")

    def test_reverse_index_name(self):
        self.assertReverse("/", "index")
