from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django.forms import ModelChoiceField
from django_mako_plus.controller.router import get_renderer
from django_mako_plus.controller import view_function
import homepage.models as hmod
from django import forms
from django.contrib.auth.decorators import permission_required

templater = get_renderer('homepage')


@view_function
def process_request(request):
    params = {}

    events = hmod.Event.objects.all().order_by('id')

    params['events'] = events

    return templater.render_to_response(request, 'event.html', params)


@view_function
# @permission_required('homepage.change_event', login_url='/homepage/invalid_permissions/')
def edit(request):
    params = {}

    try:
        event = hmod.Event.objects.get(id=request.urlparams[0])
    except hmod.Event.DoesNotExist:
        return HttpResponseRedirect('/homepage/event/')

    class AddressModelChoiceField(ModelChoiceField):
        def label_from_instance(self, obj):
            return str(obj.id) + " - " + obj.street1 + ", " + obj.street2 + ", " + obj.city + ", " + obj.state + ", " + str(obj.zip_code) + ", " + obj.country

    class EventEditForm(forms.Form):

        name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        description = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        start_date = forms.DateTimeField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        end_date = forms.DateTimeField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        map_file_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        venue_name = forms.CharField(required=True, max_length= 100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        address_id = AddressModelChoiceField(
            queryset=hmod.Address.objects.all(),
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    form = EventEditForm(initial={
    'name': event.name,
    'description': event.description,
    'start_date': event.start_date,
    'end_date': event.end_date,
    'map_file_name': event.map_file_name,
    'venue_name': event.venue_name,
    'address_id': int(event.address_id),
    })
    if request.method == 'POST':
        form = EventEditForm(request.POST)
        if form.is_valid():
            event.name = form.cleaned_data('name')
            event.description = form.cleaned_data('description')
            event.start_date = form.cleaned_data['start_date']
            event.end_date = form.cleaned_data['end_date']
            event.map_file_name = form.cleaned_data['map_file_name']
            event.venue_name = form.cleaned_data['address']
            event.address_id = form.cleaned_data['address_id']
            event.save()
            return HttpResponseRedirect('/homepage/event/')

    params['form'] = form
    return templater.render_to_response(request, 'event.edit.html', params)


@view_function
# @permission_required('homepage.add_event', login_url='/homepage/invalid_permissions/')
def create(request):

    '''Creates a new event'''
    event = hmod.Event()
    event.name = 'name'
    event.description = 'description'
    event.start_date = '2015-01-01 07:30:00'
    event.end_date = '2015-01-01 07:30:00'
    event.map_file_name = 'map file name'
    event.venue_name = 'venue'
    event.address_id = hmod.Address.objects.first().id
    event.save()

    return HttpResponseRedirect('/homepage/event.edit/{}/'.format(event.id))

@view_function
# @permission_required('homepage.delete_event', login_url='/homepage/invalid_permissions/')
def delete(request):

    '''delete an event'''
    try:
        event = hmod.Event.objects.get(id=request.urlparams[0])
    except hmod.Event.DoesNotExist:
        return HttpResponseRedirect('/homepage/event/')

    event.delete()

    return HttpResponseRedirect('/homepage/event/'.format(event.id))
