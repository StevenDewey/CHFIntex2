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

    items = hmod.Item.objects.all().order_by('id')

    params['items'] = items

    return templater.render_to_response(request, 'item.html', params)


@view_function
@permission_required('homepage.change_item', login_url='/homepage/invalid_permissions/')
def edit(request):
    params = {}

    try:
        item = hmod.Item.objects.get(id=request.urlparams[0])
    except hmod.Item.DoesNotExist:
        return HttpResponseRedirect('/homepage/item/')

    class PersonModelChoiceField(ModelChoiceField):
        def label_from_instance(self, obj):
            return str(obj.id) + " - " + obj.given_name

    class ItemEditForm(forms.Form):
        name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        description = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        value = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        standard_rental_price = forms.DecimalField(required=True, max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
        legal_entity_id = PersonModelChoiceField(
            queryset= hmod.LegalEntity.objects.all(), empty_label=None,
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    form = ItemEditForm(initial={
        'name': item.name,
        'description': item.description,
        'value': item.value,
        'standard_rental_price': item.standard_rental_price,
        'legal_entity_id': int(item.legal_entity_id),
    })
    if request.method == 'POST':
        form = ItemEditForm(request.POST)
        if form.is_valid():
            item.name = form.cleaned_data['name']
            item.description = form.cleaned_data['description']
            item.value = form.cleaned_data['value']
            item.standard_rental_price = form.cleaned_data['standard_rental_price']
            item.legal_entity_id = form.cleaned_data['legal_entity_id']
            item.save()
            return HttpResponseRedirect('/homepage/item/')

    params['form'] = form
    return templater.render_to_response(request, 'item.edit.html', params)


@view_function
@permission_required('homepage.add_item', login_url='/homepage/invalid_permissions/')
def create(request):

    '''Creates a new item'''
    item = hmod.Item()
    item.name = 'name'
    item.description = 'description'
    item.value = 00.00
    item.standard_rental_price = 00.00
    item.legal_entity_id = hmod.LegalEntity.objects.first().id
    item.save()

    return HttpResponseRedirect('/homepage/item.edit/{}/'.format(item.id))

@view_function
@permission_required('homepage.delete_item', login_url='/homepage/invalid_permissions/')
def delete(request):

    '''delete an item'''
    try:
        item = hmod.Item.objects.get(id=request.urlparams[0])
    except hmod.Item.DoesNotExist:
        return HttpResponseRedirect('/homepage/item/')

    item.delete()

    return HttpResponseRedirect('/homepage/item/'.format(item.id))
