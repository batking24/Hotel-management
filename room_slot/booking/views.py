from django.shortcuts import render,redirect
from .models import Contact,Booking,Booking_detail,Service_in_room
from room.models import Hotel,Room,Room_type,Service
from customer.models import Member,Guest
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from datetime import datetime
from django.db.models import Count 
import math
first='no'
def index(request):
    loc=Hotel.objects.values("hloc").order_by().distinct()
    hotel=[]
    if 'rooma' in request.session:
        del request.session['rooma']
       	del request.session['adulta']
       	del request.session['childa']
       	del request.session['servicea']
       	del request.session['serva']
       	print("hi1")
    if 'roomb' in request.session:
       	del request.session['roomb']
       	del request.session['adultb']
       	del request.session['childb']
       	del request.session['serviceb']
       	del request.session['servb']
    if 'roomc' in request.session:
       	del request.session['roomc']
       	del request.session['adultc']
       	del request.session['childc']
       	del request.session['servicec']
       	del request.session['servc']
    for k in loc:
    	hotel.append(k["hloc"])	
    return render(request,'booking/index.html',{"loc":hotel})
def contact(request):
    if request.method=="GET":
        return render(request,"contact/contact.html",{})
    else:
        username=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        data=Contact(name=username,email=email,message=message)
        data.save()
        return render(request,"contact/contact.html",{'message':'Thank you for contacting us.'})
def book_hotel(request):
    if request.method=="POST": 
        start_date=request.POST['start_date']
        end_date=request.POST['end_date']
        location=request.POST['location']
        rating=request.POST['rating']
        request.session['start_date']=start_date
        request.session['end_date']=end_date
        request.session['location']=location
        request.session['rating']=rating
        start_date=datetime.strptime(start_date, "%d/%b/%Y").date()
        end_date=datetime.strptime(end_date, "%d/%b/%Y").date()
        hotels=Hotel.objects.filter(hloc=location,rating__gte=rating)
        if 'rooma' in request.session:
        	del request.session['rooma']
        	del request.session['adulta']
        	del request.session['childa']
        	del request.session['servicea']
        	del request.session['serva']
        	print("hi2")
        if 'roomb' in request.session:
        	del request.session['roomb']
        	del request.session['adultb']
        	del request.session['childb']
        	del request.session['serviceb']
        	del request.session['servb']
        if 'roomc' in request.session:
        	del request.session['roomc']
        	del request.session['adultc']
        	del request.session['childc']
        	del request.session['servicec']
        	del request.session['servc']		
        return render(request,'booking/bookhotel.html',{'data':hotels})    
    else:
    	if 'rooma' in request.session:
        	del request.session['rooma']
        	del request.session['adulta']
        	del request.session['childa']
        	del request.session['servicea']
        	del request.session['serva']
        	print("hi3")
    	if 'roomb' in request.session:
        	del request.session['roomb']
        	del request.session['adultb']
        	del request.session['childb']
        	del request.session['serviceb']
        	del request.session['servb']
    	if 'roomc' in request.session:
        	del request.session['roomc']
        	del request.session['adultc']
        	del request.session['childc']
        	del request.session['servicec']
        	del request.session['servc']
    	return redirect('index')
def book(request,id):
	if request.method=="POST":
		room1=adult1=child1=serv1=0
		room2=adult2=child2=serv2=0
		room3=adult3=child3=serv3=0
		start=request.session.get('start_date',None)
		start=datetime.strptime(start, "%d/%b/%Y").date()
		end=request.session.get('end_date',None)
		end=datetime.strptime(end, "%d/%b/%Y").date()
		request.session['hotel']=id
		room_booked=Booking.objects.filter(hid=id,checkout__gte=start,checkin__lte=end)
		book_no=[]
		for b in room_booked:
			book_no.append(b.book_no)
		booked=Booking_detail.objects.filter(book_no__in=book_no).values("rtype").annotate(count=Count('rtype')).order_by()
		total=Room.objects.values("rtype").annotate(count=Count('rtype')).order_by()
		available1=0
		available2=0
		available3=0
		for x in total:
			flag=0
			for y in booked:
				if x['rtype']==y['rtype'] and x['count']>y['count']:
					flag=1
					if x['rtype']==1:
						available1=x['count']-y['count']
					elif x['rtype']==2:
						available2=x['count']-y['count']
					else:
						available3=x['count']-y['count']
			if flag==0:
				if x['rtype']==1:
					available1=x['count']
				elif x['rtype']==2:
					available2=x['count']
				else:
					available3=x['count'] 			
		service1=service2=service3=[]
		print(available1)
		print(available2)
		print(available3)
		rooma=roomb=roomc=0
		if 'rooma' in request.session:
			room1=request.session['rooma']
			adult1=request.session['adulta']	
			child1=request.session['childa']
			service1=request.session['servicea']
			serv1=request.session['serva']
		if 'roomb' in request.session:
			room2=request.session['roomb']
			adult2=request.session['adultb']	
			child2=request.session['childb']
			service2=request.session['serviceb']
			serv2=request.session['servb']
		if 'roomc' in request.session:
			room3 =request.session['roomc']	
			adult3=request.session['adultc']	
			child3=request.session['childc']
			service3=request.session['servicec']
			serv3=request.session['servc']	
		if 'rooma' in request.POST:
			rooma=request.POST['rooma']
			adult=request.POST['adulta']	
			child=request.POST['childa']
			service=request.POST['servicea']
			serv=request.POST['serva']
			room=rooma
		if 'roomb' in request.POST:
			roomb=request.POST['roomb']
			adult=request.POST['adultb']	
			child=request.POST['childb']
			service=request.POST['serviceb']
			serv=request.POST['servb']
			room=roomb
		if 'roomc' in request.POST:
			roomc=request.POST['roomc']
			adult=request.POST['adultc']	
			child=request.POST['childc']
			service=request.POST['servicec']
			serv=request.POST['servc']			
			room=roomc
		error=[]
		if not room.isnumeric():
			error.append(1)
			messages.warning(request,"Enter a valid number in adult")
		if int(room)<0 or int(adult)<0 or int(child)<0:
			error.append(1)
			messages.warning(request,"Enter a positive number")
		if int(room1)+int(rooma)>available1:
			error.append(1)
			print("hi1")
			messages.warning(request,"No more rooms available of this type")
		if int(room2)+int(roomb)>available2:
			print("hi2")
			error.append(1)
			messages.warning(request,"No more rooms available of this type")	
		if int(room3)+int(roomc)>available3:
			print("hi3")
			error.append(1)
			messages.warning(request,"No more rooms available of this type")		
		if not adult.isnumeric():
			error.append(1) 
			messages.warning(request,"Enter a valid number in adult")
		if not child.isnumeric():
			error.append(1)
			messages.warning(request,"Enter a valid number in adult")	
		if int(room)>5 or int(room1)+int(room2)+int(room3)+int(room)>5:
			error.append(1)
			messages.warning(request,"Maximum 5 rooms can be booked at a time")	
		if int(adult)>(2*int(room)):
			error.append(1)
			messages.warning(request,"Maximum 2 adults can be in a room")
		if int(child)>(2*int(room)):
			error.append(1)
			messages.warning(request,"Maximum 2 children can be in a room")
		if serv=='':
			if service != 'None':
				messages.warning(request,"Choose atleast 1 room to serve")	
		if serv !='' and int(serv)>int(room):
			error.append(1)
			messages.warning(request,"Maximum 1 extra service can be in a room")
		if serv!='' and service=='None':
			error.append(1)
			messages.warning(request,"Choose a service")
		if serv=='':
			serv=0	
		if(len(error)==0):
			if 'rooma' in request.POST:
				request.session['rooma']=int(room)+int(room1)
				request.session['adulta']=int(adult)+int(adult1)
				request.session['childa']=int(child)+int(child1)
				if service!='None':
					service1.append(service)
				request.session['servicea']=service1
				request.session['serva']=int(serv)+int(serv1)
			if 'roomb' in request.POST:
				request.session['roomb']=int(room)+int(room2)
				request.session['adultb']=int(adult)+int(adult2)
				request.session['childb']=int(child)+int(child2)
				if service!='None':
					service2.append(service)
				request.session['serviceb']=service2
				request.session['servb']=int(serv)+int(serv2)
			if 'roomc' in request.POST:
				request.session['roomc']=int(room)+int(room3)
				request.session['adultc']=int(adult)+int(adult3)
				request.session['childc']=int(child)+int(child3)
				if service!='None':
					service3.append(service)
				request.session['servicec']=service3
				request.session['servc']=int(serv)+int(serv3)
			messages.info(request,"Click Book Now to Continue or Book more Rooms")						
		return redirect('book',id)
	else:
		start=request.session.get('start_date',None)
		start=datetime.strptime(start, "%d/%b/%Y").date()
		end=request.session.get('end_date',None)
		end=datetime.strptime(end, "%d/%b/%Y").date()
		request.session['hotel']=id
		room_booked=Booking.objects.filter(hid=id,checkout__gte=start,checkin__lte=end)
		book_no=[]
		for b in room_booked:
			book_no.append(b.book_no)
		booked=Booking_detail.objects.filter(book_no__in=book_no).values("rtype").annotate(count=Count('rtype')).order_by()
		total=Room.objects.values("rtype").annotate(count=Count('rtype')).order_by()
		available=[]
		for x in total:
			flag=0
			for y in booked:
				if x['rtype']==y['rtype'] and x['count']>y['count']:
					flag=1
					if x['rtype']==1:
						available.append('A')
					elif x['rtype']==2:
						available.append('B')
					else:
						available.append('C')     
			if flag==0:
				if x['rtype']==1:
					available.append('A')
				elif x['rtype']==2:
					available.append('B')
				else:
					available.append('C')        
		data=Room_type.objects.filter(rtype__in=available)       
		ser=Service.objects.all()   
		return render(request,'booking/book.html',{'data':data,"ser":ser,"hid":id})          
def book_now(request):
	room1=request.session.get('rooma',0)
	room2=request.session.get('roomb',0)
	room3=request.session.get('roomc',0)
	adult1=request.session.get('adulta',0)
	adult2=request.session.get('adultb',0)
	adult3=request.session.get('adultc',0)
	child1=request.session.get('childa',0)
	child2=request.session.get('childb',0)
	child3=request.session.get('childc',0)
	tot=int(room1)+int(room2)+int(room3)
	service1=request.session.get('servicea',"Not availed")
	service2=request.session.get('serviceb',"Not availed")
	service3=request.session.get('servicec',"Not availed")
	serv1=request.session.get('serva',"Nil")
	serv2=request.session.get('servb',"Nil")
	serv3=request.session.get('servc',"Nil")
	start=request.session.get('start_date',None)
	start=datetime.strptime(start, "%d/%b/%Y").date()
	end=request.session.get('end_date',None)
	end=datetime.strptime(end, "%d/%b/%Y").date()
	h=request.session['hotel']
	ho=Hotel.objects.get(hid=h)
	no_of_days=end-start
	no_of_days=no_of_days.days
	price=0
	p=Room_type.objects.get(rtype='A')
	p1=p.price
	p=Room_type.objects.get(rtype='B')
	p2=p.price
	p3=0
	bill=no_of_days*((room1*p1)+(room2*p2)+(room3*p3))
	request.session['bill']=bill
	if service1 != "Not availed":
		for s in service1:
			k=Service.objects.get(sname=s)
			bill=bill+k.sprice
	if service2 != "Not availed":
		for s in service2:
			k=Service.objects.get(sname=s)
			bill=bill+k.sprice
	if service3 != "Not availed":
		for s in service3:
			k=Service.objects.get(sname=s)
			bill=bill+k.sprice		
	return render(request,"booking/book-now.html",{"tot":tot,"bill":bill,"service1":service1,"service2":service2,"service3":service3,"serv1":serv1,"serv2":serv2,"serv3":serv3,"adult2":adult2,"adult3":adult3,"child1":child1,"child2":child2,"child3":child3,"hotel":ho,"adult1":adult1,"start":start,"end":end,"room1":room1,"room2":room2,"room3":room3}) 
def book_confirm(request):
	if 'username' not in request.session:
		return redirect('user_login')
	room1=request.session.get('rooma',0)
	room2=request.session.get('roomb',0)
	room3=request.session.get('roomc',0)
	adult1=request.session.get('adulta',0)
	adult2=request.session.get('adultb',0)
	adult3=request.session.get('adultc',0)
	child1=request.session.get('childa',0)
	child2=request.session.get('childb',0)
	child3=request.session.get('childc',0)	
	service1=request.session.get('servicea',"Not availed")
	service2=request.session.get('serviceb',"Not availed")
	service3=request.session.get('servicec',"Not availed")
	serv1=request.session.get('serva',"Nil")
	serv2=request.session.get('servb',"Nil")
	serv3=request.session.get('servc',"Nil")
	start_date=request.session['start_date']
	end_date=request.session['end_date']
	username=request.session['username']
	types=request.session['type']
	amount=request.session['bill']
	start_date=datetime.strptime(start_date, "%d/%b/%Y").date()
	end_date=datetime.strptime(end_date, "%d/%b/%Y").date()
	h=request.session['hotel']
	ho=Hotel.objects.get(hid=h)
	data=""
	book_no=0
	if types=="guest":
		us=Guest.objects.get(gid=username)
		data=Booking(gid=us,plantype='A',hid=ho,checkin=start_date,checkout=end_date,cost=amount)
		data.save()
		request.session['bid']=data.book_no
		book_no=data.book_no
	else:
		user=Member.objects.get(username=username)
		customer=Guest(fname=user.fname,lname=user.lname,gemail=username,phone1=user.phone1,phone2=user.phone2,mid=user)
		customer.save()
		if user.level=='G' or user.level=='P':
			data=Booking(gid=customer.gid,plantype='C',hid=h,checkin=start_date,checkout=end_date,cost=amount)
			data.save()
			request.session['bid']=data.book_no
			book_no=data.book_no
		else:
			data=Booking(gid=customer.gid,plantype='B',hid=h,checkin=start_date,checkout=end_date,cost=amount)
			data.save()		
			request.session['bid']=data.book_no
			book_no=data.book_no		
	book=Booking.objects.get(book_no=book_no)
	temp=int(room1)
	dt=0
	for r in range(int(room1)):
		dt+=1
		temp1=int(adult1)/temp
		temp2=int(child1)/temp
		if temp1==0:
			temp1=int(adult1)
		if temp2==0:
			temp2=int(child1)	
		rt=Room_type.objects.get(rtype='A')	
		temp1=math.trunc(temp1)
		temp2=math.trunc(temp2)
		data2=Booking_detail(book_no=data,book_dtno=dt,rtype=rt,No_adults=temp1,No_children=temp2)
		data2.save()
		adult1=int(adult1)-temp1
		child1=int(child1)-temp2
	temp=int(room2)	
	for r in range(int(room2)):
		dt+=1
		temp1=int(adult2)/temp
		temp2=int(child2)/temp
		if temp1==0:
			temp1=int(adult2)
		if temp2==0:
			temp2=int(child2)
		rt=Room_type.objects.get(rtype='B')	
		temp1=math.trunc(temp1)
		temp2=math.trunc(temp2)
		data2=Booking_detail(book_no=data,book_dtno=dt,rtype=rt,No_adults=temp1,No_children=temp2)
		data2.save()
		adult2=int(adult2)-temp1
		child2=int(child2)-temp2
	temp=int(room3)	
	for r in range(int(room3)):
		dt+=1
		temp1=int(adult3)/temp
		temp2=int(child3)/temp
		if temp1==0:
			temp1=int(adult3)
		if temp2==0:
			temp2=int(child3)	
		rt=Room_type.objects.get(rtype='C')
		temp1=math.trunc(temp1)
		temp2=math.trunc(temp2)	
		data2=Booking_detail(book_no=data,book_dtno=dt,rtype=rt,No_adults=temp1,No_children=temp2)
		data2.save()
		adult3=int(adult3)-temp1
		child3=int(child3)-temp2
	del request.session['start_date']
	del request.session['end_date']
	del request.session['bill']
	del request.session['hotel']
	messages.info(request,"Room has been successfully booked")
	if types=="guest":
		return redirect('guest_dashboard')	
	return redirect('user_dashboard')		     
def user_login(request):
    if request.session.get('username',None) and request.session.get('type',None)=='member':
        return redirect('book_confirm')
    if request.session.get('username',None) and request.session.get('type',None)=='guest':
        return redirect('book_confirm')
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        if not len(username):
            messages.warning(request,"Username field is empty")
            redirect('user_login')
        elif not len(password):
            messages.warning(request,"Password field is empty")
            redirect('user_login')
        else:
            pass
        if username=="rad@gmail.com":
        	redirect("manager_dashboard")  
        if Member.objects.filter(memail=username):
            user=Member.objects.filter(memail=username)[0]
            password_hash=user.password
            res=check_password(password,password_hash)
            if res==1:
                request.session['username'] = username
                request.session['type'] = 'member'
                if first=='no':
                	first='yes'
                	return render(request,'booking/index.html',{})
                else:
                	return redirect('book_confirm')
            else:
                messages.warning(request,"Username or password is incorrect")
                redirect('user_login')
        else:
            messages.warning(request,"No, Account exist for the given Username")
            redirect('user_login')
    else:
        redirect('user_login')
    return render(request,'login/user_login.html',{})  
def user_signup(request):
    if request.session.get('username',None) and request.session.get('type',None)=='member':
        return redirect('user_dashboard')
    if request.session.get('username',None) and request.session.get('type',None)=='guest':
        return redirect('index')
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        if Member.objects.filter(memail=email):
           messages.warning(request,"Account already exist, please Login to continue")
        else:
            password=request.POST['password']
            phone1=request.POST['phone1']
            phone2=request.POST['phone2']
            profile_pic=request.FILES.get('profile_pic',None)
            error=[]
            if(len(fname)==0):
                error.append(1)
                messages.warning(request,"First name field can't be empty.")
            if(len(lname)==0):
                error.append(1)
                messages.warning(request,"Last name field can't be empty.")    
            if(len(password)<5):
                error.append(1)
                messages.warning(request,"Password field must be greater than 5 character.")
            if(len(email)==0):
                error.append(1)
                messages.warning(request,"Email field can't be empty")
            if(len(phone1)!=10):
                error.append(1)
                messages.warning(request,"Valid Phone number is a 10 digit-integer.")
            if(len(phone2)!=10):
                error.append(1)
                messages.warning(request,"Valid Phone number is a 10 digit-integer.")    
            if(len(error)==0):
                password_hash = make_password(password)
                customer=Member(fname=fname,lname=lname,memail=email,phone1=phone1,phone2=phone2,password=password,level='B',profile_pic=profile_pic,last_visit="")
                customer.save()
                messages.info(request,"Account Created Successfully, please Login to continue")
                redirect('user_signup')
            else:
                redirect('user_signup')
    else:
        redirect('user_signup')
    return render(request,'login/user_login.html',{})  
def guest_signup(request):
    if request.session.get('username',None) and request.session.get('type',None)=='member':
        return redirect('user_dashboard')
    if request.session.get('username',None) and request.session.get('type',None)=='guest':
        return redirect('index')
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        if Member.objects.filter(memail=email):
           messages.warning(request,"Account already exist, please Login to continue")
        else:
            phone1=request.POST['phone1']
            phone2=request.POST['phone2']
            profile_pic=request.FILES.get('profile_pic',None)
            error=[]
            if(len(fname)==0):
                error.append(1)
                messages.warning(request,"First name field can't be empty.")
            if(len(lname)==0):
                error.append(1)
                messages.warning(request,"Last name field can't be empty.")    
            if(len(email)==0):
                error.append(1)
                messages.warning(request,"Email field can't be empty")
            if(len(phone1)!=10):
                error.append(1)
                messages.warning(request,"Valid Phone number is a 10 digit-integer.")
            if(len(phone2)!=10):
                error.append(1)
                messages.warning(request,"Valid Phone number is a 10 digit-integer.")    
            if(len(error)==0):
                customer=Guest(fname=fname,lname=lname,gemail=email,phone1=phone1,phone2=phone2)
                customer.save()
                request.session['username'] = customer.gid
                request.session['type'] = 'guest'
                return redirect('book_confirm')
            else:
                redirect('user_signup')
    else:
        redirect('user_signup')
    return render(request,'login/guest_login.html',{})   
def user_dashboard(request):
	if request.session.get('username',None) and request.session.get('type',None)=='guest':
		return redirect('guest_dashboard')
	if request.session.get('username',None) and request.session.get('type',None)=='member':
		username=request.session['username']
		guest=Guest.objects.filter(gemail=username)
		g=[]
		for k in guest:
			g.append(k.gid)
		booking_data=Booking.objects.filter(gid__in=g).order_by('-book_no')
		counts=booking_data.filter(checkout__lt=datetime.now()).count()
		available=len(booking_data)-counts
		return render(request,"user_dash/index.html",{"data":booking_data,"count":counts,"available":available})
	else:
		return redirect("user_login")
def guest_dashboard(request):
	if request.session.get('username',None) and request.session.get('type',None)=='member':
		return redirect('user_dashboard')
	if request.session.get('username',None) and request.session.get('type',None)=='guest':
		username=request.session['username']
		guest=Guest.objects.filter(gid=username)
		g=[]
		for k in guest:
			g.append(k.gid)
		booking_data=Booking.objects.filter(gid__in=g).order_by('-book_no')
		counts=booking_data.filter(checkout__lt=datetime.now()).count()
		available=len(booking_data)-counts
		return render(request,"guest_dash/index.html",{"data":booking_data})
	else:
		return redirect("user_login")		
def cancel_room(request,id):
    data=Booking.objects.get(book_no=id)
    data.delete()
    return HttpResponse("Booking Cancelled Successfully")		
def logout(request):
    if request.session.get('username', None):
    	del request.session['username']
    	del request.session['type']
    	return render(request,"login/logout.html",{})
    else:
    	return render(request,"login/user_login.html",{})    

# Create your views here.
