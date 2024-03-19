from decimal import Context, ConversionSyntax
import json
import os
import re
from django import contrib
import mimetypes
from django.http.response import JsonResponse
from django.shortcuts import render
from userlogin.models import MilestoneModel
import rest_framework
from rest_framework import serializers
from rest_framework import response
from adminportal.serialization import AdminSerializationClass
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from FPPMS.models import Proposalmodel
from django.shortcuts import render
from rest_framework import status
import requests
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.contrib.auth.forms import UserCreationForm
import pandas as pd

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django import forms




@api_view(['GET'])
def displayProposal(request):
    if request.method == 'GET':
        results = Proposalmodel.objects.all()
        serialize = AdminSerializationClass(results, many=True)
        return Response(serialize.data)


def displayProposalList(request):
    results = Proposalmodel.objects.all()
    serialize = AdminSerializationClass(results, many=True)
    return render(request, 'proposals.html', {'Proposalmodel': serialize.data})

# callapi = requests.get('https:///displayProposal')
# results = callapi.json()
# return render(request,'proposals.html',{'Proposalmodel': results})


# Create your views here.
# def addAdmin(request):
#     results = Proposalmodel.objects.all()
#     return render(request, "addAdmin.html",{'Proposalmodel':results})

def addAdmin(request):
    # print(request.method)
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        mob = request.POST['mob']
        password = request.POST['job']
        # print(fname +" "+ lname+" "+email +" "+ mob)
        user = User.objects.create_user(fname, email, password)
        user.save()
        return redirect('home')
    return render(request, 'addAdmin.html')

@login_required
def dashboard(request):
    approved = 0
    rejected = 0
    split = 0
    pending = 0
    adminCount = User.objects.filter(is_staff=True).count()
    results = Proposalmodel.objects.all()
    admins= User.objects.filter(is_staff=True)
    allMilestones = MilestoneModel.objects.count()
    non_staff_users = User.objects.filter(is_staff=False).count()
    all_non_staff_users =User.objects.filter(is_staff=False)

    for data in results:
        if (data.status == "Approved"):
            approved = approved + 1
        if (data.status == "Rejected"):
            rejected = rejected + 1
        if (data.status == "Split"):
            split = split + 1
        if (data.status == "Pending"):
            pending = pending + 1

    final = {
        'Proposalmodel': results,
        'approved': approved,
        'rejected': rejected,
        'split': split,
        'pending': pending,
        'adminCount': adminCount,
        'allMilestones': allMilestones,
        'user': non_staff_users,
        'admins': admins,
        'all_non_staff_users': all_non_staff_users

    }
    return render(request, "dashboard.html", final)


def delete(request, pk):
    Proposalmodel.objects.filter(pk=pk).delete()
    results = Proposalmodel.objects.all()

    context = {
        'results': results
    }
    return render(request, "proposals.html", {'Proposalmodel': results})

# def update(request,pk):
#     data = request.body
#     results = Proposalmodel.objects.filter(pk=pk)
#     serialize = AdminSerializationClass(results,data=data)
#     if serialize.is_valid():
#         serialize.save()
#         results = serialize.data
#         return render(request, "proposals.html", {'Proposalmodel': results})
#     return render(request, "proposals.html")


def update(request, pk):
    # TODO: clean data here
    payload = {}
    payload['fname'] = request.POST["fname"]
    payload['lname'] = request.POST["lname"]
    payload['phone'] = request.POST["phone"]
    payload['email'] = request.POST["email"]
    payload['userType'] = request.POST["userType"]
    payload['ptitle'] = request.POST["ptitle"]
    payload['pdesc'] = request.POST["pdesc"]
    payload['status'] = request.POST["status"]
    payload['pwebsite'] = request.POST["pwebsite"]
    payload['comment'] = request.POST["comment"]
    payload['reference'] = request.POST["reference"]
    # payload['document'] = request.POST["document"]

    # save
    proposal = Proposalmodel.objects.get(id=pk)
    serializer = AdminSerializationClass(proposal, data=payload, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return redirect('proposals')

    # in case you want to return the json of the data
    # result = serializer.data
    # return JsonResponse(result)


# def proposalCount(request):
#     proposals = Proposalmodel.objects.all()
#     totalProposal_count = proposals.count()

#     context = {
#         'proposals' : proposals,
#         'totalProposal_count' : totalProposal_count
#     }

#     return render(request, 'dashboard.html' , context)

def send_dictionary(request):
    proposals = Proposalmodel.objects.all()
    totalProposal_count = proposals.count()
    dataDictionary = {
        'totalProposal': totalProposal_count,
    }

    dataJSON = json.dumps(dataDictionary)
    return render(request, 'proposals.html', {'data': dataJSON})


# Define function to download pdf file using template
def downloadproposalfile(request, filename=''):
    if filename != '':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # print(BASE_DIR)
        # Define the full file path
        filepath = BASE_DIR + '/media/' + filename
        # filepath = 'FPPMS/media/' + filename
       # print(filepath)
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
       # print("******tseting")
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    else:
        # Load the template
        # print("tseting else **")
        return render(request, 'file.html')


class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()


# def process_excel_file(excel_file):
#     df = pd.read_excel(excel_file)
#     for index, row in df.iterrows():
#         username = row['Username']
#         password = row['Password']
#         if not User.objects.filter(username=username).exists():
#             User.objects.create_user(username=username, password=password)



# def upload_excel(request):
#     if request.method == 'POST':
#         form = ExcelUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             excel_file = request.FILES['excel_file']
#             process_excel_file(excel_file)
#             print('success')
#         return HttpResponse("File uploaded successfully!")
#     else:
#         form = ExcelUploadForm()
#         return HttpResponse("Method not allowed", status=405)
    
    
# def addUser(request):

#     return render(request, 'addUser.html')
    

def addSingleUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, password=password)
                return render(request, 'addUser.html', {'message': "User created successfully"})
            else:
                return render(request, 'addUser.html', {'error': "Username already exists"})
        else:
            return render(request, 'addUser.html', {'error': "Please provide both username and password"})
    else:
        return render(request, 'addUser.html')


def addUser(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)
            for index, row in df.iterrows():
                username = row['Username']
                password = row['Password']
                if not User.objects.filter(username=username).exists():
                    User.objects.create_user(username=username, password=password)
           
            return render(request, 'addUser.html', {'message': "Students created successfully"})
            
    else:
        form = ExcelUploadForm()
    return render(request, 'addUser.html', {'form': form})




def allMilestones(request):
    milestones = MilestoneModel.objects.all()
    return render(request, 'allMilestones.html',{'milestones':milestones})
   
    
from django.shortcuts import render, redirect
from django.contrib import messages

def deleteUser(request, user_id):
    # Check if the user making the request is a staff user
    if request.user.is_staff:
        try:
            # Get the user object to delete
            user_to_delete = User.objects.get(id=user_id)
            # Delete the user
            user_to_delete.delete()
            # Provide a success message
            messages.success(request, "User deleted successfully.")
            return render(request, 'dashboard.html')
        except User.DoesNotExist:
            # If the user with the specified ID does not exist, provide an error message
            messages.error(request, "User does not exist.")
    else:
        # If the user making the request is not a staff user, provide an error message
        messages.error(request, "You are not authorized to delete users.")
    
    # Query for users or any other necessary data to render the page
    users = User.objects.all()
    
    # Render the template with appropriate context
    return render(request, 'dashboard.html')
