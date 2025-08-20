from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, logout, authenticate
from .forms import UserRegistrationForm
from django.contrib.auth.forms import AuthenticationForm

def register(request):

    if request.user.is_authenticated:
        return redirect("showed chart")

    if request.method == 'POST':
        reg_form = UserRegistrationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            login(request, user)
            messages.success(request, f"New account created: {user.username}")
            return redirect('showed chart')
        else:
            for error in list(reg_form.errors.values()):
                messages.error(request, error)


    else:
        reg_form = UserRegistrationForm()

    return render(request,"register.html",{"reg_form":reg_form})


@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, 'Logged out')
    return redirect('showed chart')


def custom_login(request):
    if request.user.is_authenticated:
        return redirect('showed chart')


    if request.method == 'POST':
        auth_form = AuthenticationForm(request=request, data=request.POST)
        if auth_form.is_valid():
            user = authenticate(
                username=auth_form.cleaned_data['username'],
                password=auth_form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, f"{user.username}You have been logged in")
                return redirect('showed chart')

        else:
            for error in list(auth_form.errors.values()):
                messages.error(request, error)

    auth_form = AuthenticationForm()

    return render(request,'login.html', {'auth_form': auth_form})
