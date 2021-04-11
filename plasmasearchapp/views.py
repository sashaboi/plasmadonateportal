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





def home(request):
    print(request.user)
    return render(request, 'plasmasearchapp/index.html')


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



def doneedash(request):
    userlog = request.user
    printlat = Userinfo.objects.get(user=userlog).lat
    printlong = Userinfo.objects.get(user=userlog).long
    userplace = (printlat , printlong)
    userlist = []
    distancea = []
    userbg = Userinfo.objects.get(user=userlog).bloodgroup
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


        
    



    context = {'userlist' : userlist }

    return render(request, 'plasmasearchapp/doneedash.html',context)



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


def latlong(request):
    if request.method =='POST':
        print('printing post data' , request.POST)
    return render(request, 'plasmasearchapp/latlong.html')

def testingpost(request):
    if request.method == "POST":
        print(request.POST)
        
    resp = {

    }
    return JsonResponse(resp)

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
                Userinfo.objects.filter(user=userlog).update(last_name=aprofilepic)
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