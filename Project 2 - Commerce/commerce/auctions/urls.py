from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add_listing, name="add_listing"),
    path("listing/<str:listing_id>", views.view_listing, name="view_listing"),
    path("listing/<str:listing_id>/add", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.view_watchlist, name='view_watchlist'),
    path('catgories', views.browse_categories, name='categories'),
    path('categories/<str:category>', views.view_category, name='view_category'),
    path("listing/<str:listing_id>/remove", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("listing/<str:listing_id>/bid", views.place_bid, name="place_bid")
]
