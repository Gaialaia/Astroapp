from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from .forms import UserRegistrationForm

def register(request):

    if request.user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        reg_form = UserRegistrationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            login(request, user)
            messages.success(request, f"New account created: {user.username}")
            return redirect('/')
        else:
            for error in list(reg_form.errors.values()):
                messages.error(request,'')


    else:
        reg_form = UserRegistrationForm()

    return render(request,"register.html",{"reg_form":reg_form})