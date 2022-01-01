from django.test import TestCase, override_settings
from jommerce.urls import coming_soon_urlpatterns

urlpatterns = coming_soon_urlpatterns


@override_settings(ROOT_URLCONF=__name__)
class ComingSoonModeTests(TestCase):
    def test_admin(self):
        response = self.client.get("/admin/")
        self.assertNotEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, "coming-soon.html")

    def test_template(self):
        template_name = "coming-soon.html"
        self.assertTemplateUsed(self.client.get("/"), template_name)
        self.assertTemplateUsed(self.client.get("/blog/"), template_name)
        self.assertTemplateUsed(self.client.get("/blog/post/"), template_name)

    def test_status(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/blog/").status_code, 200)
        self.assertEqual(self.client.get("/blog/post/").status_code, 200)
