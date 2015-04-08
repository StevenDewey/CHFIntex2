from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django_mako_plus.controller.router import get_renderer
from django_mako_plus.controller import view_function
import homepage.models as hmod
from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.decorators import permission_required

templater = get_renderer('homepage')


@view_function
def process_request(request):
    params = {}

    rentals = hmod.RentalProduct.objects.all()
    params['rentals'] = rentals

    return templater.render_to_response(request, 'rental.html', params)


@view_function
@permission_required('homepage.change_rental', login_url='/homepage/invalid_permissions/')
def edit(request):
    params = {}

    try:
        rental = hmod.Rental.objects.get(id=request.urlparams[0])
    except hmod.Rental.DoesNotExist:
        return HttpResponseRedirect('/homepage/rental/')

    class PersonModelChoiceField(ModelChoiceField):
        def label_from_instance(self, obj):
            return str(obj.id) + " - " + obj.given_name + " " + obj.family_name

    class OrganizationModelChoiceField(ModelChoiceField):
        def label_from_instance(self, obj):
            return str(obj.id) + " - " + obj.given_name + " - " + obj.organization_type

    class RentalEditForm(forms.Form):
        rental_time = forms.DateTimeField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        discount_percent = forms.DecimalField(max_digits=10, decimal_places=4, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        Organization_id = OrganizationModelChoiceField(
            queryset=hmod.Organization.objects.all(), empty_label=None,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        Person_id = PersonModelChoiceField(
            queryset=hmod.Person.objects.all(), empty_label=None,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        Agent_id = PersonModelChoiceField(
            queryset=hmod.Agent.objects.all(), empty_label=None,
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    form = RentalEditForm(initial={
        'rental_time': rental.rental_time,
        'discount_percent': rental.discount_percent,
        'Organization_id': rental.Organization_id,
        'Person_id': rental.Person_id,
        'Agent_id': rental.Agent_id,
    })
    if request.method == 'POST':
        form = RentalEditForm(request.POST)
        if form.is_valid():
            rental.rental_time = form.cleaned_data['rental_time']
            rental.discount_percent = form.cleaned_data['discount_percent']
            rental.Organization_id = form.cleaned_data['Organization_id']
            rental.Person_id = form.cleaned_data['Person_id']
            rental.Agent_id = form.cleaned_data['Agent_id']
            rental.save()
            return HttpResponseRedirect('/homepage/rental/')

    params['form'] = form
    return templater.render_to_response(request, 'rental.edit.html', params)


@view_function
@permission_required('homepage.add_rental', login_url='/homepage/invalid_permissions/')
def create(request):

    '''Creates a new rental'''
    rental = hmod.Rental()
    rental.rental_time = '2015-01-01 06:00:00'
    rental.discount_percent = 00.10
    # try:
    #     Organization = hmod.Organization.objects.first()
    # except Organization.DoesNotExist:
    #     return HttpResponseRedirect('/homepage/organization.create/')
    rental.Organization_id = hmod.Organization.objects.first().id
    rental.Person_id = hmod.Person.objects.first().id
    rental.Agent_id = hmod.Agent.objects.first().id
    rental.save()

    return HttpResponseRedirect('/homepage/rental.edit/{}/'.format(rental.id))

@view_function
@permission_required('homepage.delete_rental', login_url='/homepage/invalid_permissions/')
def delete(request):

    '''delete an rental'''
    try:
        rental = hmod.Rental.objects.get(id=request.urlparams[0])
    except hmod.Rental.DoesNotExist:
        return HttpResponseRedirect('/homepage/rental/')

    rental.delete()

    return HttpResponseRedirect('/homepage/rental/'.format(rental.id))
