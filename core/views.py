from os import name
from django.http import HttpResponse
from django.shortcuts import render, HttpResponse
from . import views
# Create your views here.


def index(request):
    return render(request, 'index.html')
