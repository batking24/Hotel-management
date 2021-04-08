from django.db import models
from customer.models import Guest
from datetime import date
from room.models import Hotel,Room,Room_type,Service
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    message=models.TextField(max_length=2000)
    def __str__(self):
        return self.name
'''
class RoomImage(models.Model):
    room=models.ForeignKey(Rooms, on_delete=models.CASCADE)
    room_image=models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None)
'''
class Booking(models.Model):
    book_no=models.AutoField(primary_key=True)
    gid=models.ForeignKey(Guest,on_delete=models.CASCADE)
    plantypechoices=(('A','A'),('B','B'),('C','C'),)
    plantype=models.CharField(max_length=1,choices=plantypechoices)
    hid=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    checkin=models.DateField(auto_now=False,auto_now_add=False)
    checkout=models.DateField(auto_now=False,auto_now_add=False)
    cost=models.IntegerField()
    def __str__(self):
        return "Booking ID: "+str(self.book_no)
    @property
    def is_past_due(self):
        return date.today()>self.checkout
class Booking_detail(models.Model):
    book_no=models.ForeignKey(Booking,on_delete=models.CASCADE)
    book_dtno=models.IntegerField()
    rno=models.ForeignKey(Room,on_delete=models.CASCADE)
    rtype=models.ForeignKey(Room_type,on_delete=models.CASCADE)
    adult=((0,'0'),(1,'1'),(2,'2'),)
    No_adults=models.IntegerField(choices=adult)
    children=((0,'0'),(1,'1'),)
    No_children=models.IntegerField(choices=children)
    class Meta(object):
        unique_together = [
            ("book_no", "book_dtno"),
        ]
class Service_in_room(models.Model):
    sid=models.ForeignKey(Service,on_delete=models.CASCADE)
    book_dtno=models.ForeignKey(Booking_detail,on_delete=models.CASCADE)
    class Meta(object):
        unique_together = [
            ("book_dtno", "sid"),
        ]        
# Create your models here.
