from django.test import TestCase, override_settings
from django.urls import reverse, NoReverseMatch


@override_settings(ROOT_URLCONF="dj.blog.urls")
class UrlPatternsTests(TestCase):
    def assertReverse(self, url, name, args=[], kwargs={}):
        try:
            self.assertEqual(url, reverse(name, args=args, kwargs=kwargs))
        except NoReverseMatch:
            self.fail(f"Reversal of url named '{name}' failed with NoReverseMatch")

    def test_reverse_index_name(self):
        self.assertReverse("/", "index")

    def test_reverse_post_name(self):
        self.assertReverse("/what-is-python/", "post", args=["what-is-python"])
        self.assertReverse(
            "/what-is-django/", "post", kwargs={"slug": "what-is-django"}
        )  # noqa
