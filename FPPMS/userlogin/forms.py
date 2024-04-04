
from django import forms
from .models import MilestoneModel

class MileStoneForm(forms.ModelForm):
    class Meta:
        model = MilestoneModel
        fields = ['mileStoneTitle', 'mileStoneContent']



