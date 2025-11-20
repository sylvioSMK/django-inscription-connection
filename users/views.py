from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from .models import User

def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "users/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            try:   
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                form.add_error(None, "Utilisateur introuvable")
                return render(request, "users/login.html", {"form": form})

            if user.check_password(password):
                request.session["user_id"] = user.id
                return redirect("home")
            else:
                form.add_error(None, "Mot de passe incorrect")
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def home_view(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = User.objects.get(id=user_id)
    return render(request, "users/home.html", {"user": user})


def logout_view(request):
    return redirect("login")
