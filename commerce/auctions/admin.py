from django.contrib import admin

# Register your models here.
from .models import Listing, User, Bid, Comment

class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'image', 'active', 'start_price', 
         'auction_start', 'auction_end',  )
    prepopulated_fields = {'slug' : ('title',)}
    


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'email', 'last_name',  'cash',
     'my_bids', 'my_comments')


class BidAdmin(admin.ModelAdmin):
    list_display = ('bid_amount', 'date', 'current_bid', 'contact_id', 'listing_id')

admin.site.register(Listing, ListingAdmin)