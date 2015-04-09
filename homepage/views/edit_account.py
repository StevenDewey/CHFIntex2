from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django.contrib.auth import authenticate, login
from django_mako_plus.controller import view_function
import homepage.models as hmod
from django_mako_plus.controller.router import get_renderer
from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django import forms

templater = get_renderer('homepage')


@view_function
def process_request(request):
    params = {}

    try:
        user = hmod.User.objects.get(id=request.urlparams[0])
    except hmod.User.DoesNotExist:
        return HttpResponseRedirect('/homepage/')

    if request.urlparams[1] != "None":
        try:
            address = hmod.Address.objects.get(id=request.urlparams[1])
        except hmod.Address.DoesNotExist:
            return HttpResponseRedirect('/homepage/')
    else:
        address = hmod.Address()
        address.street1 = ''
        address.street2 = ''
        address.city = ''
        address.state = ''
        address.zip_code = ''
        address.country = ''
        address.save()


    class userEditForm(forms.Form):
        first_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        last_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        email = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        phone = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        street1 = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        street2 = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        city = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        state = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        zip_code = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        country = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    form = userEditForm(initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
        'street1': address.street1,
        'street2': address.street2,
        'city': address.city,
        'state': address.state,
        'zip_code': address.zip_code,
        'country': address.country,

    })

    if request.method == 'POST':
        form = userEditForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            address.street1 = form.cleaned_data['street1']
            address.street2 = form.cleaned_data['street2']
            address.city = form.cleaned_data['city']
            address.state = form.cleaned_data['state']
            address.zip_code = form.cleaned_data['zip_code']
            address.country = form.cleaned_data['country']

            address.save()

            user.address_id = address.id

            user.save()
            return HttpResponseRedirect('/homepage/account/{}/'.format(user.id) + '{}/'.format(user.address_id))
        else:
            params['error'] = "<p class='bg-danger'>first_name, last_name, and email are required fields</p>"
            params['user'] = user
            params['form'] = form
            return templater.render_to_response(request, 'edit_account.html', params)

    params['error'] = ""
    params['user'] = user
    params['form'] = form
    return templater.render_to_response(request, 'edit_account.html', params)




@view_function
def password(request):
    params = {}

    try:
        user = hmod.User.objects.get(id=request.urlparams[0])
    except hmod.User.DoesNotExist:
        return HttpResponseRedirect('/homepage/')


    class userEditForm(forms.Form):
        new_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
        confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    form = userEditForm(initial={
        'new_password': user.password,
        'confirm_password': user.password,
    })

    they_dont_match=False

    if request.method == 'POST':
        form = userEditForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['new_password'] == form.cleaned_data['confirm_password']:
                user.set_password(form.cleaned_data['new_password'])

                user.save()

                userauth = authenticate(username=user.username,
                                    password=form.cleaned_data['new_password'])
                login(request, userauth)

                return HttpResponseRedirect('/homepage/account/{}/'.format(user.id) + '{}/'.format(user.address_id))
            else:
                they_dont_match = True
                pass

    if they_dont_match:
        params['error'] = "<p class='bg-danger'>Passwords don't match</p>"
    else:
        params['error'] = ""
    params['user'] = user
    params['form'] = form
    return templater.render_to_response(request, 'edit_account.password.html', params)
