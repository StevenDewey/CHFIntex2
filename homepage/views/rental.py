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
    request.session['ptype'] = "rental"

    return templater.render_to_response(request, 'rental.html', params)

@view_function
def admin(request):
    params = {}

    rentals = hmod.RentalProduct.objects.all()
    params['rentals'] = rentals

    return templater.render_to_response(request, 'rental.admin.html', params)

@view_function
@permission_required('homepage.change_rentalitem', login_url='/homepage/invalid_permissions/')
def edit(request):
    params = {}

    try:
        rental = hmod.RentalProduct.objects.get(id=request.urlparams[0])
    except hmod.RentalProduct.DoesNotExist:
        return HttpResponseRedirect('/homepage/rental.admin/')

    class RentalEditForm(forms.Form):
        Name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
        Description = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        PriceDay = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
        ReplacementPrice = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
        # ImagePath = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    form = RentalEditForm(initial={
        'Name': rental.product_specification.name,
        'Description': rental.product_specification.description,
        'PriceDay': rental.price_per_day,
        'ReplacementPrice': rental.replacement_price,
        # 'ImagePath': rental.product_specification.photo.image,
    })
    if request.method == 'POST':
        form = RentalEditForm(request.POST)
        if form.is_valid():
            rental.product_specification.name = form.cleaned_data['Name']
            rental.product_specification.description = form.cleaned_data['Description']
            rental.price_per_day = form.cleaned_data['PriceDay']
            rental.replacement_price = form.cleaned_data['ReplacementPrice']
            # rental.product_specification.photo.image = form.cleaned_data['ImagePath']
            rental.product_specification.save()
            rental.save()
            return HttpResponseRedirect('/homepage/rental.admin/')

    params['form'] = form
    return templater.render_to_response(request, 'rental.edit.html', params)


@view_function
@permission_required('homepage.add_rentalitem', login_url='/homepage/invalid_permissions/')
def create(request):
    params = {}

    class RentalEditForm(forms.Form):
        Name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
        Description = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        PriceDay = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
        ReplacementPrice = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
        # ImagePath = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    '''Creates a new rental'''
    form = RentalEditForm()

    if request.method == 'POST':
        form = RentalEditForm(request.POST)
        if form.is_valid():

            ProdSpec = hmod.ProductSpecification()
            ProdSpec.description = form.cleaned_data['Description']
            ProdSpec.name = form.cleaned_data['Name']
            ProdSpec.type = "rental"
            ProdSpec.category_id = 1
            ProdSpec.save()
            ProdSpec.photo = hmod.Photograph.objects.get(id=22)
            ProdSpec.Sku = ProdSpec.id
            ProdSpec.save()

            rental = hmod.RentalProduct()
            rental.cost = 10.00
            rental.quantity_on_hand = 1
            rental.shelf_location = 2
            rental.product_specification = ProdSpec
            rental.times_rented = 0
            rental.for_sale = False
            rental.price_per_day = form.cleaned_data['PriceDay']
            rental.replacement_price = form.cleaned_data['ReplacementPrice']
            rental.save()

            return HttpResponseRedirect('/homepage/rental.admin/')

    params['form'] = form
    return templater.render_to_response(request, 'rental.edit.html', params)

@view_function
@permission_required('homepage.delete_rentalitem', login_url='/homepage/invalid_permissions/')
def delete(request):

    # delete an rental
    try:
        rental = hmod.RentalProduct.objects.get(id=request.urlparams[0])
    except hmod.RentalProduct.DoesNotExist:
        return HttpResponseRedirect('/homepage/rental.admin/')

    rental.delete()

    return HttpResponseRedirect('/homepage/rental.admin/')
