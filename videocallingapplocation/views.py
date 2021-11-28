from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .decorators import unauthenticated_user
from django.contrib import messages

# Create your views here.
def loginuser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request,user)
            print("LOGGED IN:",request.user.get_username())
            return redirect("index")
        else:
            print("Could not log the user in")
            messages.warning(request, "Invalid Credentials")
            redirect("login")
    else:
        print(request.method)
    return render(request,"videocallingapplocation/html/login.html")

@unauthenticated_user
def logoutuser(request):
    logout(request)
    return redirect("login")

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email_id = request.POST['email_id']
        if username != "" and password != "" and email_id !="" and User.objects.filter(username = username).count()==0 and all([i in "abcdefghijklmnopqrstuvwxyz1234567890" for i in username]) and all([i in "abcdefghijklmnopqrstuvwxyz1234567890" for i in password]):
            User.objects.create_user(username=username,password=password,email=email_id)
            messages.success(request,"User Registered Successfully")
            return redirect("login")
        else:
            if User.objects.filter(username = username).count()!=0:
                messages.warning(request, "User already exists.")
            elif not all([i in "abcdefghijklmnopqrstuvwxyz1234567890" for i in username]):
                messages.warning(request,"Username can only be alphanumeric.")
            elif not all([i in "abcdefghijklmnopqrstuvwxyz1234567890" for i in password]):
                messages.warning(request,"Password can only be alphanumeric.")
            else:
                messages.warning(request, "Could not create the user")
            return redirect("register")
    return render(request,"videocallingapplocation/html/register.html")

@unauthenticated_user
def index(request):
    if request.user.is_authenticated:
        return render(request,'videocallingapplocation/html/index.html')
    else:
        return redirect("login")

@unauthenticated_user
def room(request,room_name):
    return render(request,'videocallingapplocation/html/room.html',{"room_name":room_name})
