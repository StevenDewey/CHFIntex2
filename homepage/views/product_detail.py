from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django_mako_plus.controller.router import get_renderer
from django_mako_plus.controller import view_function
from django.contrib.auth.decorators import permission_required
import homepage.models as hmod
from django import forms

templater = get_renderer('homepage')

@view_function
def process_request(request):
    params = {}
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>> #1")
    product = hmod.SerializedProduct.objects.get(id=request.urlparams[0])
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>> #2")
    params['product'] = product
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>> #3")
    return templater.render_to_response(request, 'product_detail.html', params)

# @view_function
# @permission_required('homepage.change_product', login_url='/homepage/invalid_permissions/')
# def edit(request):
#     params = {}
#
#     try:
#         product = hmod.Product.objects.get(id=request.urlparams[0])
#     except hmod.Product.DoesNotExist:
#         return HttpResponseRedirect('/homepage/product/')
#
#     class ProductEditForm(forms.Form):
#         id = forms.CharField(required=True, max_length=100)
#         name = forms.CharField(required=True,  max_length=100)
#         description = forms.CharField(required=True, max_length=100)
#         category = forms.CharField(required=True, max_length=100)
#         current_price = forms.DecimalField(required=True, max_digits= 10, decimal_places=2)
#
#     form = ProductEditForm(initial={
#     'id': product.id,
#     'name': product.name,
#     'description': product.description,
#     'category': product.category,
#     'current_price': product.current_price,
#     })
#     if request.method == 'POST':
#         form = ProductEditForm(request.POST)
#         if form.is_valid():
#             product.id = form.cleaned_data['id']
#             product.name = form.cleaned_data['name']
#             product.description = form.cleaned_data['description']
#             product.category = form.cleaned_data['category']
#             product.current_price = form.cleaned_data['current_price']
#             product.save()
#             return HttpResponseRedirect('/homepage/product/')
#
#     params['form'] = form
#     return templater.render_to_response(request, 'product.edit.html', params)