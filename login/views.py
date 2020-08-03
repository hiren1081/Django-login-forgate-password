from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string, get_template
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.conf import settings
 


@login_required(login_url = '/login/')
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if(password1 == password2):
            user = User.objects.filter(username=username, password=password1, email=email)
            if user:
                return HttpResponse("username is already taken")
            else:
                new_user = User.objects.create_user(username=username, email=email, password=password2)
                new_user.save()
                return redirect('/login/')
    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/home/')
        else:
            return HttpResponse("username and password not match")
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/login/')


def forgate(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subject, from_email, to = 'Click Link And Reset Password', settings.EMAIL_HOST_USER, email
        text_content = 'Click the Link'
        html_content = '<a href = "http://127.0.0.1:8000/recover">Click Hear for reser your password</a> '
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        request.session['email'] = email
        return HttpResponse('chack your email')
    return render(request, 'forgate.html')


def recover(request):
    email = request.session.get('email')
    if request.method == 'POST':
        password1 = request.POST.get('pass1')
        password2 = request.POST.get('pass2')
        if(password1 == password2):
            user = User.objects.filter(email=email)[0]
            user.set_password(password2)
            user.save()
            return redirect('/login/')
        else:
            return HttpResponse('please chack your password')
    return render(request, 'recover.html')
