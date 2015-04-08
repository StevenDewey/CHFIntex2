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

    areas = hmod.Area.objects.all().order_by('id')

    params['areas'] = areas

    return templater.render_to_response(request, 'area.html', params)


@view_function
# @permission_required('homepage.change_area', login_url='/homepage/invalid_permissions/')
def edit(request):
    params = {}

    try:
        area = hmod.area.objects.get(id=request.urlparams[0])
    except hmod.area.DoesNotExist:
        return HttpResponseRedirect('/homepage/area/')

    class AddressModelChoiceField(ModelChoiceField):
        def label_from_instance(self, obj):
            return str(obj.id) + " - " + obj.street1 + ", " + obj.street2 + ", " + obj.city + ", " + obj.state + ", " + str(obj.zip_code) + ", " + obj.country

    class areaEditForm(forms.Form):

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

    form = areaEditForm(initial={
    'name': area.name,
    'description': area.description,
    'start_date': area.start_date,
    'end_date': area.end_date,
    'map_file_name': area.map_file_name,
    'venue_name': area.venue_name,
    'address_id': int(area.address_id),
    })
    if request.method == 'POST':
        form = areaEditForm(request.POST)
        if form.is_valid():
            area.name = form.cleaned_data('name')
            area.description = form.cleaned_data('description')
            area.start_date = form.cleaned_data['start_date']
            area.end_date = form.cleaned_data['end_date']
            area.map_file_name = form.cleaned_data['map_file_name']
            area.venue_name = form.cleaned_data['address']
            area.address_id = form.cleaned_data['address_id']
            area.save()
            return HttpResponseRedirect('/homepage/area/')

    params['form'] = form
    return templater.render_to_response(request, 'area.edit.html', params)


@view_function
# @permission_required('homepage.add_area', login_url='/homepage/invalid_permissions/')
def create(request):

    '''Creates a new area'''
    area = hmod.area()
    area.name = 'name'
    area.description = 'description'
    area.start_date = '2015-01-01 07:30:00'
    area.end_date = '2015-01-01 07:30:00'
    area.map_file_name = 'map file name'
    area.venue_name = 'venue'
    area.address_id = hmod.Address.objects.first().id
    area.save()

    return HttpResponseRedirect('/homepage/area.edit/{}/'.format(area.id))

@view_function
# @permission_required('homepage.delete_area', login_url='/homepage/invalid_permissions/')
def delete(request):

    '''delete an area'''
    try:
        area = hmod.area.objects.get(id=request.urlparams[0])
    except hmod.area.DoesNotExist:
        return HttpResponseRedirect('/homepage/area/')

    area.delete()

    return HttpResponseRedirect('/homepage/area/'.format(area.id))
