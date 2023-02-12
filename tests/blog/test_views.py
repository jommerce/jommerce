from django.test import TestCase, override_settings
from django.utils import timezone
from jommerce.blog.models import Post
from jommerce.auth.models import User


@override_settings(ROOT_URLCONF="jommerce.blog.urls")
class IndexViewTests(TestCase):
    def test_template_name(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "blog/index.html")

    def test_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


@override_settings(ROOT_URLCONF="jommerce.blog.urls")
class PostDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email="test@example.com", password="123456")
        cls.post = Post.objects.create(
            title="What is Python?",
            slug="what-is-python",
            author_id=1,
            publication_date=timezone.now() - timezone.timedelta(seconds=1),
        )

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

    def test_show_only_published_post(self):
        Post.objects.create(
            title="What is Django?", slug="what-is-django", author=self.user
        )
        Post.objects.create(
            title="What is Jommerce?",
            slug="what-is-jommerce",
            author=self.user,
            publication_date=timezone.now() + timezone.timedelta(seconds=1),
        )
        response = self.client.get("/what-is-django/")
        self.assertEqual(response.status_code, 404)
        response = self.client.get("/what-is-jommerce/")
        self.assertEqual(response.status_code, 404)
