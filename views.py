from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from .models import Entry

"""
    authentication scenario draft 1
    1. user opens homepage (blog/index.html)
        if user is already logged in:
        true: homepage has "dashboard" and "logout" links
        false: homepage has "login" link

    2. user clicks on login link
    3. system opens login page where login form is presented to the user

    4. user enters login info and clicks submit
        if system verified these user credentials:
        true: redirect user back to the homepage where "dashboard", "logout" links will be shown
        false: redirect to login page

"""

def index(request):

    blog_list = Entry.objects.all().order_by('-created')

    context = {
        "userIsLoggedIn" : request.user.is_authenticated,
        "blog_list" : blog_list
    }

    return render(request, 'blog/index.html', context)


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'blog/dashboard.html')
    else:
        return redirect('index')


def login(request):
    return render(request, 'blog/login.html')


def login_submit(request):

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth_login(request, user)
        return redirect('index')
    else:
        return redirect('login')


def logout(request):
    auth_logout(request)
    return redirect('index')
