from django.db import models
class Member(models.Model):
    mid=models.AutoField(primary_key=True)
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    memail=models.CharField(max_length=50,unique=True)
    phone1=models.CharField(max_length=10) 
    phone2=models.CharField(max_length=10)
    password=models.CharField(max_length=5)
    levelchoice=(('B','Basic'),('S','Silver'),('G','Gold'),('P','Platinum'),)  
    level=models.CharField(max_length=1,choices=levelchoice)
    profile_pic=models.ImageField(upload_to="media", height_field=None, width_field=None, max_length=None,blank=True)
    last_visit=models.DateField(auto_now=False, auto_now_add=False,blank=True)
class Guest(models.Model):
    gid=models.AutoField(primary_key=True) 
    fname=models.CharField(max_length=50)
    lname=models.CharField(max_length=50)
    gemail=models.CharField(max_length=50)
    phone1=models.CharField(max_length=10)
    phone2=models.CharField(max_length=10)
    mid=models.ForeignKey(Member,on_delete=models.CASCADE,null=True,blank=True)

