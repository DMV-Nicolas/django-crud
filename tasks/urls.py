from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/create", views.create_task, name="create_task"),
    path("tasks/<int:id>", views.task_details, name="task_details"),
    path("tasks/<int:id>/complete", views.complete_task, name="complete_task"),
    path("tasks/<int:id>/incomplete",
         views.incomplete_task, name="incomplete_task"),
    path("tasks/<int:id>/delete", views.delete_task, name="delete_task"),
    path("humans.txt/", views.humans_txt),
]
