from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

import calendar
import json

from .models import Entry

def login(request):
    context = { "userIsLoggedIn" : request.user.is_authenticated }
    return render(request, 'blog/login.html', context)

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

def index(request):

    query = "select \
                id, title, body, slug, markup, \
                EXTRACT(YEAR FROM created)::SMALLINT as pub_year, \
                EXTRACT(MONTH FROM created)::SMALLINT as pub_month, \
                EXTRACT(DAY FROM created)::SMALLINT as pub_day \
            from blog_entry \
            where publish=True \
            order by created desc;"

    blog_list = Entry.objects.raw(query)

    archive = {}

    for b in blog_list:
        post = {'title':b.title, 'slug':b.slug}
        if b.pub_year not in archive:
            archive[b.pub_year] = {}
            archive[b.pub_year][b.pub_month] = []
        else:
            if b.pub_month not in archive[b.pub_year]:
                archive[b.pub_year][b.pub_month] = []

        archive[b.pub_year][b.pub_month].append(post)

    context = {
        "userIsLoggedIn" : request.user.is_authenticated,
        "blog_list" : blog_list,
        "archive" : json.dumps(archive)
    }

    return render(request, 'blog/index.html', context)
    
def entry(request, slug):
    entry = Entry.objects.filter(slug=slug)[0]

    context = {
        "userIsLoggedIn" : request.user.is_authenticated,
        "entry" : {
            "title" : entry.title,
            "created" : entry.created,
            "body" : entry.body,
            "markup": entry.markup,
        }
    }
    return render(request, 'blog/entry_view.html', context)


def archive(request):
    return render(request, 'blog/archive/archive.html')

def about(request):
    context = { "userIsLoggedIn" : request.user.is_authenticated }
    return render(request, 'blog/about.html', context)

def dashboard(request):
    if request.user.is_authenticated:
        context = { "userIsLoggedIn" : request.user.is_authenticated }
        return render(request, 'blog/dashboard.html', context)
    else:
        return redirect('index')
