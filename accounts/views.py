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

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            login(request,user)
            return redirect('settings')

    else:
        form = SignUpForm()
    
    my_context = {
        "form": form,
    }

    return render(request, "registration/signup.html", my_context)
