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
    print(">>>>>>>>>>>>>>")
    print(mto_products)

    return templater.render_to_response(request, 'mto_product.html', params)

