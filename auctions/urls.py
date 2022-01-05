from django.conf.urls import url
from django.urls import path
from .views import (
    IndexView,
    ListingCreate,
    ListingDelete,
    ListingUpdate,
    Listing_detail,
)
from . import views


app_name = "auctions"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("lcr/", ListingCreate.as_view(), name="listing_create"),
    path("ldl/<slug:slug>", ListingDelete.as_view(), name="listing_delete"),
    path("lul/<slug:slug>", ListingUpdate.as_view(), name="listing_update"),
    # path("detail/<slug:slug>", ListingDetail.as_view(), name="listing_detail"),
    path("detail/<slug:slug>", views.Listing_detail, name="listing_detail"),
    path("deets/<slug:slug>", views.new_listing_detail, name="new_listing_detail"),
    # path("", views.index, name="index"),
    path("watchlist/", views.watchlistview, name="watchlist"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
]
