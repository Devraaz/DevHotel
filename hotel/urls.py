from django.contrib import admin
from django.urls import path
from hotel import views
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('check_rooms', views.check_rooms, name='check_rooms'),


    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('bookings', views.bookings, name='bookings'), 
    path('profile', views.profile, name='profile'),
    path('payment_status', views.payment_status, name='payment_status'),
    path('confirmed', views.confirm_booking, name='confirmed'),
    path('past_booking', views.past_booking, name='past_booking'),
    path('ratings', views.ratings, name='ratings'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)