
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Driver,Dbuser,Catalog,Sponsor,Administrator
from .forms import CreateNewCatalog,CHOICES
from django.db.models import Q
from .models import Driver,Dbuser,Sponsor,Employs
from ebaysdk.shopping import Connection as shopping
from bs4 import BeautifulSoup
import smtplib  
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def removeFakeSponsor(request):
    Employs.objects.filter(drivers=999999).delete()
    Driver.objects.filter(id=999999).delete()
    Dbuser.objects.filter(dbuser_id=999999).delete()
    return render(request,'Sponsor/fakeDriver.html')

def fakeDriver(request):
    fakeDbuser = Dbuser(dbuser_id=999999,user_password='test',created_date="00/00/00",updated_date="00/00/00")
    fakeDbuser.save()
    fakeDriver = Driver(id=fakeDbuser,driver_name='fakeDriver',employee_number=999999,driver_address="---",driver_points=1,driver_rate=1)
    fakeDriver.save()
    try: 
        Employs.objects.get(drivers=999999)
        employDriver = Employs.objects.get(drivers=999999)
    except Employs.DoesNotExist:
        employDriver = Employs(sponsors=Sponsor.objects.get(id=Dbuser.objects.get(dbuser_id=request.user.id)),drivers=fakeDriver,driver_points=999999)
        employDriver.save()
    return render(request,'Sponsor/fakeDriver.html',{'driver':employDriver})

def mainPage(request):
    return HttpResponseRedirect('/login')

def sendEmail(send_from, send_to, subject, message):
    msg = email.message.Message()
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Subject'] = subject
    msg.add_header('Content-Type', 'text')
    msg.set_payload(message)
    smtp_obj = smtplib.SMTP("localhost")
    smtp_obj.sendmail(msg['From'], [msg['To']], msg.as_string())
    smtp_obj.quit()

def sendEmail(send_from, send_to, subject, msg):
    RECIPIENT  = send_to
    send_from="root@ahhtiger.com"
    HOST = "email-smtp.us-west-2.amazonaws.com"
    PORT = 587
    SUBJECT = subject
    BODY_TEXT = msg
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Drivers</h1>
    <p>"""+msg+"""</p>
    </body>
    </html>
                """
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr(("Drivers", send_from))
    msg['To'] = RECIPIENT
    part1 = MIMEText(BODY_TEXT, 'plain')
    part2 = MIMEText(BODY_HTML, 'html')
    msg.attach(part1)
    msg.attach(part2)
    try:  
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("AKIAZZ2UPLYCPTWWT6O3","BEVcUJXPgZ4s3ZBFumhgCEwuQAi73RIzVt8HsWmfB6DZ")
        server.sendmail(send_to, RECIPIENT, msg.as_string())
        server.close()
    except Exception as e:
        print ("Error: ", e)
    else:
        print ("Email sent!")
    
# Create your views here.
def home(request):
    user=request.user
    if Administrator.objects.filter(auser=user.id):
        return redirect('/admin')
    elif Sponsor.objects.filter(id=user.id):
        return redirect('sponsor-profile')
    elif Driver.objects.filter(id=user.id):
        return redirect('user-profile')

def loginRedirect(request):
    user=request.user
    if Administrator.objects.filter(auser=user.id):
        return redirect('/admin')
    elif Sponsor.objects.filter(id=user.id):
        return redirect('sponsor-profile')
    elif Driver.objects.filter(id=user.id):
        return redirect('user-profile')
    #return HttpResposneRedirect('/admin')
    return redirect('/admin')

@login_required
def profile(request):
    user=request.user
    driver=Driver.objects.get(id=user.id)
    if Employs.objects.filter(drivers=user.id).exists():
        employer = Employs.objects.filter(drivers=user.id)
        return render(request,'User/profile.html',{'driver':driver,'pointvalue':employer})
    else:
        return render(request,'User/profile.html',{'driver':driver})

#@login_required
def sponsorProfile(request):
    driverdata = []
    notsponsoreddrivers =[]
    driverpoints = []
    user = request.user
    if(Employs.objects.exists()):
        dofs = Employs.objects.filter(sponsors=user.id).values_list('drivers',flat=True)
        for drivers in dofs:
            driverdata.extend(Driver.objects.filter(id=drivers))
            driverpoints.extend(Employs.objects.filter(drivers=drivers))
        notsponsoreddrivers = Driver.objects.exclude(id__in=dofs)
        return render(request,'Sponsor/sponsorProfile.html',{'test':driverdata,'nonsponsored':notsponsoreddrivers,'points':driverpoints})
    else:
        nonsponsoreddrivers = Driver.objects.all()
        return render(request,'Sponsor/sponsorProfile.html',{'nonsponsored':nonsponsoreddrivers})

def addDriver(request):
    if request.method=="POST":
        driver = request.POST.get("addDriver")
        userid = request.user
        driverid = Driver.objects.get(driver_name=driver)
        employDriver = Employs(sponsors=Sponsor.objects.get(id=Dbuser.objects.get(dbuser_id=userid.id)),drivers=driverid,driver_points=0)
        #employDriver = Employs(sponsors=Sponsor.objects.get(suser=Dbuser.objects.get(dbuser_id=userid.id)),drivers=Driver.objects.get(duser=driverid.duser))
        employDriver.save()
    return redirect('sponsor-profile')

def removeDriver(request):
    if request.method=="POST":
        driver = request.POST.get("removeDriver")
        driver=driver.rsplit(' ', 1)[0]
        userid =request.user
        driverid = Driver.objects.get(driver_name=driver)
        Employs.objects.filter(drivers=driverid).delete()
    return redirect('sponsor-profile')

#@login_required
def addpoints(request):
    if(Employs.objects.exists()):
        #names =[driver['driver_name'] for driver in list(Driver.objects.all().values())]
        names = Employs.objects.filter(sponsors = request.user.id)
        return render(request,'User/addpoints.html',{'names':names})
#@login_required
def updatePassword(request):
    #names =[driver['username'] for driver in list(User.objects.all().values())]
    names = request.user
    return render(request,'User/updatePassword.html',{'names':names})
#@login_required
def PostUpdatePassword(request):
    username=request.POST.get("username", "")
    password1=request.POST.get("password1", "")
    password2=request.POST.get("password2")
    if password1 == password2:
        user = request.user
        user.set_password(password1)
        user.save()
        dbuserobj = Dbuser.objects.get(dbuser_id=request.user.id)
        dbuserobj.user_password=password1
        dbuserobj.save()
        if Sponsor.objects.filter(id=request.user.id):
            updatedSponsor = authenticate(username=username,password=password1)
            login(request,updatedSponsor)
            return redirect('sponsor-profile')
        elif Driver.objects.filter(id=request.user.id):
            updatedDriver = authenticate(username=username,password=password1)
            login(request,updatedDriver)
            return redirect('user-profile')
    return HttpResponse("updated password")
#@login_required
def PostPoint(request):
    points=request.POST.get("points", "")
    username=request.POST.get("username", "")
    driverid = Driver.objects.filter(driver_name=username)
    employsobj = Employs.objects.filter(drivers__in=driverid).get(sponsors=request.user.id)
    employsobj.driver_points=points
    employsobj.save()
    userid=Driver.objects.get(driver_name=username).id.dbuser_id
    email=User.objects.get(id=userid).email
    sendEmail("root@ahhtiger.com",email,"Points","Your points has been updated by your sponser")

    #confirmation mail
    semail=User.objects.get(id=request.user.id).email
    sendEmail("root@ahhtiger.com",semail,"Points","You just added points to "+email)
    return HttpResponse("Updated points. Sent a email to "+email)
#@login_required
def PostPointDist(request):
    rate = request.POST.get("points", "")
    username=request.POST.get("username", "")
    Driver.objects.filter(driver_name=username).update(driver_rate=rate)
    return redirect('sponsor-profile')

#@login_required
def updateUsername(request):
    names =[driver['username'] for driver in list(User.objects.all().values())]
    return render(request,'User/updateUsername.html',{'names':names})
#@login_required
def PostUpdateUsername(request):
    username=request.POST.get("username", "")
    nusername=request.POST.get("newusername", "")
    user = User.objects.get(username=username)
    user.username=nusername
    user.save()
    return HttpResponse("updated username")

def register(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password1']
        verifypassword=request.POST['password2']
        userType=request.POST.get('userType',None)
        if password == verifypassword:
           u = User.objects.create_user(username=username,password=password)
           u.save()
           if userType == "Driver":
              dbuserobj = Dbuser(dbuser_id=u.id,user_password=password,created_date="00/00/00",updated_date="00/00/00")
              dbuserobj.save()
              driverobj = Driver(id=dbuserobj,driver_name=username,employee_number=1,driver_address="---",driver_points=1,driver_rate=0)
              driverobj.save()
              newuser=authenticate(username=username,password=password)
              login(request,newuser)
              return redirect('user-profile')
           elif userType == "Sponsor":
              dbuserobj = Dbuser(dbuser_id=u.id,user_password=password,created_date="00/00/00",updated_date="00/00/00")
              dbuserobj.save()
              sponsorobj = Sponsor(id=Dbuser.objects.get(dbuser_id=dbuserobj.dbuser_id),company_name=username,comp_address="---",point_value=1,payment_method="Credit",payment_numb=1)
              #sponsorobj = Sponsor(id=dbuserobj,company_name=username,comp_address="---",point_value=1,payment_method="Credit",payment_numb=1)
              sponsorobj.save()
              newuser=authenticate(username=username,password=password)
              login(request,newuser)
              return redirect('sponsor-profile')
           elif userType == "Admin":
              dbuserobj = Dbuser(dbuser_id=u.id,user_password=password,created_date="00/00/00",updated_date="00/00/00")
              dbuserobj.save()
              adminobj = Administrator(auser=Dbuser.objects.get(dbuser_id=dbuserobj.dbuser_id),admin_name=username,admin_email="---",admin_phone=1)
              adminobj.save()
              newuser=authenticate(username=username,password=password)
              login(request,newuser)
              return redirect('/admin/')
        else:
           messages.error(request,'Passwords do not match try again')
           return redirect('register')
    return render(request,"registration/register.html")

#@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

#@login_required
def updateName(request):
    if request.method=="POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        User = request.user
        User.first_name = firstname
        User.last_name = lastname
        User.save()
        driverobj = Driver.objects.get(id=User.id)
        driverobj.driver_name = firstname + ' ' + lastname
        driverobj.save()
        return redirect('user-profile')
    return render(request,"User/updateName.html")
#@login_required
def updateEmail(request):
    if request.method=="POST":
        email = request.POST['email']
        User = request.user
        User.email = email
        User.save()
        if Sponsor.objects.filter(id=User.id):
            return redirect('sponsor-profile')
        elif Driver.objects.filter(id=User.id):
            return redirect('user-profile')
    return render(request,"User/email.html")
#@login_required
def updateAddress(request):
    if request.method=="POST":
        address = request.POST['address']
        User = request.user
        User.address = address
        User.save()
        driverobj = Driver.objects.get(id=User.id)
        driverobj.driver_address = address
        driverobj.save()
        return redirect('user-profile')
    return render(request,"User/address.html")
#@login_required
def createCatalog(request):
    if request.method == "POST":
        form = CreateNewCatalog(request.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            c = Catalog(name=n)
            c.save()

        return HttpResponseRedirect("/%i" %c.id)

    form = CreateNewCatalog()
    return render(request, 'User/createCatalog.html', {'form':form})
#@login_required
def index(request, id):
    cat = Catalog.objects.get(id=id)
    return render(request, 'User/catalog.html', {'cat':cat})


def readIncentive(request): 
#    if request.method=="POST": 
#        incentive = request.POST['incentive'] 
#        User = request.user 
#        User.incentive = incentive 
#        User.save() 
    return render(request,"Sponsor/incentive.html")
#Might need to change this Need to ad an html file for the point_value
def updateDollarVal(request): 
     if request.method=="POST": 
         pointValue = request.POST['Dollar Value'] 
         User = request.user
         sponsorobj = Sponsor.objects.get(id=User.id)
         sponsorobj.point_value = pointValue 
         sponsorobj.save()
         return redirect('sponsor-profile')
     return render(request,"Sponsor/UpdateDollarVal.html") 

def paymentmethod(request): 
    #if request.method=="POST": 
    form=CHOICES(request.POST)
    if form.is_valid():
        card_type = form.cleaned_data.get("paymentmethod") 
        card_number = request.POST.get("card_number") 
        userid = request.user.id
        sponsor = Sponsor.objects.get(id=userid)
        sponsor.payment_method = card_type 
        sponsor.payment_numb = card_number 
        sponsor.save()
        return redirect("sponsor-profile")
    return render(request,"Sponsor/paymentmethod.html",{'form':form})

def removeSponsor(request):
    if request.method=="POST":
        sponsor = request.POST.get("removeSponsor")
        sponsor=sponsor.split(' ', 1)[1]
        userid =request.user
        sponsorid = Sponsor.objects.get(company_name=sponsor)
        Employs.objects.filter(sponsors=sponsorid).delete()
    return redirect('user-profile')
