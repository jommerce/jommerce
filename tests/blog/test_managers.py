from django.test import TestCase
from django.utils import timezone
from djplus.auth.models import User
from djplus.blog.models import Post


class PublishedManagerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(email="test@example.com", password="123456")

    def test_published_posts(self):
        Post.objects.create(title="What is Django?", slug="what-is-django", author=self.user)
        Post.objects.create(title="What is Python?", slug="what-is-python", author=self.user,
                            publication_date=timezone.now()+timezone.timedelta(seconds=1))
        post = Post.objects.create(title="What is Djplus?", slug="what-is-djplus", author=self.user,
                                   publication_date=timezone.now() - timezone.timedelta(seconds=1))
        self.assertEqual(list(Post.published.all()), [post])
