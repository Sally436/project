from django import forms
from .models import Profile, Processor_Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group


class CreatUserForm(UserCreationForm):
    email = forms.EmailField()
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'groups')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'phone', 'image']

class ProcessorProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Processor_Profile
        fields = ['address', 'phone', 'FDA_Number', 'reports', 'image']
