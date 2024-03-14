from django.contrib import admin
from django.db import models  # Import models module from Django
from .models import MilestoneModel
from ckeditor.widgets import CKEditorWidget

class MilestoneModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}  
    }

admin.site.register(MilestoneModel, MilestoneModelAdmin)
