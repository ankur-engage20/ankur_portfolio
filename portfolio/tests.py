import json

from django.test import TestCase, override_settings

from .models import Task


class TaskApiTests(TestCase):
    def post_json(self, url, data, method="post"):
        return getattr(self.client, method)(url, json.dumps(data), content_type="application/json")

    def test_create_and_list(self):
        response = self.post_json("/api/tasks/", {"title": "Docker seekhna", "description": "basics"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["title"], "Docker seekhna")

        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)

    def test_create_requires_title(self):
        response = self.post_json("/api/tasks/", {"title": "  "})
        self.assertEqual(response.status_code, 400)

    def test_invalid_json(self):
        response = self.client.post("/api/tasks/", "not json", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_get_update_delete(self):
        task = Task.objects.create(title="CI/CD")
        url = f"/api/tasks/{task.id}/"

        self.assertEqual(self.client.get(url).json()["title"], "CI/CD")

        response = self.post_json(url, {"done": True}, method="put")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["done"])
        self.assertEqual(response.json()["title"], "CI/CD")

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_missing_task_returns_404(self):
        self.assertEqual(self.client.get("/api/tasks/999/").status_code, 404)


class PageTests(TestCase):
    def test_pages_load(self):
        self.assertEqual(self.client.get("/").status_code, 200)
        self.assertEqual(self.client.get("/tasks/").status_code, 200)


@override_settings(CORS_ALLOW_ALL_ORIGINS=False, CORS_ALLOWED_ORIGINS=["https://web.gpslive.online"])
class CorsTests(TestCase):
    def test_allowed_origin_gets_cors_header(self):
        response = self.client.get("/api/tasks/", HTTP_ORIGIN="https://web.gpslive.online")
        self.assertEqual(response["Access-Control-Allow-Origin"], "https://web.gpslive.online")

    def test_other_origin_is_blocked(self):
        response = self.client.get("/api/tasks/", HTTP_ORIGIN="https://evil.example.com")
        self.assertNotIn("Access-Control-Allow-Origin", response)

    def test_preflight_for_json_post(self):
        response = self.client.options(
            "/api/tasks/",
            HTTP_ORIGIN="https://web.gpslive.online",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="POST",
            HTTP_ACCESS_CONTROL_REQUEST_HEADERS="content-type",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("content-type", response["Access-Control-Allow-Headers"])
