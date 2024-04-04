"""FPPMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, re_path
from django.contrib import admin
from django.urls import path
from rest_framework import views

from . import views as mainviews
from adminportal import views as adminportal_views
from adminlogin import views as adminlogin_views
from userlogin import views as userlogin_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve



urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('Insertproposal',mainviews.saveproposal,name="saveproposal"),   
    path('',mainviews.insertproposal, name="home"),
    path('displayProposal',adminportal_views.displayProposal,name="displayProposal"),
    path('proposals',adminportal_views.displayProposalList, name="proposals"),
    path('addAdmin',adminportal_views.addAdmin, name="addAdmin"),
    path('dashboard',adminportal_views.dashboard,name="dashboard"),
    path('forgotpassword',adminlogin_views.forgotpassword,name="forgotpassword"),
    path('forgotpasswordlink', adminlogin_views.subscribe, name ="subscribe"),
    path('adminlogin/', include('django.contrib.auth.urls')),
    path('adminlogin/', include('adminlogin.urls')),
    path('aboutus', mainviews.aboutus, name="about"),
    path('faq', mainviews.faq, name="faq"),
    path('resetPassword', adminlogin_views.resetPassword, name="resetPassword"),
    path('deleteProposal/<int:pk>', adminportal_views.delete, name="deleteProposal"),
    path('updateProposal/<int:pk>', adminportal_views.update, name="updateProposal"),
    path('addUser',adminportal_views.addUser, name="addUser"),
    path('addSingleUser',adminportal_views. addSingleUser, name="addSingleUser"),
    path('userlogin/', include('userlogin.urls')),
    path('allMilestones',adminportal_views.allMilestones,name="allMilestones"),
    path('deleteUser/<int:user_id>/', adminportal_views.deleteUser, name="deleteUser"),
    path('adminlogin/login_user', adminportal_views.AdminLoginView.as_view(), name='login_user'),
   
    # path('upload_excel',adminportal_views.upload_excel,name="upload_excel"),
    
    #path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    #url(r'^download/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT}),
    
    
    path('downloadfile/<str:filename>', adminportal_views.downloadproposalfile, name="downloadfile"),
    
    

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)