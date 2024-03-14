import re
from .forms import ProposalForm
from FPPMS.models import Proposalmodel
from FPPMS.serialize import Proposalserialize
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
import requests
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.db import connection
from FPPMS.settings import EMAIL_HOST_USER
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect

from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages







@api_view(['POST'])
def saveproposal(request):
    if request.method == "POST":
        saveserialize = Proposalserialize(data=request.data)
        
        try:
            myfile = request.FILES['file']  # Update 'file' to the correct key for the file upload field
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            document = filename
        except MultiValueDictKeyError:
            document = None  # Handle case when file is not uploaded
        
        if saveserialize.is_valid():
            saveserialize.save()
            messages.success(request, 'Your proposal was successfully sent! You will be contacted regarding the proposal soon.')
            emails = prepareEmailForSenders()
            sub, msg = getEmailBody()
            for email in emails:
                send_mail(sub, msg, "Fanshawe BIA Project Proposal", [email], fail_silently=False)
            return render(request, 'index.html')
        else:
            # Render the form with error messages
            messages.error(request, 'Sorry, data not saving!')
            return render(request, 'index.html', {'form': saveserialize.errors})
    
    return Response(status=status.HTTP_400_BAD_REQUEST)



def insertproposal(request):
    if request.method == "POST":
        form = ProposalForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            headers = {'Content-Type': 'application/json'}
            read = requests.post('http://127.0.0.1:8000/Insertproposal', json=data, headers=headers)

            if read:
                messages.success(request, 'Your proposal was successfully sent! You will be contacted regarding the proposal soon.')
                emails = prepareEmailForSenders()
                sub, msg = getEmailBody()

                for email in emails:
                    send_mail(sub, msg, "Fanshawe BIA Project Proposal", [email], fail_silently=False)

                return render(request, 'index.html')
            else:
                messages.error(request, 'INVALID Data!')
        else:
            messages.error(request, 'Sorry, data not saving!')
    else:
        form = ProposalForm()

    return render(request, 'index.html', {'form': form})
    
def getProjectDetails():
    with connection.cursor() as cursor:
        cursor.execute("SELECT title, fname || lname FROM `proposals` as p order by p.id desc")
        row = cursor.fetchone()
    return row

def getEmailBody():
    row = getProjectDetails()
    msg = 'Dear Project Proposal Admin,\r\n\nA new Fanshawe BIA project proposal has been submitted in the system by '+row[1] + '.\r\n\nPlease access the admin area https://fppms.pythonanywhere.com/adminlogin/login_user? to view it. \r\n\nRegards,\r\nFanshawe Project Proposal\r\nhttps://fanshaweprojectproposals.ca'
    title  = 'New BIA Project Proposal Received : ' +row[0]
    return title, msg

def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("SELECT email FROM `auth_user` where is_superuser = 1")
        rows = cursor.fetchall()
    return rows

def prepareEmailForSenders():
    rows = my_custom_sql()
    emails = list()
    for sig in rows:
        emails.append(sig[0])
    return emails


def aboutus(request):
    return render(request, "GetToKnowUs.html")

def faq(request):
    return render(request, "FAQ.html")