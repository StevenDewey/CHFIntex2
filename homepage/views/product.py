from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django_mako_plus.controller.router import get_renderer
from django_mako_plus.controller import view_function
import homepage.models as hmod
from django import forms
from django.contrib.auth.decorators import permission_required


templater = get_renderer('homepage')


@view_function
def process_request(request):
    params = {}

    products = hmod.SerializedProduct.objects.filter(for_sale = True).order_by('id')

    params['products'] = products

    return templater.render_to_response(request, 'product.html', params)


@view_function
def filter(request):
    params = {}
    searchTerm = request.urlparams[0]
    products = hmod.ProductSpecification.objects.filter(name__icontains=searchTerm)
    print(">>>>>>>>>>>>>>")
    print(searchTerm)
    print(products)
    params['products'] = products
    return templater.render_to_response(request, 'searchProducts.html', params)




@view_function
def admin(request):
    params = {}

    products = hmod.SerializedProduct.objects.filter(for_sale = True).order_by('id')
    params['products'] = products

    return templater.render_to_response(request, 'product.admin.html', params)

@view_function
# @permission_required('homepage.change_product', login_url='/homepage/invalid_permissions/')
def edit(request):
    params = {}

    try:
        product = hmod.RentalProduct.objects.get(id=request.urlparams[0])
    except hmod.RentalProduct.DoesNotExist:
        return HttpResponseRedirect('/homepage/product.admin/')

    class productEditForm(forms.Form):
        Name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
        Description = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        PriceDay = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
        ReplacementPrice = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
        # ImagePath = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    form = productEditForm(initial={
        'Name': product.product_specification.name,
        'Description': product.product_specification.description,
        'PriceDay': product.price_per_day,
        'ReplacementPrice': product.replacement_price,
        # 'ImagePath': product.product_specification.photo.image,
    })
    if request.method == 'POST':
        form = productEditForm(request.POST)
        if form.is_valid():
            product.product_specification.name = form.cleaned_data['Name']
            product.product_specification.description = form.cleaned_data['Description']
            product.price_per_day = form.cleaned_data['PriceDay']
            product.replacement_price = form.cleaned_data['ReplacementPrice']
            # product.product_specification.photo.image = form.cleaned_data['ImagePath']
            product.save()
            return HttpResponseRedirect('/homepage/product.admin/')

    params['form'] = form
    return templater.render_to_response(request, 'product.edit.html', params)


@view_function
# @permission_required('homepage.add_product', login_url='/homepage/invalid_permissions/')
def create(request):
    params = {}

    class productEditForm(forms.Form):
        Name = forms.CharField(required=True, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
        Description = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        Price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
        # ReplacementPrice = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
        # ImagePath = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    '''Creates a new product'''
    form = productEditForm()

    if request.method == 'POST':
        form = productEditForm(request.POST)
        if form.is_valid():

            ProdSpec = hmod.ProductSpecification()
            ProdSpec.description = form.cleaned_data['Description']
            ProdSpec.name = form.cleaned_data['Name']
            ProdSpec.type = "product"
            ProdSpec.category_id = 1
            ProdSpec.save()
            ProdSpec.photo = hmod.Photograph.objects.get(id=22)
            ProdSpec.Sku = ProdSpec.id
            ProdSpec.save()

            product = hmod.SerializedProduct()
            product.cost = 10.00
            product.quantity_on_hand = 1
            product.shelf_location = 2
            product.product_specification = ProdSpec
            product.price_per_day = 22.22
            product.replacement_price = 22.22
            product.times_rented = 0
            product.price = form.cleaned_data['Price']
            product.save()

            return HttpResponseRedirect('/homepage/product.admin/')

    params['form'] = form
    return templater.render_to_response(request, 'product.edit.html', params)

@view_function
# @permission_required('homepage.delete_product', login_url='/homepage/invalid_permissions/')
def delete(request):

    # delete an product
    try:
        product = hmod.SerializedProduct.objects.get(id=request.urlparams[0])
    except hmod.SerializedProduct.DoesNotExist:
        return HttpResponseRedirect('/homepage/product.admin/')

    product.delete()

