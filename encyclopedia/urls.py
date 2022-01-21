from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:article>", views.article, name="article"),
    path("search", views.search, name="search"),
    path("newpage", views.new_entry, name="newpage"),
    path("wiki/<str:article>/edit", views.edit, name="edit"),
    path("random", views.random, name="random")
]
