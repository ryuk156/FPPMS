from http.client import HTTPResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect, render
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AbstractUser
from django.db import models
from .forms import MileStoneForm
from .models import MilestoneModel
from django.shortcuts import get_object_or_404





#studenthome
def student_home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('studentdashboard')
        else:
            messages.error(request,('Invalid Username or Password '))
            return redirect('studentlogin')

    else:
        return render(request,'authentication/login.html',{})
    
def student_Logout(request):
    logout(request)
    return redirect('studentlogin')  

#studentdashboard
@login_required
def student_dashboard(request):
    milestones = MilestoneModel.objects.filter(mileStoneAuthor=request.user)
   
    return render(request, "authentication/dashboard.html", {'milestones': milestones})


@login_required
def delete_milestone(request, milestone_id):
    # Get the milestone object or return a 404 error if not found
    milestone = get_object_or_404(MilestoneModel, pk=milestone_id)
    
    # Check if the milestone belongs to the current user
    if milestone.mileStoneAuthor != request.user:
        # Optionally, handle unauthorized access (e.g., return an error page)
        return HTTPResponse("You are not authorized to delete this milestone.")

    if request.method == 'POST':
        # Delete the milestone
        milestone.delete()
        messages.success(request, 'Milestone deleted successfully.')
        return redirect('studentdashboard')
    
    return render(request, 'authentication/delete_milestone.html', {'milestone': milestone})

#studentMileStoneCreate
@login_required
def student_createmilestone(request):
    if request.method == 'POST':
        form = MileStoneForm(request.POST)
        if form.is_valid():
            milestone = form.save(commit=False)
            milestone.mileStoneAuthor = request.user
            milestone.save()
            # Set the new_post_added variable to True to indicate a new post has been added
            new_post_added = True
            return render(request, 'authentication/create_milestone.html', {'form': form, 'new_post_added': new_post_added})
    else:
        form = MileStoneForm()
    
    # If the request method is not POST or the form is invalid, render the page without the new_post_added variable
    return render(request, 'authentication/create_milestone.html', {'form': form})
    

    


