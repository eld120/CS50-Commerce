from django.urls import path

from . import views
from .views import IndexView, ListingCreate, ListingDelete, ListingUpdate

app_name = "auctions"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("create/", ListingCreate.as_view(), name="listing_create"),
    path("delete/<slug:slug>", ListingDelete.as_view(), name="listing_delete"),
    path("update/<slug:slug>", ListingUpdate.as_view(), name="listing_update"),
    # path("detail/<slug:slug>", ListingDetail.as_view(), name="listing_detail"),
    path("detail/<slug:slug>", views.Listing_detail, name="listing_detail"),
    path("deets/<slug:slug>", views.new_listing_detail, name="new_listing_detail"),
    # path("", views.index, name="index"),
    path("watchlist/", views.watchlistview, name="watchlist"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
]
