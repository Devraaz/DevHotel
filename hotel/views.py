from django.shortcuts import render, redirect, get_object_or_404
from management.models import room_details, payments, booking, booking_history 
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import Customer, rating
import razorpay
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.db.models import Avg




# Create your views here.
def index(request):
    cust_id = request.session.get('cust_id')
    if cust_id:
        if request.method == 'POST':
            
            cust = Customer.objects.get(id = cust_id)
            cust = Customer.objects.get(name = cust.name)
            rat = request.POST.get('rating')
            review = request.POST.get('review')

            rev = rating(cust_name= cust, review = review, rating = rat)
            rev.save()
            messages.info(request, "Submitted Successfully")
            return redirect('home')
        
    cust_ratings = rating.objects.values_list('rating')
    aggregate_rating = cust_ratings.aggregate(Avg('rating')).get('rating__avg')
    
    last_rating = rating.objects.order_by('-id')[:1]

    return render(request, 'index.html', {'aggregate_rating': aggregate_rating, 'last_rating': last_rating})

def check_rooms(request):
    rooms = room_details.objects.all() 
    if request.method == 'GET':
        checkin = datetime.strptime(request.GET.get('checkin'), '%Y-%m-%d').date()
        checkout = datetime.strptime(request.GET.get('checkout'), '%Y-%m-%d').date()
       
        available_rooms = []
        for room in rooms:
            book = booking.objects.filter(room_no = room.room_no)
            if room.is_available(checkin, checkout):
                available_rooms.append(room)
                print(room.room_no)
                for b in book:   #
                    if book.filter(room_no =room.room_no).exists():
                        if b.is_available(checkin, checkout):
                            available_rooms.append(room)
                        else:
                            if available_rooms:
                                available_rooms.pop()
                    else:
                        available_rooms.append(room)
        
        available_rooms = set(available_rooms)
        context = {'available_rooms': available_rooms, 'checkin': checkin, 'checkout': checkout}
        return render(request, 'check_rooms.html', context)
    
    
    else:
        return render(request, 'check_rooms.html')


        
def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        password1 = request.POST.get('pswd1')
        password2 = request.POST.get('pswd2')

        if password1 == password2:
            if Customer.objects.filter(email=email).exists():
                messages.info(request, "Username already Exist")
                return render(request, 'register.html')
            else:
                cust = Customer(name=name, email=email, phone_no = phone_no, password = password1)
                cust.password = make_password(cust.password)
                cust.save()
                messages.info(request, "Sucessfully Registed")
                return render(request, 'login.html')
        else:
            messages.info(request, "Password is Not Matching")
            return render(request, 'register.html')

    return render(request, 'register.html')
        
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pswd1')
        try:
            cust = Customer.objects.get(email=email)
        except:
            messages.info(request, "Email/Password Wrong")
            return redirect('login')
        if cust:
            flag = check_password(password, cust.password)
            if flag:
                request.session['cust'] = cust.name
                request.session['cust_email'] = cust.email
                request.session['cust_id'] = cust.id

                
                messages.info(request, 'Logged In Sucessfully')
                return redirect('profile')           
            else:
                messages.info(request, 'Email/Password Wrong')
                return render(request, 'login.html')
        else:
            messages.info(request, 'Email/Password Wrong')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logout(request):
    request.session.clear()
    messages.info(request, "Log Out Successful")
    return redirect('login')
    
def bookings(request):
    
    if request.method == 'POST':
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        room_id = request.POST.get('room_id')
        cust_id = request.session.get('cust_id')
        version = int(request.POST.get('version'))


            #   Storing the data in session so to use in payment_status and confirmation
        request.session['checkin'] = checkin       
        request.session['checkout'] = checkout
        request.session['room_id'] = room_id
        request.session['cust_id'] = cust_id
        
        if cust_id:
            request.session['payment_in_process'] = True
            
            checkin = datetime.strptime(checkin, '%B %d, %Y').date()
            checkout = datetime.strptime(checkout, '%B %d, %Y').date()
            num_days = (checkout - checkin).days

            room = get_object_or_404(room_details, id=room_id)
            cust = get_object_or_404(Customer, id=cust_id)
            new_price = room.price*num_days

            print(type(room.version), type(version))

            if room.version != version:
                messages.info(request, 'Room is Booked')
                return redirect('profile')
            else:
                room.version += 1
                room.save()


            client = razorpay.Client(auth = (settings.KEY, settings.SECRET))

            payment = client.order.create({'amount': new_price*100, 'currency': 'INR', 'payment_capture': 1})
            context = {'room': room,'checkin': checkin, 'checkout': checkout , "new_price": new_price, 'cust': cust, 'payment': payment}
            
            
            return render(request, 'bookings.html', context)
        else:
            messages.info(request, 'Login to continue')
            return redirect('login')

    return render(request, 'bookings.html')


def profile(request):
    if request.method == 'POST':
        if len(request.FILES) != 0:
            id_proof = request.FILES['id_proof']
            
        cust_id = request.session.get('cust_id')
        cust = Customer.objects.get(id = cust_id)
        
        cust.c_idproof = id_proof
        cust.save()


        messages.info(request, 'Successful')
        return render(request, 'index.html')
    else:
        
        cust_id = request.session.get('cust_id')
        cust = Customer.objects.get(id=cust_id)
        return render(request, 'profile.html', {'cust': cust})

        
    return render(request, 'profile.html')

@csrf_exempt
def payment_status(request):
    if not request.session.get('payment_in_process'):
        return redirect('bookings')
    client = razorpay.Client(auth = (settings.KEY, settings.SECRET))

    razorpay_payment_id = request.GET.get('razorpay_payment_id')
    razorpay_order_id = request.GET.get('razorpay_order_id')
    razorpay_signature = request.GET.get('razorpay_signature')
    payment = client.payment.fetch(razorpay_payment_id)

    payment_amount = payment['amount']/100
    payment_status = payment['status']
    if payment_status == 'captured':
        payment_status = 'Yes'
    c_email = request.session.get('cust_email')
    

    request.session['razorpay_order_id'] = razorpay_order_id

    pay = payments(razorpay_order_id = razorpay_order_id, razorpay_payment_id=razorpay_payment_id, razorpay_signature=razorpay_signature, amount=payment_amount, payment_status = payment_status, customer_email = c_email)
    try:
        pay.save()
    except IntegrityError:
        messages.info(request, ('Please don\'t reload the page'))
        return render(request, 'payment_status.html', {'error_message': 'Payment already exists.'})
    else:
        messages.info(request, "Payment Successful")
        context={'payment_id': razorpay_payment_id, 'order_id': razorpay_order_id, 'amount': payment_amount}
        return render(request, 'payment_status.html', context)
    
@csrf_exempt
def confirm_booking(request):
    if request.method == 'POST':

        # Getting the variable from session
        cust = request.session.get('cust_id')
        room = request.session.get('room_id')
        checkin = request.session.get('checkin')
        checkout = request.session.get('checkout')
        order_id = request.session.get('razorpay_order_id')

        if booking.objects.filter(order_id = order_id).exists():
            messages.info(request, 'Room is already Booked')
            return render(request, 'confirmed.html')
    

        cust = Customer.objects.get(id = cust)
        room = room_details.objects.get(id = room)
        payment = payments.objects.get(razorpay_order_id = order_id)

        checkin = datetime.strptime(checkin, '%B %d, %Y').strftime('%Y-%m-%d')
        checkout = datetime.strptime(checkout, '%B %d, %Y').strftime('%Y-%m-%d')
        print(cust.name, room.room_type, checkin, checkout)

        request.session.pop('payment_in_progress', None)
        
        book = booking(cust_name = cust.name, cust_phone = cust.phone_no, cust_email = cust.email, cust_idproof = cust.c_idproof, room_no = room.room_no, room_type = room.room_type, checkin = checkin, checkout = checkout, is_booked = 'Yes',price = payment.amount, payment_status = payment.payment_status, order_id = order_id, date = datetime.today())
        book.save()


        context = {'cust': cust, 'room': room, 'payment': payment, 'checkin': checkin, 'checkout': checkout}

        messages.info(request, "Room Booked Successful")
        
        return render(request, 'confirmed.html', {'book': book})



    return render(request, 'confirmed.html')

def past_booking(request):
    c_email = request.session.get('cust_email')
    book = booking_history.objects.filter(cust_email = c_email)

    return render(request, 'past_bookings.html', {'book': book})


def ratings(request):
    
    

    return render(request, 'index.html')