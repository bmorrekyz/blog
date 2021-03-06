from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login_submit', views.login_submit, name='login_submit'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('logout', views.logout, name='logout'),
    path('about', views.about, name='about'),
    path('archive', views.archive, name='archive'),

    path('entry/<slug:slug>', views.entry, name="entry"),
]
