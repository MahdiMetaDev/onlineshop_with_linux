from django.test import TestCase
from django.urls import reverse


class HomePageTestCase(TestCase):

    def test_url_by_name(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_raw_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    
    def test_rendered_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")
        self.assertTemplateUsed(response, "_base.html")


class AboutUsPageTestCase(TestCase):

    def test_url_by_name(self):
        response = self.client.get(reverse("aboutus"))
        self.assertEqual(response.status_code, 200)

    def test_raw_url(self):
        response = self.client.get("/aboutus/")
        self.assertEqual(response.status_code, 200)

    def test_rendered_template(self):
        response = self.client.get(reverse("aboutus"))
        self.assertTemplateUsed(response, "pages/aboutus.html")
        self.assertTemplateUsed(response, "_base.html")

    def test_template_content(self):
        response = self.client.get(reverse("aboutus"))
        self.assertContains(response, "email")
        