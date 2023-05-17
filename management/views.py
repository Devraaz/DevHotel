from django.shortcuts import render, redirect
from management.models import staff_user, room_details, payments, booking, booking_history
from django.contrib import messages
from datetime import datetime
from django.db.models import Q
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
        
    if request.method == 'GET':
        room_no  = request.GET.get('room')
        room_type  = request.GET.get('room_type')
        booked  = request.GET.get('booked')
        checkin  = request.GET.get('checkin')
        price  = request.GET.get('price')

        if room_no or room_type or booked or checkin or price:
            data = room_details.objects.all()
            if room_no:
                data = data.filter(room_no=int(room_no))

            if room_type:
                data = data.filter(room_type__icontains=room_type)

            if booked:
                data = data.filter(is_booked__icontains=booked)

            if checkin:
                data = data.filter(checkInDate=checkin)

            if price:
                data = data.filter(price__lte=price)

                 
            return render( request,'management/see_rooms.html', {'data': data })


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
    if request.method == 'GET':
        name  = request.GET.get('name')
        phone  = request.GET.get('phone')
        room_no  = request.GET.get('room')

        if name or phone or room_no:
            book = booking.objects.filter(Q(cust_name__icontains=name)
                                        & (Q(cust_phone__exact=phone) if phone else Q())
                                        & (Q(room_no__exact=room_no) if room_no else Q())
                                          )
            
            return render(request, 'management/cust_bookings.html', {'book': book})

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
    if request.method == 'GET':
        
        book_id = request.GET.get('book_id')
        name = request.GET.get('name')
        email = request.GET.get('email')
        room_no = request.GET.get('room_no')
        checkin = request.GET.get('checkin')
        order_id = request.GET.get('order_id')

        book = booking_history.objects.all()

        if name:
            book = book.filter(cust_name__icontains=name)

        if email:
            book = book.filter(cust_email__icontains=email)

        if room_no:
            book = book.filter(room_no__exact=room_no)

        if checkin:
            book = book.filter(checkin=checkin)

        if book_id:
            book = book.filter(id__exact = book_id)

        if order_id:
            book = book.filter(order_id__contains=order_id)
        
        return render(request, 'management/booking_history.html', {'book': book})




    return render(request, 'management/booking_history.html', {'book': book})

def payment(request):
    if request.method == 'GET':
        order_id  = request.GET.get('order_id')
        payment_id  = request.GET.get('payment_id')
        if order_id is not None or payment_id is not None:
            pay = payments.objects.filter(razorpay_order_id__icontains=order_id,  razorpay_payment_id__icontains=payment_id)
        


            return render(request, 'management/payments.html', {'pay': pay})        
    pay = payments.objects.all()
    return render(request, 'management/payments.html', {'pay': pay})