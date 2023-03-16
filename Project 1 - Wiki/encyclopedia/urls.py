from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("results", views.search, name ="search"),
    path("newpage", views.new_page, name="newpage"),
    path("random", views.random_page, name="random"),
    path("edit", views.edit_page, name="edit"),
    path("<str:title>", views.display_entry, name="wiki_entry")
]
