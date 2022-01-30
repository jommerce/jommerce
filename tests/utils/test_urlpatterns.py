from django.test import TestCase, override_settings


@override_settings(ROOT_URLCONF="jommerce.utils.urlpatterns.maintenance_mode")
class MaintenanceMode(TestCase):
    def test_template(self):
        template_name = "503.html"
        self.assertTemplateUsed(self.client.get("/"), template_name)
        self.assertTemplateUsed(self.client.get("/blog/"), template_name)
        self.assertTemplateUsed(self.client.get("/blog/post/"), template_name)

    def test_status(self):
        self.assertEqual(self.client.get("/").status_code, 503)
        self.assertEqual(self.client.get("/blog/").status_code, 503)
        self.assertEqual(self.client.get("/blog/post/").status_code, 503)


@override_settings(ROOT_URLCONF="jommerce.utils.urlpatterns.coming_soon_mode")
class ComingSoonMode(TestCase):
    def test_template(self):
        template_name = "coming-soon.html"
        self.assertTemplateUsed(self.client.get("/"), template_name)
        self.assertTemplateUsed(self.client.get("/blog/"), template_name)
        self.assertTemplateUsed(self.client.get("/blog/post/"), template_name)

    def test_status(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/blog/").status_code, 200)
        self.assertEqual(self.client.get("/blog/post/").status_code, 200)
