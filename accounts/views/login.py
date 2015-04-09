from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django.contrib.auth import authenticate, login
from django_mako_plus.controller import view_function
import homepage.models as hmod
from django.contrib import auth
import json
from ldap3 import Server, Connection, AUTH_SIMPLE, STRATEGY_SYNC, STRATEGY_ASYNC_THREADED, SEARCH_SCOPE_WHOLE_SUBTREE, GET_ALL_INFO
from django_mako_plus.controller.router import get_renderer
from django import forms

templater = get_renderer('accounts')

@view_function
def process_request(request):
    return HttpResponseRedirect('/homepage/')

@view_function
def logincheckoutptone(request):
# def loginform(request):
    params = {}

    params['error'] = ""
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/homepage/index/')

    params['form'] = form
    return templater.render_to_response(request, 'login.html', params)

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
                               # , widget=forms.PasswordInput

    # def clean(self):
    #     user = authenticate(username=self.cleaned_data['username'],
    #                         password=self.cleaned_data['password'])
        #if user == None:
         #  raise forms.ValidationError('Incorrect username or password')
        # return self.cleaned_data
@view_function
def logincheckoutpttwo(request):
    form = LoginForm()
    params = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            newUserName = form.cleaned_data['username']
            newPassword = form.cleaned_data['password']
             #BYU's is fine for now, but we'll have to do our own Active Directory for INTEX_II
            try:
                s = Server('www.chf2015.com', port=636, get_info=GET_ALL_INFO)
                c = Connection(s, auto_bind = True, client_strategy = STRATEGY_SYNC, user=newUserName, password=newPassword, authentication=AUTH_SIMPLE)
                #print(s.info)
                print("<<<<<<<<<<<<<<<<<< connected")
                newuser, created = hmod.User.objects.get_or_create(username=newUserName)
                if created:
                   
                    newuser.set_password(newPassword)
                    newuser.save()
                print("<<<<<<<<<<<<<<<<<< user")
                #print(newuser)
            except:
                pass
            try:
                user = authenticate(username=newUserName,
                         password=newPassword)
                login(request, user)
            except:
                params['error'] = "<p class='bg-danger'>Incorrect Username or Password</p>"
                params['form'] = form
                return templater.render_to_response(request, 'login.html', params)
        else:
            params['error'] = ""
            params['form'] = form
            return templater.render_to_response(request, 'login.html', params)

        print("inner")
    print("outer")
    return HttpResponseRedirect('/homepage/checkout')