import django,os,sys
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


from django.forms import forms
from django.forms import ModelForm
from django import forms
os.environ['DJANGO_SETTINGS_MODULE']="myproject.settings"
django.setup()
from myapp.models import *
from django.http import HttpResponse
from django.shortcuts import render, redirect, loader, get_object_or_404
from django.shortcuts import render_to_response
from django.views import View
from django.views.generic import ListView, DetailView ,CreateView, UpdateView,DeleteView
from django.urls import reverse_lazy

from django.contrib import messages



class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'User Nsme'})
    )

    password = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'First Name '})
    )




class LoginView(View):

    def get(self,request):
        form = LoginForm()
        return render(request,template_name='CustomerLogin.html',context={'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)
                return redirect('myapp:cards',user.id)
            else:
                messages.error(request, 'Invalid Credentials')


        # return render(request,template_name='collegeshtml')





def logout_user(request):
    logout(request)
    return redirect('myapp:login')
