from django.test import TestCase
from djplus.blog.models import Post, Category


class PostModelTests(TestCase):
    def test_string_method(self):
        post = Post(title="What is Python?")
        self.assertEqual(str(post), "What is Python?")

    def test_get_absolute_url(self):
        post = Post(slug="what-is-python")
        self.assertEqual(post.get_absolute_url(), "/blog/what-is-python/")
        post = Post(slug="what-is-django")
        self.assertEqual(post.get_absolute_url(), "/blog/what-is-django/")


class CategoryModelTests(TestCase):
    def test_string_method(self):
        parent = Category(slug="parent", name="parent")
        child1 = Category(slug="child1", name="child1", parent=parent)
        child2 = Category(slug="child2", name="child2", parent=parent)
        grandchild = Category(slug="grandchild", name="grandchild", parent=child1)

        self.assertEqual(str(parent), "parent")
        self.assertEqual(str(child1), "parent > child1")
        self.assertEqual(str(child2), "parent > child2")
        self.assertEqual(str(grandchild), "parent > child1 > grandchild")
