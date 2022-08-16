from django.test import TestCase
from djplus.blog.models import Post


class PostModelTests(TestCase):
    def test_string_method(self):
        post = Post(title="What is Python?")
        self.assertEqual(str(post), "What is Python?")

    def test_get_absolute_url(self):
        post = Post(slug="what-is-python")
        self.assertEqual(post.get_absolute_url(), "/blog/what-is-python/")
        post = Post(slug="what-is-django")
        self.assertEqual(post.get_absolute_url(), "/blog/what-is-django/")
