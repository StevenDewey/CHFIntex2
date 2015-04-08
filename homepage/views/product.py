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
@permission_required('homepage.change_product', login_url='/homepage/invalid_permissions/')
def edit(request):
    params = {}

    try:
        product = hmod.Product.objects.get(id=request.urlparams[0])
    except hmod.Product.DoesNotExist:
        return HttpResponseRedirect('/homepage/product/')

    class ProductEditForm(forms.Form):
        name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        description = forms.CharField(required=True, max_length=500, widget=forms.TextInput(attrs={'class': 'form-control'}))
        category = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        price = forms.DecimalField(max_digits= 10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))

    form = ProductEditForm(initial={
    'name': product.name,
    'description': product.description,
    'category': product.category,
    'price': product.price,
    })
    if request.method == 'POST':
        form = ProductEditForm(request.POST)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.description = form.cleaned_data['description']
            product.category = form.cleaned_data['category']
            product.price = form.cleaned_data['price']
            product.save()
            return HttpResponseRedirect('/homepage/product/')

    params['form'] = form
    return templater.render_to_response(request, 'product.edit.html', params)


@view_function
@permission_required('homepage.add_product', login_url='/homepage/invalid_permissions/')
def create(request):

    '''Creates a new product'''
    product = hmod.Product()
    product.name = 'name'
    product.description = 'description'
    product.category = 'category'
    product.price = '00.00'
    product.save()

    return HttpResponseRedirect('/homepage/product.edit/{}/'.format(product.id))

@view_function
@permission_required('homepage.delete_item', login_url='/homepage/invalid_permissions/')
def delete(request):

    '''delete an product'''
    try:
        product = hmod.Product.objects.get(id=request.urlparams[0])
    except hmod.Product.DoesNotExist:
        return HttpResponseRedirect('/homepage/product/')

    product.delete()

    return HttpResponseRedirect('/homepage/product/'.format(product.id))
