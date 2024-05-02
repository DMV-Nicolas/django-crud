from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import TaskForm
from .models import Task


def index(req):
    return render(req, "index.html")


def humans_txt(req):
    return render(req, "humans.txt", content_type="text/plain")


def signup(req):
    if req.method == "GET":
        return render(req, "signup.html", {
            "form": UserCreationForm()
        })
    elif req.method == "POST":
        username = req.POST["username"]
        password1 = req.POST["password1"]
        password2 = req.POST["password2"]
        if (password1 != password2):
            return render(req, "signup.html", {
                "form": UserCreationForm(),
                "error": "passwords don't match"
            })
        if (len(password1) < 8):
            return render(req, "signup.html", {
                "form": UserCreationForm(),
                "error": "password length is less than 8"
            })

        user = User.objects.create_user(username=username, password=password1)
        user.save()
        login(req, user)
        return redirect("tasks")


def signin(req):
    if req.method == "GET":
        return render(req, "signin.html", {
            "form": AuthenticationForm()
        })
    elif req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req, username=username, password=password)
        if user is None:
            return render(req, "signin.html", {
                "form": AuthenticationForm(),
                "error": "username or password is incorrect"
            })

        login(req, user)
        return redirect("tasks")


@login_required
def signout(req):
    logout(req)
    return redirect("signin")


@login_required
def tasks(req):
    tasks = Task.objects.filter(user=req.user)
    return render(req, "tasks.html", {
        "tasks": tasks
    })


@login_required
def create_task(req):
    if req.method == "GET":
        return render(req, "create_task.html", {
            "form": TaskForm()
        })
    elif req.method == "POST":
        title = req.POST["title"]
        description = req.POST["description"]
        important = True if len(req.POST) == 4 else False
        user = req.user

        task = Task.objects.create(
            title=title, description=description, important=important, user=user)
        task.save()

        return redirect("tasks")


@login_required
def task_details(req, id):
    if req.method == "GET":
        task = get_object_or_404(Task, id=id, user=req.user)
        return render(req, "task_details.html", {
            "task": task,
            "edit_form": TaskForm(instance=task)
        })
    elif req.method == "POST":
        task = get_object_or_404(Task, id=id, user=req.user)
        form = TaskForm(req.POST, instance=task)
        form.save()
        return redirect("tasks")


@login_required
def complete_task(req, id):
    if req.method == "POST":
        task = get_object_or_404(Task, id=id, user=req.user)
        task.completed_at = timezone.now()
        task.save()
        return redirect("tasks")


@login_required
def incomplete_task(req, id):
    if req.method == "POST":
        task = get_object_or_404(Task, id=id, user=req.user)
        task.completed_at = None
        task.save()
        return redirect("tasks")


@login_required
def delete_task(req, id):
    if req.method == "POST":
        task = get_object_or_404(Task, id=id, user=req.user)
        task.delete()
        return redirect("tasks")
