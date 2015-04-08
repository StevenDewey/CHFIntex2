from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django_mako_plus.controller.router import get_renderer
from django_mako_plus.controller import view_function
import datetime
from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
import homepage.models as hmod

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
        user.address_id = address.id
        user.save()

    params['user'] = user
    return templater.render_to_response(request, 'account.html', params)
