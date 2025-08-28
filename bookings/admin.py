from django.contrib import admin
from .models import TravelOption, Booking, UserProfile

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ('travel_id', 'type', 'source', 'destination', 'date_time', 'price', 'available_seats')
    list_filter = ('type', 'source', 'destination', 'date_time')
    list_editable = ('date_time',)
    search_fields = ('source', 'destination')
    ordering = ('date_time',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'travel_option', 'number_of_seats', 'total_price', 'status', 'booking_date')
    list_filter = ('status', 'booking_date')
    search_fields = ('user__username', 'travel_option__source', 'travel_option__destination')
    ordering = ('-booking_date',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')
