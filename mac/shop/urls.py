from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='Shop home'),
    path('about/',views.about,name='About us'),
    path('contact/',views.contact,name='Contact us'),
    path('tracker/',views.track,name='Tracking Status'),
    path('search/',views.search,name='Search'),
    path('productview/<int:id>',views.prodview,name='Product View'),
    path('checkout/',views.checkout,name='Check out'),
    path('handlerequest/',views.handlerequest,name='Handle Request'),

]
