import random
from django.shortcuts import render , HttpResponse , redirect
from datetime import datetime
from home.models import Contact 
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout , authenticate , login
from django.core.mail import send_mail
from authentication.settings import EMAIL_HOST_USER

# Create your views here.
def index(request):
    return render(request , 'index.html')

def home(request):
    return render(request , 'home.html')

def about(request):
    return render(request , 'about.html')

def courses(request):
    return render(request , 'courses.html')

def contact(request):
    if request.method == 'POST' :
        name = request.POST.get('name')
        email = request.POST.get('email')
        desc = request.POST.get('message')
        date = datetime.today()

        contact = Contact(name = name, email = email , desc = desc , date = date)
        contact.save()
        messages.success(request, "Thanks for contacting us !")
    
    return render(request , 'contact.html')

def loginUser(request):
    if request.method == 'POST' :
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username , password=password)
        if user is not None :
            login(request , user)
            return redirect("/after_login")
        
        else :
            messages.error(request, 'Invalid username or password.')
            return render(request , 'login.html')
        
    return render(request , 'login.html')

def after_login(request):
    if request.user.is_anonymous :
        return redirect("/login")
    return render(request , 'after_login.html')

def signup(request):
    if request.method == 'POST':
        user = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'signup.html')
        
        if User.objects.filter(username=user).exists():
            messages.error(request, 'User name is already registered.')
            return render(request, 'signup.html')

        user = User.objects.create_user(username=user, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully.')
        return redirect("/login")

    return render(request, 'signup.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")

def forgot_password(request):
    return render(request , 'forgot-password.html')

def generate_otp(request):
    return random.randint(100000 , 999999)

def emailverification(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            otp = generate_otp(request)
            request.session['otp'] = otp
            request.session['email'] = email
            send_mail("OTP for New Password", f"Your OTP for New Password is {otp}" , EMAIL_HOST_USER , [email] , fail_silently=True)
            return render(request , 'otp-verification.html')
        
        else :
            messages.error(request, 'Email is not registered')
            return render(request , 'forgot-password.html')
        
def verify_otp(request):
    if request.method == "POST" :
        entered_otp = request.POST["otp"]

        if int(entered_otp) == request.session.get("otp") :
            return render(request , "password-reset.html")

        # if int(entered_otp) == 1234 :
        #     return render(request , "password-reset.html")
        
        else:
            messages.error(request , "Invalid OTP")
            return render(request , "otp-verification.html")
        
    return render(request , "otp-verification.html")

def password_reset(request):
    if request.method == "POST":
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]
        
        if new_password == confirm_password:
            email = request.session.get('email')
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            messages.success(request, "Your password has been successfully reset.")
            return redirect('login')
        
        else:
            messages.error(request, "Passwords do not match.")
            return render(request, 'password-reset.html')
    
    return render(request, 'password-reset.html')