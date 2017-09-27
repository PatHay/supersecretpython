from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from forms import Register, Login, Trip
from models import User, Travel_Plan
import bcrypt

def index(request):
    form = Register()
    login = Login()
    context = {
        'form': form,
        'form2': login,
    }
    return render(request, "belt_test/login.html", context)

def register(request):
    form = Register(request.POST)
    form2 = Login()
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            create = User.objects.create(name = form.cleaned_data['name'], 
            username = form.cleaned_data['username'], password = bcrypt.hashpw(form.cleaned_data['password'].encode('utf8'), bcrypt.gensalt()))
            messages.add_message(request, messages.INFO, form.cleaned_data['name'], extra_tags="name")
            return redirect('/')
    context = {
        "form": form,
        "form2": form2,
    }
    return render(request, "belt_test/login.html", context)

def login(request):
    try:
        request.session['login']
        request.session['username']
    except KeyError:
        request.session['login'] = []
        request.session['username'] = []
    form = Register()
    login = Login(request.POST)
    if request.method == 'POST':
        if login.is_valid():    
            print "valid"
            username = login.cleaned_data['username']
            request.session['login'] = User.objects.get(username=username).id
            request.session['username'] = User.objects.get(username=username).username
            print request.session['username']
            return redirect('/travels')

    context = {
        "form": form,
        "form2": login,
    }
    return render(request, "belt_test/login.html", context)

def success(request):
    context = {
        'username': request.session['username'],
        'my_trips': User.objects.get(id=request.session['login']).joint_trips.order_by("start_date")|User.objects.get(id=request.session['login']).my_trips.order_by("start_date"),
        'trips': Travel_Plan.objects.exclude(planned_by = request.session['login']).order_by("start_date"),
    }
    return render(request, "belt_test/index.html", context)

def logout(request):
    request.session.clear()
    return redirect('/')

def add(request):
    form = Trip()
    context = {
        'form': form,
    }
    return render(request, "belt_test/add.html", context)

def add_trip(request):
    form = Trip(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            Travel_Plan.objects.create(destination = form.cleaned_data['destination'], desc = form.cleaned_data['desc'], start_date = form.cleaned_data['travel_from'],end_date = form.cleaned_data['travel_to'], planned_by = User.objects.get(id = request.session['login']))
            return redirect('/travels')
    context = {
        "form": form,
    }
    return render(request, "belt_test/add.html", context)


def display(request, number):
    
    context = {
        "destination": Travel_Plan.objects.get(id=number).destination,
        "planned_by": Travel_Plan.objects.get(id=number).planned_by.name,
        "desc": Travel_Plan.objects.get(id=number).desc,
        "travel_from": Travel_Plan.objects.get(id=number).start_date,
        "travel_to": Travel_Plan.objects.get(id=number).end_date,
        "others": Travel_Plan.objects.get(id=number).joined_users.all()
    }
    return render(request,"belt_test/trip_display.html", context)

def join(request, number):
    if Travel_Plan.objects.get(id=number).joined_users.filter(username=request.session['username']):
        messages.add_message(request, messages.INFO, request.session['username'], extra_tags="name")

    else:
        trip = Travel_Plan.objects.get(id=number)
        User.objects.get(id=request.session['login']).joint_trips.add(trip)
    
    return redirect('/travels')