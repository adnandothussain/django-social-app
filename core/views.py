from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Profile
# Create your views here.


def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method != "POST":
        return render(request, 'signup.html')

    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    confirmPassword = request.POST["password2"]

    if password != confirmPassword:
        messages.info(request, 'Confirm password did not matched!')
        return redirect('signup')

    if User.objects.filter(email=email).exists():
        messages.info(request, 'Email already exist!')
        return redirect('signup')

    if User.objects.filter(username=username).exists():
        messages.info(request, 'Username already exist!')
        return redirect('signup')

    user = User.objects.create_user(
        username=username, email=email, password=password)
    user.save()

    # Login the user and redirect to the settings page

    # create a profile object for new user
    user_model = User.objects.get(username=username)
    profile_model = Profile.objects.create(
        user=user_model, id_user=user_model.id)

    profile_model.save()
    return redirect('login')


def login(request):
    return render(request, 'signin.html')
