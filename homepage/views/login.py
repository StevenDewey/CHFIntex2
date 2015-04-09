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

templater = get_renderer('homepage')


@view_function
def process_request(request):
# def loginform(request):
    params = {}

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

    def clean(self):
        user = authenticate(username=self.cleaned_data['username'],
                            password=self.cleaned_data['password'])
        #if user == None:
         #  raise forms.ValidationError('Incorrect username or password')
        return self.cleaned_data
@view_function
def logincheckout(request):
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
            user = authenticate(username=newUserName,
                     password=newPassword)
            login(request, user)
            return templater.render_to_response(request, 'checkout.html', params)
        print("inner")
    print("outer")
    return templater.render_to_response(request, 'checkout.html', params)
@view_function
def loginform(request):
    params = {}
    checkoutLogin = request.urlparams[0]
    print("<<<<<<<<<<<<<<<<<<<")
    print(checkoutLogin)
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            newUserName = form.cleaned_data['username']
            newPassword = form.cleaned_data['password']
             #BYU's is fine for now, but we'll have to do our own Active Directory for INTEX_II
            #try:
            s = Server('www.chf2015.com', port=636, get_info=GET_ALL_INFO)
            c = Connection(s, auto_bind = True, client_strategy = STRATEGY_SYNC, user=newUserName, password=newPassword, authentication=AUTH_SIMPLE)
            search_results = c.search(
                search_base = 'DC=chf2015,DC=local',
                search_filter = '(userPrincipalName='+newUserName+')',
                attributes = ['*']
            )
            ##print(c.response_to_json(search_results)) (objectClass=person)
            user_info = c.response[0]['attributes']
            print(s.info) # display info from the DSE. OID are decoded when recognized by the library
            print(">>>>> print connection results")
            print("------------------------------------")
            print(c.result)
            print(c.response) #it's okay if this is None
            print("++++++++++++++++++++++++++")
            print(user_info['givenName'])
            print(user_info['sn'])
            print(user_info['homePhone'])
            print(user_info['mail'])
            print(user_info['memberOf'][0])
            print(user_info['memberOf'])
            print("<<<<<<<<<<<<<<<<<< connected")
            
            newFirstName = user_info['givenName']
            newLastName = user_info['sn']
            newPhone = user_info['homePhone']
            newEmail = user_info['mail']
            newGroups = user_info['memberOf'][0]
            newGroups = newGroups.split(",")
            for k in newGroups:
                print(k)

            newuser, created = hmod.User.objects.get_or_create(username=newUserName)
            if created:
                newuser.first_name = newFirstName
                newuser.last_name = newLastName
                newuser.email = newEmail
                newuser.phone = newPhone
                newuser.set_password(newPassword)
                newuser.save()
                if "CN=Agent" in newGroups:
                    newuser.groups.add(3)
                elif "CN=Administrators" in newGroups:
                    newuser.groups.add(1)
            print("<<<<<<<<<<<<<<<<<< user")
                #print(newuser)
            #except:
                #pass
            print("<<<<<<<<<<<<<<<<<< would have tried to log in here")
            user = authenticate(username=newUserName,
                     password=newPassword)
            login(request, user)
            #
            #user = authenticate(username=form.cleaned_data['username'],
            #              password=form.cleaned_data['password'])
            #login(request, user)
            if checkoutLogin == "true":
                # return HttpResponse('''
                # <script>
                # window.location.href = '/homepage/checkout/';
                # </script>
                # ''')
                return templater.render_to_response(request, '/homepage/checkout/', params)
            else:
                return HttpResponse('''
                <script>
                    window.location.href = window.location.href;
                </script>
                ''')

    params['form'] = form
    return templater.render_to_response(request, 'login.loginform.html', params)
    # return templater.render_to_response(request, 'login.html', params)

@view_function
def loginformcheckout(request):
    params = {}

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponse('/homepage/checkout/')

    params['form'] = form
    return templater.render_to_response(request, 'login.loginform.html', params)
    # return templater.render_to_response(request, 'login.html', params)




@view_function
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/homepage/')
