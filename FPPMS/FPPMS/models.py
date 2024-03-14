from typing import Reversible
from django.db import models
from django.dispatch import receiver
from django.urls import reverse

class Proposalmodel(models.Model):
    title=models.CharField(max_length=250)
    fname=models.CharField(max_length=250)
    lname=models.CharField(max_length=250)
    phone=models.CharField(max_length=12)
    email=models.CharField(max_length=250)
    userType=models.CharField(max_length=250, default="other")
    status=models.CharField(max_length=255)
    ptitle=models.CharField(max_length=250)
    pdesc=models.CharField(max_length=2323250)
    pwebsite=models.CharField(max_length=250)
    comment=models.CharField(max_length=133234250)
    reference=models.CharField(max_length=250)
    document=models.FileField(blank=True, null=True)
    
    
    class Meta:
        db_table="proposals"

class passwordreset(models.Model):
    userid=models.IntegerField()
    token=models.CharField(max_length=250)
    isvalid=models.IntegerField()
    validtill=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'PasswordReset'
        managed = True
        