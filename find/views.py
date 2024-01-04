from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Mechanic
from . import forms
import requests
import json
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    lat2=float(lat2)
    lon2=float(lon2)
    # Earth's radius in kilometers
    earth_radius = 6371

    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat/2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Calculate the distance
    distance = earth_radius * c
    if distance<10:
        distance+=2
    elif distance<30:
        distance+=5
    elif distance<70:
        distance+=7
    elif distance<100:
        distance+=15

    return distance

def find_mech(request):
    mechanic=dict()
    mech=list()
    lat,lon=0,0
    if request.method=='POST':
        user_ip = request.META.get('REMOTE_ADDR')
        # Getting latitude and longitude of the ip
        response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=b647ac5556484dfc8644a81135ff22a9&"+user_ip)
        res=json.loads(response.content)
        lat = res['latitude']
        lon = res['longitude']

        # sorting mechanics based on distance
        mechanic=Mechanic.objects.all()
        for i in mechanic:
            x=Mechanic.objects.get(shop_name=i)
            mech.append(list((x,calculate_distance(lat,lon,float(x.lattitude),float(x.longitude)))))
        #     print(x.name)
        #     print()
        # print(mechanic,type(mechanic))
        mech=sorted(mech,key= lambda x:x[1])
    return render(request,'find_mech.html',{'mechanics':mech})


def index(request):
    # Use latitude and longitude as needed
    return render(request, 'index.html',{})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method=='POST':
        username=request.POST.get('username')
        passw=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
            print('successfull')
        except:
            pass
        user=authenticate(request, username=username, password=passw)

        if user is not None:
            login(request,user)
            return redirect(reverse('profile', args=[request.user.id]))
        else:
             messages.error(request,'Username or password doesn\'t exist')
    return render(request,'login.html',{'message':messages})

def logoutUser(request):
    logout(request)
    return redirect('index')

def signup(request):
    users=list(User.objects.all().values_list('username',flat=True))
    print(users)
    if request.method=='POST':
        username=request.POST.get('username')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        password=request.POST.get('password')
        password2=request.POST.get('conf-password')
        if username not in users and password==password2:
            x=User.objects.create(
                username=username,
                password=password,
                first_name=firstname,
                last_name=lastname,
                email=email,
            )
            x.save()
            login(request,x)
            return redirect('user_det')
        elif username in users:
            messages.error(request,'Username already exists...')
        else:
            messages.error(request,'Passwords doesn\'t match...')
        '''user=forms.Register_user(request.POST)
        if user.is_valid():
            usr=user.save()
            login(request, usr)
            return redirect('index')'''
    return render(request,'sign-up.html')#,{'form':user})


def user_det(request):
    latitude=None
    longitude=None
    m=Mechanic.objects.all().values_list('shop_name',flat=True)
    if request.method=='POST':
        
        # Get user's IP address or any other available method to identify user location
        user_ip = request.META.get('REMOTE_ADDR')

        # Getting latitude and longitude of the ip
        response = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=b647ac5556484dfc8644a81135ff22a9&"+user_ip)
        res=json.loads(response.content)
        latitude = res['latitude']
        longitude = res['longitude']


        user=request.user
        name=request.POST.get('name')
        address=request.POST.get('address')
        shop_name=request.POST.get('shop')
        phone_number=request.POST.get('phone')
        about=request.POST.get('about')
        if shop_name in m:
            messages.error(request,"Shop name already exists")
        else:
            mech=Mechanic.objects.create(
                user=user,
                name=name,
                address=address,
                shop_name=shop_name,
                phone_number=phone_number,
                lattitude=latitude,
                longitude=longitude,
                about=about
            )
            mech.save()
            
            return redirect('index')
    return render(request,'user_det.html',{})

def profile(request,user):
    profile=Mechanic.objects.get(user=user)
    return render(request,'profile.html',{'profile':profile})