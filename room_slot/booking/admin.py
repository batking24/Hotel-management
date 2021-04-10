from django.contrib import admin
from .models import Contact, Booking, Booking_detail, Service_in_room

admin.site.register(Contact)
admin.site.register(Booking)
admin.site.register(Booking_detail)
admin.site.register(Service_in_room)
# Register your models here.
