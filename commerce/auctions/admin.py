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
    list_display = ("bid_amount", "date", "current_bid", "contact_id", "listing_id")



class WatchlistAdmin(admin.ModelAdmin):
    list_display = ("user", "listing")


class BidAdmin(admin.ModelAdmin):
    list_display = ("bid_amount", "date", "current_bid", "winning_bid", "owner", "listing")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "comment_date", "owner", "listing")


admin.site.register(Listing, ListingAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)