from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
# Create your views here.


@login_required(login_url='signin')
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


def signin(request):
    if request.method != "POST":
        return render(request, 'signin.html')

    username = request.POST["username"]
    password = request.POST["password"]
    user = auth.authenticate(username=username, password=password)

    if user == None:
        messages.info(request, 'Invalid credentials!')
        return redirect('signin')
    auth.login(request, user)
    return redirect('/')


def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required(login_url="signin")
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method != "POST":
        return render(request, 'setting.html', {'user_profile': user_profile})

    bio = request.POST["bio"]
    location = request.POST["location"]

    if request.FILES.get('image') == None:
        image = user_profile.profileImg

    if request.FILES.get('image') != None:
        image = request.FILES.get('image')

    user_profile.bio = bio
    user_profile.location = location
    user_profile.profileImg = image
    user_profile.save()
    return redirect('settings')
