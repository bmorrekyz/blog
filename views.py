from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

import calendar

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

def archive(request):

    # trying to get info about how many posts there were per year
    # and then count by month in each year.
    # TO DO: update query to get the by month count
    query = 'SELECT DISTINCT( \
              EXTRACT(YEAR FROM created), EXTRACT(MONTH FROM created)) as item, \
              null as id \
             FROM blog_entry'

    archive_info = [{'2018':[],'2019':[]}]
    dates = Entry.objects.raw(query)

    for date in dates:
        # ex: archive = [{'2018':['November','December'], '2019':['January']}]
        archive = date.item.strip("(").strip(")").split(",")
        year = str(archive[0])
        month = calendar.month_name[int(archive[1])]
        archive_info[0][year].append(month)

    context = {
        "userIsLoggedIn" : request.user.is_authenticated,
        "archive_info" : archive_info
    }
    return render(request, 'blog/archive/archive.html', context)

def yearly_archive(request, year):

    query = "select * from blog_entry where EXTRACT(YEAR FROM created) = " + str(year) + ";"
    yearly_posts = Entry.objects.raw(query)

    context = {
        "userIsLoggedIn" : request.user.is_authenticated,
        "year" : year,
        "posts_by_year": yearly_posts
    }

    return render(request, 'blog/archive/yearly_archive.html', context)

def monthly_archive(request, year, month):

    query = "select * from blog_entry where EXTRACT(MONTH FROM created) =  \
             EXTRACT(MONTH FROM to_date('" + month + "', 'Month')) \
             AND EXTRACT(YEAR FROM created) = " + str(year) + ";"

    posts = Entry.objects.raw(query)

    context = {
        "userIsLoggedIn" : request.user.is_authenticated,
        "month" : month,
        "year" : year,
        "posts" : posts
    }
    return render(request, 'blog/archive/monthly_archive.html',context)

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


def about(request):
    context = {
        "userIsLoggedIn" : request.user.is_authenticated
    }
    return render(request, 'blog/about.html', context)

def index(request):

    blog_list = Entry.objects.all().order_by('-created')

    context = {
        "userIsLoggedIn" : request.user.is_authenticated,
        "blog_list" : blog_list
    }

    return render(request, 'blog/index.html', context)


def dashboard(request):
    if request.user.is_authenticated:
        context = {
            "userIsLoggedIn" : request.user.is_authenticated
        }
        return render(request, 'blog/dashboard.html', context)
    else:
        return redirect('index')


def login(request):
    context = {
        "userIsLoggedIn" : request.user.is_authenticated
    }
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
