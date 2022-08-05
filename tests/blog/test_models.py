from django.test import TestCase
from djplus.blog.models import Post


class PostModelTests(TestCase):
    def test_string_method(self):
        post = Post(title="What is Python?")
        self.assertEqual(str(post), "What is Python?")
