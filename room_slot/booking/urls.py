from django.urls import path
from . import views
urlpatterns=[
    path('',views.index,name='index'),
    path('contact-us',views.contact,name='contact-us'),
    path('login',views.user_login,name='user_login'),
    path('signup',views.user_signup,name='user_signup'),
    path('book_hotel',views.book_hotel,name='book_hotel'),
    path('book/<str:id>',views.book,name='book'),
    path('book_service/<str:id>',views.book_service,name='book_service'),
    path('book_now/<str:id>',views.book_now,name='book_now')
    ]