from django.contrib import admin
from login.models import Customer, RoomManager
from booking.models import Contact,Rooms,Booking

# Register your models here.
admin.site.register(Customer)
admin.site.register(RoomManager)
admin.site.register(Contact)
admin.site.register(Rooms)
admin.site.register(Booking)
# we can regsiter all of them in the same place
# to automatically register:https://medium.com/hackernoon/automatically-register-all-models-in-django-admin-django-tips-481382cf75e5
