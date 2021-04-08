from django.shortcuts import render,redirect
from .models import Contact,Booking,Booking_detail
from room.models import Hotel,Room,Room_type,Service
from customer.models import Member
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.contrib import messages
from datetime import datetime
from django.db.models import Count 
def index(request):
    loc=Hotel.objects.values("hloc").order_by().distinct()
    hotel=[]
    for k in loc:
    	hotel.append(k["hloc"])
    print(hotel)	
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
        return render(request,'booking/bookhotel.html',{'data':hotels})    
    else:
    	return redirect('index')
def book(request,id):
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
    return render(request,'booking/book.html',{'data':data})   
def book_service(request,id):
    request.session['rtype']=id
    data=Service.objects.all()
    return render(request,"booking/bookservice.html",{'data':data})         
def book_now(request,id):
    request.session['sid']=id
    start=request.session.get('start_date',None)
    start=datetime.strptime(start, "%d/%b/%Y").date()
    end=request.session.get('end_date',None)
    end=datetime.strptime(end, "%d/%b/%Y").date()
    rtype=request.session['rtype']
    h=request.session['hotel']
    ho=Hotel.objects.get(hid=h)
    hotel=ho.hname
    data=Room_type.objects.get(rtype=rtype)
    no_of_days=end-start
    no_of_days=no_of_days.days
    print(no_of_days)
    price=0
    name="No Service Availed"
    id=int(id)
    if id!=0:
    	print(id)
    	s=Service.objects.get(sid=id)
    	name=s.sname
    	price=s.sprice
    bill=data.price*no_of_days
    bill=bill+price
    return render(request,"booking/book-now.html",{"data":data,"start":start,"end":end,"no_of_days":no_of_days,"bill":bill,"sname":name,"hotel":hotel,"sprice":price}) 	            
def user_login(request):
    if request.session.get('username',None) and request.session.get('type',None)=='member':
        return redirect('user_dashboard')
    if request.session.get('username',None) and request.session.get('type',None)=='guest':
        return redirect('guest')
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
                return render(request,'booking/index.html',{})
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

# Create your views here.
