"""
Task CRUD API — sirf Django se (koi extra package nahi).

  GET     /api/tasks/        → saare tasks ki list
  POST    /api/tasks/        → naya task banao       body: {"title": "...", "description": "..."}
  GET     /api/tasks/<id>/   → ek task
  PUT     /api/tasks/<id>/   → task update karo      body: {"title": "...", "done": true}  (jo field bhejo wahi badlega)
  DELETE  /api/tasks/<id>/   → task delete karo
"""
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Task


def _read_json(request):
    try:
        return json.loads(request.body or "{}"), None
    except json.JSONDecodeError:
        return None, JsonResponse({"error": "Invalid JSON"}, status=400)


# csrf_exempt: practice API hai, login nahi hai — isliye curl/Postman se test karna aasaan rahe.
@csrf_exempt
@require_http_methods(["GET", "POST"])
def task_list(request):
    if request.method == "GET":
        tasks = [task.to_dict() for task in Task.objects.all()]
        return JsonResponse({"count": len(tasks), "results": tasks})

    data, error = _read_json(request)
    if error:
        return error

    title = str(data.get("title", "")).strip()
    if not title:
        return JsonResponse({"error": "title zaroori hai"}, status=400)

    task = Task.objects.create(
        title=title[:200],
        description=str(data.get("description", "")).strip(),
    )
    return JsonResponse(task.to_dict(), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def task_detail(request, pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return JsonResponse({"error": "Task nahi mila"}, status=404)

    if request.method == "GET":
        return JsonResponse(task.to_dict())

    if request.method == "DELETE":
        task.delete()
        return JsonResponse({"message": f"Task {pk} delete ho gaya"})

    data, error = _read_json(request)
    if error:
        return error

    if "title" in data:
        title = str(data["title"]).strip()
        if not title:
            return JsonResponse({"error": "title khaali nahi ho sakta"}, status=400)
        task.title = title[:200]
    if "description" in data:
        task.description = str(data["description"]).strip()
    if "done" in data:
        task.done = bool(data["done"])

    task.save()
    return JsonResponse(task.to_dict())
