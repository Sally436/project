from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from .forms import CreatUserForm, UserUpdateForm, ProfileUpdateForm, ProcessorProfileUpdateForm
from django.contrib.auth import login

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CreatUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            
            # Assign the selected group to the user
            group = form.cleaned_data['groups']
            group.user_set.add(user)
            return redirect('user-login')
    else:
        form = CreatUserForm()
    context = {
        'form': form,
    }
    return render(request, 'users/register.html', context)

def profile(request):
    return render(request, 'users/profile.html')


def profile_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        processor_profile_form = ProcessorProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        elif user_form.is_valid() and processor_profile_form.is_valid():
            user_form.save()
            processor_profile_form.save()
        return redirect('user-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        processor_profile_form = ProcessorProfileUpdateForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'processor_profile_form': processor_profile_form,
    }
    return render(request, 'users/profile_update.html', context)