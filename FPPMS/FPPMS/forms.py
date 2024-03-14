# forms.py
from django import forms
from django.core.exceptions import ValidationError

class ProposalForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, error_messages={'required': "Please don't leave this field empty."})
    fname = forms.CharField(max_length=100, required=True)
    lname = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)
    userType = forms.CharField(max_length=20, required=True)
    status = forms.CharField(max_length=20, required=True)
    ptitle = forms.CharField(max_length=100, required=True)
    pwebsite = forms.URLField(required=True)
    pdesc = forms.CharField(widget=forms.Textarea, required=True)
    comment = forms.CharField(widget=forms.Textarea, required=True)
    reference = forms.CharField(max_length=100, required=True)
    document = forms.FileField(required=False)

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit():
            raise ValidationError("Phone number should only contain digits.")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@example.com'):  # Add your email domain validation
            raise ValidationError("Please use a valid email address.")
        return email

    def clean_document(self):
        document = self.cleaned_data.get('document')
        if document:
            # Add file type validation if needed
            allowed_types = ['pdf', 'doc', 'docx']
            file_type = document.name.split('.')[-1].lower()
            if file_type not in allowed_types:
                raise ValidationError("Invalid file type. Please upload a PDF or Word document.")
        return document

    def clean(self):
        cleaned_data = super().clean()
        # Add additional custom validation if needed
        return cleaned_data
