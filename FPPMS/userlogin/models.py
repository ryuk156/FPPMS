from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.models import AbstractUser


from ckeditor.fields import RichTextField



class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField()



class MilestoneModel(models.Model):
    mileStoneTitle = models.CharField(max_length=200)
    mileStoneContent = RichTextField()
    mileStoneAuthor = models.ForeignKey(User, on_delete=models.CASCADE)
    mileStonePublishDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mileStoneTitle
    



