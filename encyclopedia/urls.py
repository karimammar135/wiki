from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry_name>", views.entry_page, name="entry_page"),
    path("/new_page", views.new_page, name="new_page"),
    path("/random", views.random, name="random"),
    path("/edit/<str:title>", views.edit, name="edit")
]
