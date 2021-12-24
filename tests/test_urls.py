from django.test import TestCase
from django.conf import settings
from unittest import skipIf

COMING_SOON_MODE = getattr(settings, "COMING_SOON_MODE", False)


class ComingSoonModeTests(TestCase):
    @skipIf(not COMING_SOON_MODE, "Because the value of 'COMING_SOON_MODE' is False")
    def test_admin_url(self):
        response = self.client.get("/admin/")
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, "coming-soon.html")

    @skipIf(not COMING_SOON_MODE, "Because the value of 'COMING_SOON_MODE' is False")
    def test_with_coming_soon_mode(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "coming-soon.html")

        response = self.client.get("/blog/post/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "coming-soon.html")

    @skipIf(COMING_SOON_MODE, "Because the value of 'COMING_SOON_MODE' is True")
    def test_without_coming_soon_mode(self):
        response = self.client.get("/")
        self.assertTemplateNotUsed(response, "coming-soon.html")
        response = self.client.get("/blog/post/")
        self.assertTemplateNotUsed(response, "coming-soon.html")
