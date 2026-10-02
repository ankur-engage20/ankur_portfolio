from django.urls import path

from . import api, views

app_name = "portfolio"

urlpatterns = [
    path("", views.index, name="index"),
    path("tasks/", views.tasks_page, name="tasks"),
    path("api/tasks/", api.task_list, name="api-task-list"),
    path("api/tasks/<int:pk>/", api.task_detail, name="api-task-detail"),
]
