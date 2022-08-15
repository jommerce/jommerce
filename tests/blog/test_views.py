from django.test import TestCase, override_settings
from djplus.blog.models import Post
from djplus.auth.models import User


@override_settings(ROOT_URLCONF="djplus.blog.urls")
class IndexViewTests(TestCase):
    def test_template_name(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "blog/index.html")

    def test_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


@override_settings(ROOT_URLCONF="djplus.blog.urls")
class PostDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email="test@example.com", password="123456")
        cls.post = Post.objects.create(title="What is Python?", slug="what-is-python", author_id=1)

    def test_template_name(self):
        response = self.client.get("/what-is-python/")
        self.assertTemplateUsed(response, "blog/post.html")

    def test_status_code(self):
        response = self.client.get("/what-is-python/")
        self.assertEqual(response.status_code, 200)

    def test_context_object_name(self):
        response = self.client.get("/what-is-python/")
        self.assertIn("post", response.context)
        self.assertIsInstance(response.context["post"], Post)
