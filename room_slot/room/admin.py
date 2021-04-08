from django.contrib import admin
from .models import Room_type,Hotel,Room,Service

admin.site.register(Room_type)
admin.site.register(Room)
admin.site.register(Service)
admin.site.register(Hotel)
# Register your models here.
