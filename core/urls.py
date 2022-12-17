from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
]
