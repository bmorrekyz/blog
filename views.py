from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

import calendar
import json

from .models import Entry


def login_submit(request):

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth_login(request, user)

    return redirect('index')

def logout(request):
    auth_logout(request)
    return redirect('index')

def index(request):

    query = "SELECT BE.id, BE.title, BE.body, BE.slug, BE.markup, BT.tag, \
                EXTRACT(YEAR FROM BE.created)::SMALLINT as pub_year, \
                EXTRACT(MONTH FROM BE.created)::SMALLINT as pub_month, \
                EXTRACT(DAY FROM BE.created)::SMALLINT as pub_day \
            FROM blog_entry AS BE, blog_blogentrytag AS BET, blog_tag AS BT \
            WHERE \
            	BE.publish=True \
            	AND BE.id=BET.blog_entry_id \
            	AND BET.tag_id=BT.id \
            ORDER BY BE.created desc;"

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
    return render(request, 'blog/includes/archive.html')

def about(request):
    context = { "userIsLoggedIn" : request.user.is_authenticated }
    return render(request, 'blog/about.html', context)

def dashboard(request):
    if request.user.is_authenticated:
        context = { "userIsLoggedIn" : request.user.is_authenticated }
        return render(request, 'blog/dashboard.html', context)
    else:
        return redirect('index')
