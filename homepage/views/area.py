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
        area = hmod.Area.objects.get(id=request.urlparams[0])
    except hmod.Area.DoesNotExist:
        return HttpResponseRedirect('/homepage/area.admin/')

    class areaEditForm(forms.Form):

        name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        description = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        place_number = forms.CharField(required=False, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        coordinator_id = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        supervisor_id = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        event_id = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))

    form = areaEditForm(initial={
    'name': area.name,
    'description': area.description,
    'place_number': area.place_number,
    'coordinator_id': area.coordinator_id,
    'supervisor_id': area.supervisor_id,
    'event_id': area.event_id,
    })
    if request.method == 'POST':
        form = areaEditForm(request.POST)
        if form.is_valid():
            area.name = form.cleaned_data['name']
            area.description = form.cleaned_data['description']
            area.place_number = form.cleaned_data['place_number']
            area.coordinator_id = form.cleaned_data['coordinator_id']
            area.supervisor_id = form.cleaned_data['supervisor_id']
            area.event_id = form.cleaned_data['event_id']
            area.save()
            return HttpResponseRedirect('/homepage/area.admin/')

    params['form'] = form
    return templater.render_to_response(request, 'area.edit.html', params)


@view_function
# @permission_required('homepage.add_area', login_url='/homepage/invalid_permissions/')
def create(request):

    '''Creates a new area'''
    area = hmod.Area()
    area.name = 'name'
    area.description = 'description'
    area.place_number = 1
    area.coordinator_id = 1
    area.supervisor_id = 1
    area.event_id = 1
    area.photo_id = 22
    area.save()

    return HttpResponseRedirect('/homepage/area.edit/{}/'.format(area.id))

@view_function
# @permission_required('homepage.delete_area', login_url='/homepage/invalid_permissions/')
def delete(request):

    '''delete an area'''
    try:
        area = hmod.Area.objects.get(id=request.urlparams[0])
    except hmod.Area.DoesNotExist:
        return HttpResponseRedirect('/homepage/area.admin/')

    area.delete()

    return HttpResponseRedirect('/homepage/area.admin/'.format(area.id))

@view_function
def admin(request):
    params = {}

    areas= hmod.Area.objects.all().order_by('id')

    params['areas'] = areas

    return templater.render_to_response(request, 'area.admin.html', params)