from django.shortcuts import render,redirect, HttpResponse
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from django.contrib import messages
   
from apps.travel_buddy.models import *

def index(request):
    return render(request,"travel_buddy/index.html")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/')
    else:
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'])
        if 'success' not in request.session:
            request.session['success'] = 'Thanks for registering! Please Log in.'
        return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/')
    
    var1 = User.objects.get(email=request.POST['email'])
    if var1.password == request.POST['password']:
        request.session['name'] = var1.first_name
        request.session['loggedin'] = True
        request.session['userid'] = var1.id
        request.session['first_name'] = var1.first_name
        request.session['last_name'] = var1.last_name
        return redirect('/travels')
    else:
        if 'loggedin' not in request.session:
            request.session['loggedin'] = False
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def travels(request):
    if 'loggedin' not in request.session:
        return redirect('/')
    if request.session['loggedin'] != True:
        return redirect('/')

    context = {
        "user": User.objects.all(),
        "plans": Trip.objects.filter(join=request.session['userid']),
        "trips": Trip.objects.exclude(join=request.session['userid'])
    }
    
    return render(request, 'travel_buddy/travels.html', context)

def view(request, id):
    this_trip = Trip.objects.get(id=id)
    uploader = this_trip.uploaded_by.id
    travellers = User.objects.filter(joined=this_trip).exclude(id=uploader)
    
    context = {
        "trip": this_trip,
        "planner": this_trip.uploaded_by,
        "guests": travellers,

    }
    return render(request, 'travel_buddy/view.html', context)

def new(request):
    return render(request, 'travel_buddy/new.html')

def create(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        
        return redirect('/new')
    else:
        Trip.objects.create(
            destination=request.POST['destination'], 
            start=request.POST['start'],
            end=request.POST['end'],
            plan=request.POST['plan'], 
            uploaded_by=User.objects.get(id=request.session['userid'])   
        )

        trip = Trip.objects.last()
        trip.join.add(User.objects.get(id=request.session['userid']))

        return redirect('/travels')

def join(request, id):
    joiner = User.objects.get(id=request.session['userid'])
    trip = Trip.objects.get(id=id)

    trip.join.add(joiner)

    print(trip.join.all().values())
    return redirect('/travels')

def destroy(request, id):
    trip = Trip.objects.get(id=id)

    trip.delete()

    return redirect('/travels')

def cancel(request, id):
    trip = Trip.objects.get(id=id)
    trip.join.remove(request.session['userid'])

    return redirect('/travels')
