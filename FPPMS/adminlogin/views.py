from datetime import timedelta
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import forms
from django.core.mail import send_mail
import urllib.parse
from FPPMS.settings import EMAIL_HOST_USER
from FPPMS.models import passwordreset
import uuid
import datetime
import time


redirectUrl = 'https://fppms.pythonanywhere.com/resetPassword?'    ##change link for the new password
appname= 'FPPMS '


def forgotpassword(request):

   return render(request, "authenticate/ForgotPassword.html")


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        else:
            if username == "":
                messages.error(request,('Invalid Username  '))
            elif password == "" :
                messages.error(request,('Invalid password  '))
            return redirect('login')

    else:
        return render(request,'authenticate/login.html',{})

def resetPassword(request):

    if request.method == 'GET':
        id = request.GET["id"]
        token = request.GET["token"]
        print('id',id,'token',token)
        if not passwordreset.objects.filter(userid=id).exists():
            raise Exception("token is not generated for the current user")
        else:
            psd = passwordreset.objects.get(userid=id)
            if psd.token == token:
                print('password changed!')
                context = {
                    "user_token": token,
                        }
                return render(request,'authenticate/resetPassword.html',context)
        return redirect('login')

    elif request.method == 'POST':
         pwd = request.POST['pass']
         cpwd = request.POST['cpassword']
         usertoken = request.POST['custId']
         if pwd == cpwd :
            if passwordreset.objects.filter(token=usertoken).exists():
                psd = passwordreset.objects.get(token=usertoken)
                curuser = User.objects.get(id=psd.userid)
                curuser.set_password(pwd)
                curuser.save()
                psd.delete()
            else:
                raise Exception( "token is not valid")
         else:
             raise Exception( "password is not valid")
    return redirect('login')

def getAndsaveToken(input):

    #curuser = User.objects.get(email=input)
    # if curuser is not None:
    if User.objects.filter(email=input):
        curuser = User.objects.get(email=input)
        print('current user',curuser.email,curuser.id)
        if not passwordreset.objects.filter(userid=curuser.id).exists():
            psd = passwordreset.objects.create(userid=curuser.id,isvalid=1)
        else:
            psd = passwordreset.objects.get(userid=curuser.id)
        psd.token = uuid.uuid1().hex
        psd.save()
        return psd.token, curuser.id
    # else:
        # raise Exception("User does not exist")
    # return psd.token, curuser.id

def logout_user(request):
    logout(request)
    messages.success(request,('You were logged out'))
    return redirect('login')



def subscribe(request):

    sub = forms.Subscribe()
    if request.method == 'POST':
        sub = forms.Subscribe(request.POST)
        subject = appname+'<IMP> : Password Reset Link'
        recepient = str(sub['Email'].value())
        print(recepient)
        if User.objects.filter(email=recepient):
            token ,id = getAndsaveToken(recepient)
            message = getMessageContent(token,id)
            send_mail(subject,
                message, EMAIL_HOST_USER, [recepient], fail_silently = False)
            return render(request, 'authenticate/login.html')
        else:
            var_messages_error = "User Does Not Exist !"
            context={'var_messages_error':var_messages_error, 'recepient':recepient}
            return render(request, 'authenticate/ForgotPassword.html', context)
    return render(request, 'authenticate/ForgotPassword.html')


def getMessageContent(token, id):
    queryparam = { 'next' : '/admin/','token':token,'id':id}
    body = 'Dear User,\r\n\nPlease click on the below link to reset your password.\r\n{0}\r\n\nRegards,\nFPPMS Team'.format(redirectUrl+urllib.parse.urlencode(queryparam))
    return body

