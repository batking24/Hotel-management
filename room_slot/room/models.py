from django.db import models
class Hotel(models.Model):
    hid=models.AutoField(primary_key=True)
    hname=models.CharField(max_length=50)
    hloc=models.CharField(max_length=50)
    hotel_image=models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None,default='0.jpeg')
    ratingchoices=((1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5'),)
    rating=models.IntegerField(choices=ratingchoices)  
class Room_type(models.Model):
	rtypechoices=(('A','DELUXE'),('B','SUITE'),('C','RGWR'),)
	rtype=models.CharField(max_length=1,choices=rtypechoices)
	room_image=models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None,default='0.jpeg')
	price=models.IntegerField(default=1000) 
class Room(models.Model):
    rno=models.IntegerField()
    hid=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    rtype=models.ForeignKey(Room_type,on_delete=models.CASCADE) 
    def __str__(self):
        return "Room No: "+str(self.rno)
    class Meta(object):
        unique_together = [
            ("rno", "hid"),
        ]
class Service(models.Model):
    sid=models.AutoField(primary_key=True)
    sname=models.CharField(max_length=10,unique=True)
    simage=models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None,default='0.jpeg')
    sprice=models.IntegerField()
# Create your models here.
