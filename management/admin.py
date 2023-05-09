from django.contrib import admin
from management.models import staff_user, room_details, booking, booking_history, payments


# Register your models here.
admin.site.register(room_details)
admin.site.register(staff_user)
admin.site.register(booking)
admin.site.register(booking_history)
admin.site.register(payments)
