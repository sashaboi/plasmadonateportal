from django.http.response import JsonResponse
from django.shortcuts import render ,redirect
from django.http import HttpResponse , JsonResponse 
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserform ,userinfoform
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from .models import Userinfo ,requestplasma 
from django.contrib.auth.models import User
from geopy import distance
import folium 
from .decorators import unauthenticated_user 
from django.contrib.auth.decorators import login_required
import random
from .sms import send_sms




def home(request):
    print(request.user)
    return render(request, 'plasmasearchapp/index.html')

@login_required(login_url='login')
def donordash(request):
    userlog = request.user
    print(userlog)
    if requestplasma.objects.filter(donor = userlog):
        plasmarequests =requestplasma.objects.filter(donor = userlog).filter(accepted = False)
        context = {'plasmarequests':plasmarequests}
    else:
        print('no requests')

    if request.method =='POST':
        print(request.POST)
        doneefromform= request.POST.get('userid')
        print(doneefromform)
        doneeid = User.objects.get(username = doneefromform).pk
        requestplasma.objects.filter(donor= userlog , donee = doneeid).update(accepted = True)
        #SEND COMMUNICATION TO DONEE THAT USER HAS ACCEPTED REQUEST CONTACT HIM




    

    return render(request, 'plasmasearchapp/donordash.html',context)


@login_required(login_url='login')
def doneedash(request):
    userlog = request.user
    printlat = Userinfo.objects.get(user=userlog).lat
    printlong = Userinfo.objects.get(user=userlog).long
    userplace = (printlat , printlong)
    userlist = []
    distancea = []
    userbg = Userinfo.objects.get(user=userlog).bloodgroup
    m = folium.Map(location =[printlat, printlong], zoom_start = 15)
    


    for user in Userinfo.objects.all():
        if user.type == 'donor':
            print('user is donor')
            newplace = (user.lat , user.long)
            dist = distance.distance(userplace, newplace).km 
            if dist < int(100):
                print('user is within 5 km')
                print(user.bloodgroup)
                
                if userbg == (user.bloodgroup):
                    print('bg matches')
                    userlist.append(user)
                    distancea.append(dist)
                    userlat = user.lat
                    userlong = user.long
                    folium.Marker(location =[userlat, userlong] , tooltip =(user.first_name , user.last_name)).add_to(m)

    

    if request.method == 'POST':
        print(request.POST)
        donormatched = request.POST.get('userid')
        print(donormatched)
        usermatched = User.objects.get(pk = donormatched)
        
        if requestplasma.objects.filter(donor= usermatched , donee =request.user ,accepted = False):
            print('request already sent') 
        else:
            data = requestplasma(donor= usermatched , donee =request.user ,accepted = False) 
            # SEND COMMUNICATION TO DONOR THAT HE HAS A REQUEST
            data.save()


        
    

    m = m._repr_html_()

    context = {'userlist' : userlist , 'm': m}

    return render(request, 'plasmasearchapp/doneedash.html',context)


@unauthenticated_user
def signup(request):
    form = CreateUserform()
    if request.method == 'POST':
        form = CreateUserform(request.POST)
        if form.is_valid():
            form.save()
            useremail = form.cleaned_data.get('email')
            messages.success(request , 'Account was created for ' + useremail)
            return redirect('login')
        else:
            print(form.errors.as_data())
            print('error')



    
    context = {'form': form}
    return render(request, 'plasmasearchapp/signup.html',context)
    
@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        usernamea= request.POST.get('username')
        passworda = request.POST.get('password')
        user = authenticate(request,username = usernamea , password = passworda)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.info(request , 'Username or pass is incorrect')
    
    return render(request, 'plasmasearchapp/login.html')

def logoutpage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def latlong(request):
    if request.method =='POST':
        print('printing post data' , request.POST)
    return render(request, 'plasmasearchapp/latlong.html')


@login_required(login_url='login')
def testingpost(request):
    userlog = request.user
    if request.method == "POST":
        print(request.POST['lat'])
        alat = request.POST['lat']
        along = request.POST['long']
        
        Userinfo.objects.filter(user=userlog).update(lat=alat)
        Userinfo.objects.filter(user=userlog).update(long=along)
        
        return redirect('doneedash')
    

@login_required(login_url='login')
def infoform(request):
    form = userinfoform()
    userlog = request.user

    if Userinfo.objects.filter(user=userlog):
        form = userinfoform(instance=userlog)
        print('already exists')
        if request.method == 'POST':
            form = userinfoform(request.POST or None,request.FILES or None,instance=userlog)
            print('Printing post :', request.POST)
            print('printing post files :' , request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()

                afirst_name=form.cleaned_data['first_name']
                amiddle_name=form.cleaned_data['middle_name']
                alast_name=form.cleaned_data['last_name']
                aprofilepic=form.cleaned_data['profilepic']
                aphoneno=form.cleaned_data['phoneno']
                aage=form.cleaned_data['age']
                agender=form.cleaned_data['gender']
                alat=form.cleaned_data['lat']
                along=form.cleaned_data['long']
                adesctext=form.cleaned_data['desctext']
                acovidnegcert=form.cleaned_data['covidnegcert']
                acovidnegdate=form.cleaned_data['covidnegdate']
                aquartype=form.cleaned_data['quartype']
                agovtid=form.cleaned_data['govtid']
                abloodgroup=form.cleaned_data['bloodgroup']

                Userinfo.objects.filter(user=userlog).update(first_name=afirst_name)
                Userinfo.objects.filter(user=userlog).update(middle_name=amiddle_name)
                Userinfo.objects.filter(user=userlog).update(last_name=alast_name)
                Userinfo.objects.filter(user=userlog).update(profilepic=aprofilepic)
                Userinfo.objects.filter(user=userlog).update(phoneno=aphoneno)
                Userinfo.objects.filter(user=userlog).update(age=aage)
                Userinfo.objects.filter(user=userlog).update(gender=agender)
                Userinfo.objects.filter(user=userlog).update(lat=alat)
                Userinfo.objects.filter(user=userlog).update(long=along)
                Userinfo.objects.filter(user=userlog).update(first_name=afirst_name)
                Userinfo.objects.filter(user=userlog).update(desctext=adesctext)
                Userinfo.objects.filter(user=userlog).update(covidnegcert=acovidnegcert)
                Userinfo.objects.filter(user=userlog).update(covidnegdate=acovidnegdate)
                Userinfo.objects.filter(user=userlog).update(quartype=aquartype)
                Userinfo.objects.filter(user=userlog).update(govtid=agovtid)
                Userinfo.objects.filter(user=userlog).update(bloodgroup=abloodgroup)

                
                
                
                
                print('form is valid')
                return redirect('homepage')
            else:
                print(form.errors)

    else:
        print('first time')
        form = userinfoform()
        print('already exists')
        if request.method == 'POST':
            form = userinfoform(request.POST or None,request.FILES or None)
            print('Printing post :', request.POST)
            print('printing post files :' , request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()             
                
                print('form is valid')
                return redirect('homepage')
            else:
                print(form.errors)








    
    

    context = {'form': form}    
    return render(request, 'plasmasearchapp/infoform.html' ,context)


    
@login_required(login_url='login')
def phoneotp(request):
    
    
    if request.method == 'POST':
        print(request.POST)
        User = request.user
        Userlog = request.user
        userid = User.pk
        userotp =request.POST['otp']
        member = Userinfo.objects.get(user=User)
        assignedotp=member.sentotp
        print('assigned otp = ',assignedotp ,'userotp = ', userotp)
        if str(userotp) == str(assignedotp):
            print('otp is correct')
            Userinfo.objects.filter(user=User).update(phoneverified=True)           
            
            return redirect('homepage')
        else:
            print('incorrect otp')
    
    else :
        otp = random.randint(100000, 999999)
        User = request.user
        userid = User.pk
        member = Userinfo.objects.get(user=User)
        member.sentotp = otp
        member.save()
        number = member.phoneno
        print('printing data',member.sentotp)
        send_sms(number,otp)
        

    context = {}
    
    return render(request, 'plasmasearchapp/phoneotp.html',context)