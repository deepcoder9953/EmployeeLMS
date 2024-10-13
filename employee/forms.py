from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import LeaveApplication, Empform, UserProfile

class EmpformRegistrationForm(forms.ModelForm):
    class Meta:
        model = Empform
        fields = ['firstname', 'lastname', 'username', 'password', 'email', 'address', 'position', 'photo']
        widgets = {
            'password': forms.PasswordInput(), 
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Empform.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['department', 'start_date', 'end_date', 'leave_type', 'reason']