from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Listing, User, Bid, Comment, Watchlist


class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "image",
        "active",
        "start_price",
        "auction_start",
        "auction_end",
    )
    prepopulated_fields = {"slug": ("title",)}


class BidAdmin(admin.ModelAdmin):
    list_display = ("bid_current", "bid_max", "date", "owner", "listing")


class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "listing")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "comment_date", "owner", "listing")


admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
