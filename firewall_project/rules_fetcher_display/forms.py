from django import forms 
from django.contrib.auth.models import User
from rules_fetcher_display.models import UserProfileInfo


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    username = forms.CharField(max_length=11)
    email = forms.EmailField()

    class Meta():
        model = UserProfileInfo
        fields = ('username','email','password')
    