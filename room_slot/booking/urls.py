from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('contact-us',views.contact,name='contact-us'),
    path('login',views.user_login,name='user_login'),
    path('signup',views.user_signup,name='user_signup'),
    path('book_hotel',views.book_hotel,name='book_hotel'),
    path('book/<str:id>',views.book,name='book'),
    path('book_now',views.book_now,name='book_now'),
    path('confirm-now-booking',views.book_confirm,name="book_confirm"),
    path('login1',views.guest_signup,name='guest_login'),
    path('cancel-room/<str:id>',views.cancel_room,name='cancel-room'),
    path('dashboard/',views.user_dashboard,name='user_dashboard'),
    path('dashboard1/',views.guest_dashboard,name='guest_dashboard'),
    ]