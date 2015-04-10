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

    mto_products = hmod.ProductSpecification.objects.filter(type="mto").order_by('vendor')

    params['mto_products'] = mto_products

    return templater.render_to_response(request, 'mto_product.html', params)

@view_function
def admin(request):
    params = {}

    mto_products = hmod.ProductSpecification.objects.filter(type="mto").order_by('id')

    params['mto_products'] = mto_products

    return templater.render_to_response(request, 'mto_product.admin.html', params)

@view_function
def delete(request):

    '''delete an event'''
    try:
        mto_products = hmod.ProductSpecification.objects.get(id=request.urlparams[0])
    except hmod.Event.DoesNotExist:
        return HttpResponseRedirect('/homepage/mto_product.admin/')

    mto_products.delete()

    return HttpResponseRedirect('/homepage/mto_product.admin/'.format(mto_products.id))

@view_function
def create(request):
    params = {}

    class MTOEditForm(forms.Form):

        name = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
        description = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        manufacturer = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        average_cost = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
        order_form_name = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        production_time = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        category_id = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    form = MTOEditForm()

    '''Creates a new event'''
    if request.method == 'POST':
        form = MTOEditForm(request.POST)
        if form.is_valid():
            mto = hmod.ProductSpecification()
            mto.type = "mto"
            mto.name = form.cleaned_data['name']
            mto.price = form.cleaned_data['price']
            mto.description = form.cleaned_data['description']
            mto.manufacturer = form.cleaned_data['manufacturer']
            mto.average_cost = form.cleaned_data['average_cost']
            mto.category_id = form.cleaned_data['category_id']
            mto.order_form_name = form.cleaned_data['order_form_name']
            mto.production_time = form.cleaned_data['production_time']
            mto.photo_id = 22
            mto.vendor_id = 3
            mto.area_id = 2
            mto.sku = 2
            mto.save()
            return HttpResponseRedirect('/homepage/mto_product.admin/')
        else:
            params['error'] = "<p class='bg-danger'>All fields are required</p>"
            params['form'] = form
            return templater.render_to_response(request, 'mto_product.edit.html', params)

    params['error'] = ""
    params['form'] = form
    return templater.render_to_response(request, 'mto_product.edit.html', params)

@view_function
def edit(request):
    params = {}

    try:
        mto = hmod.ProductSpecification.objects.get(id=request.urlparams[0])
    except hmod.ProductSpecification.DoesNotExist:
        return HttpResponseRedirect('/homepage/mto_product.admin/')

    class MTOEditForm(forms.Form):

        name = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
        description = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        manufacturer = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        average_cost = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
        sku = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        order_form_name = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        production_time = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))
        category_id = forms.CharField(required=True, max_length=1000, widget=forms.TextInput(attrs={'class': 'form-control'}))

    form = MTOEditForm(initial={
    'name': mto.name,
    'price': mto.price,
    'description': mto.description,
    'manufacturer': mto.manufacturer,
    'average_cost': mto.average_cost,
    'sku': mto.sku,
    'order_form_name': mto.order_form_name,
    'production_time': mto.production_time,
    'category_id': mto.category_id,
    })
    if request.method == 'POST':
        form = MTOEditForm(request.POST)
        if form.is_valid():
            mto.name = form.cleaned_data['name']
            mto.price = form.cleaned_data['price']
            mto.description = form.cleaned_data['description']
            mto.manufacturer = form.cleaned_data['manufacturer']
            mto.average_cost = form.cleaned_data['average_cost']
            mto.sku = form.cleaned_data['sku']
            mto.order_form_name = form.cleaned_data['order_form_name']
            mto.production_time = form.cleaned_data['production_time']
            mto.category_id = form.cleaned_data['category_id']
            mto.save()
            return HttpResponseRedirect('/homepage/mto_product.admin/')
        else:
            params['error'] = "<p class='bg-danger'>All fields are required</p>"
            params['form'] = form
            return templater.render_to_response(request, 'mto_product.edit.html', params)

    params['error'] = ""
    params['form'] = form
    return templater.render_to_response(request, 'mto_product.edit.html', params)
