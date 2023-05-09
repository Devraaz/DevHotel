from django.contrib import admin
from django.urls import path
from management import views
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='management'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('staff_logout', views.staff_logout, name='staff_logout'),
    path('add_rooms', views.add_rooms, name='add_rooms'),
    path('see_rooms', views.see_rooms, name='see_rooms'),
    path('update_room', views.update_room, name='update_room'),
    path('cust_bookings', views.cust_bookings, name='cust_bookings'),
    path('book_history', views.book_history, name='book_history'),
    path('payment', views.payment, name='payment'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)