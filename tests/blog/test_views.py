from django.test import TestCase, override_settings


@override_settings(ROOT_URLCONF="djplus.blog.urls")
class IndexViewTests(TestCase):
    def test_template_name(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "blog/index.html")

    def test_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
