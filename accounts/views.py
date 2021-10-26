from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.views import generic
from .forms import SignUpForm


#class SignUpView(generic.CreateView):
    #form_class = UserCreationForm
    #success_url = reverse_lazy('login')
    #template_name = 'registration/signup.html'

def signup(response):
    if response.method == "POST":
        form = SignUpForm(response.POST)
        if form.is_valid():
            form.save()
        
        return redirect("/login")

    else:
        form = SignUpForm()
    return render(response, "registration/signup.html", {"form": form})
