from django.shortcuts import render, redirect
from management.models import staff_user, room_details, payments, booking, booking_history
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.
def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            staff = staff_user.objects.get(email=email)
        except:
            messages.info(request, "Password Invalid")
            return redirect('management')
        
        if staff:
            if(password == staff.password):
                flag=True
            else:
                flag=False
            
            if flag:
                messages.info(request, "Successful")
                request.session['staff'] = staff.id
                request.session['staff_name'] = staff.name
                return redirect('dashboard')
            else:
                messages.info(request, "Password  Invalid")
                return redirect('management')
        else:
            messages.info(request, "Email or Password Invalid")
            return redirect('index')
        
    return render(request, 'management/management.html')


def staff_logout(request):
    request.session.clear()
    messages.info(request, "Log Out Successful")
    return redirect('management')

def dashboard(request):
    
    return render(request, 'management/dashboard.html')

        

def add_rooms(request):
    if request.method == 'POST':
        room_no = request.POST['room_no']
        room_type = request.POST['room_type']
        is_booked = request.POST['is_booked']
        checkInDate = request.POST['checkInDate']
        if not checkInDate:
            checkInDate = None
        checkOutDate = request.POST['checkOutDate']
        if not checkOutDate:
            checkOutDate = None
        price = request.POST['price']

        
        if room_details.objects.filter(room_no = room_no).exists():
            messages.info(request, 'Room No. Alerady Exist')
            return redirect('add_rooms')
        else:
            room = room_details(room_no = room_no, room_type = room_type, is_booked = is_booked,checkInDate = checkInDate, checkOutDate = checkOutDate, price = price)
            room.save()
            messages.info(request, 'Room Added Successfully')
    else:

        return render(request, 'management/add_rooms.html')

    
    return render(request, 'management/add_rooms.html')
    
def see_rooms(request):
    if request.method == 'POST':
        room_no = request.POST.get('room_no')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        book_id = request.POST.get('book_id')

        checkin = datetime.strptime(checkin, '%B %d, %Y').date()
        checkout = datetime.strptime(checkout, '%B %d, %Y').date()
    
        book = booking.objects.get(id = book_id)

        print(book.id)

        print(checkin)
        if room_no is not None:
            room = room_details.objects.get(room_no  = room_no)
            room.is_booked = 'Yes'
            room.checkInDate = checkin
            room.checkOutDate = checkout
            room.book_id = book_id
            if room.book_id is not None:
                room.save()
            else:
                messages.info(request, "Room is Already Checked Out")
                return render(request, 'management/see_rooms.html')

            book_hist = booking_history(book_id = book.id, cust_name = book.cust_name, cust_phone = book.cust_phone, cust_email = book.cust_email, cust_idproof = book.cust_idproof, room_no = book.room_no, room_type = book.room_type, checkin = book.checkin, checkout = book.checkout, is_booked = 'Yes',price = book.price, payment_status = book.payment_status, order_id = book.order_id, date = datetime.today())
            book_hist.save()
            book.delete()

            messages.info(request, 'Successfully Checked In')
            return render(request, 'management/see_rooms.html', {'book_id': book_id})
        else:
            messages.info(request, 'There is some problems')
            return render('cust_bookings' )
    data = room_details.objects.filter()
    return render( request,'management/see_rooms.html', {'data': data })

def update_room(request):
    if request.method == 'GET':
        room_no = request.GET.get('room_no')
        room_type = request.GET.get('room_type')
        is_booked = request.GET.get('is_booked')
        checkInDate = request.GET.get('checkInDate')
        checkOutDate = request.GET.get('checkOutDate')
        price = request.GET.get('price')


        if room_no is not None:
            if room_details.objects.filter(room_no = room_no).exists():
                room = room_details.objects.get(room_no = room_no)
                room.room_type = room_type
                room.is_booked = is_booked
                room.checkInDate = checkInDate
                if not room.checkInDate:
                    room.checkInDate = None
                room.checkOutDate = checkOutDate
                if not room.checkOutDate:
                    room.checkOutDate = None
                room.price = price
                room.save()

                messages.info(request, "Room Updated Sucessfully")
                return render(request, 'management/update_room.html')    
            else:
                messages.info(request, "Room Doesn't Exist")
            return render(request, 'management/update_room.html')

        else:
            return render(request, 'management/update_room.html')
    else:

        return render(request, 'management/update_room.html')
        

    return render(request, 'management/update_room.html')
    
def cust_bookings(request):
    book = booking.objects.all()
    
    return render(request, 'management/cust_bookings.html', {'book': book})

def book_history(request):
    book = booking_history.objects.all()
    
    if request.method == 'POST':
        
        book_id = request.POST.get('book_id')
        print(book_id)
        if book_id is not None:
            try:
                room = room_details.objects.get(book_id = book_id)
                room.is_booked = 'No'
                room.checkInDate = None
                room.checkOutDate = None
                room.book_id = None
            
                room.save()
                
                checked_id = booking_history.objects.get(book_id = book_id)
                checked_id.checked_out = 'Yes'
                checked_id.save()
                
                messages.info(request, 'Checked Out Successfully')
                return render(request, 'management/see_rooms.html')
            except ValueError:
                messages.info(request, "Room is Already Checked Out")
                
           

            
        else:
            messages.info(request, "Room is Already Checked Out")
            return render(request, 'management/see_rooms.html')
    
    return render(request, 'management/booking_history.html', {'book': book})

def payment(request):
    pay = payments.objects.all()
    return render(request, 'management/payments.html', {'pay': pay})