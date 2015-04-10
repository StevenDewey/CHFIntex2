from django.conf import settings
from django.http import HttpResponse
from django_mako_plus.controller import view_function
from .. import dmp_render, dmp_render_to_response
import homepage.models as hmod

global ptype
ptype = "product"

@view_function
def process_request(request):
    params = {}

    request.session['ptype'] = "product"

    if 'shopCartDict' not in request.session:
        request.session['shopCartDict'] = {}
    # print(request.session['shopping_cart'])
    # fav_color = request.session.pop('shopping_cart')

    # pid = request.urlparams[0]
    # qty = request.urlparams[1]
    #
    # # print(request.session['shopping_cart'])
    # if pid in request.session['shopCartDict']:
    #     request.session['shopCartDict'][pid] += int(qty)
    # else:
    #     request.session['shopCartDict'][pid] = int(qty)
    # request.session.modified = True
    # print(request.session['shopCartDict'])
    productDictionary = {}
    ##quantity = []

    orderTotal = 0
    for k,v in request.session['shopCartDict'].items():
        productObject = hmod.SerializedProduct.objects.get(id=k)
        productDictionary[productObject] = int(v)
        orderTotal += productObject.product_specification.price * v

    params['orderTotal'] = orderTotal
    params['products'] = productDictionary
    ##params['quantities'] = quantity
    print(request.session['shopCartDict'])
    ##request.session.flush()
    return dmp_render_to_response(request, 'shoppingCart.html', params)


@view_function
def add(request):
    ##request.session.flush()
    ##print(request.session['shopCartDict'])
    params = {}

    request.session['ptype'] = "product"

    if 'shopCartDict' not in request.session:
        request.session['shopCartDict'] = {}
    # print(request.session['shopping_cart'])
    # fav_color = request.session.pop('shopping_cart')

    pid = request.urlparams[0]
    qty = request.urlparams[1]

    # print(request.session['shopping_cart'])
    if pid in request.session['shopCartDict']:
        request.session['shopCartDict'][pid] += int(qty)
    else:
        request.session['shopCartDict'][pid] = int(qty)
    request.session.modified = True
    print(request.session['shopCartDict'])
    productDictionary = {}
    ##quantity = []

    orderTotal = 0
    for k,v in request.session['shopCartDict'].items():
        productObject = hmod.SerializedProduct.objects.get(id=k)
        productDictionary[productObject] = int(v)
        orderTotal += productObject.product_specification.price * v

    params['orderTotal'] = orderTotal
    params['products'] = productDictionary
    ##params['quantities'] = quantity
    print(request.session['shopCartDict'])
    ##request.session.flush()
    return dmp_render_to_response(request, 'shoppingCart.html', params)

@view_function
def updateQuantity(request):
    params = {}

    pid = request.urlparams[0]
    qty = request.urlparams[1]

    # # print(request.session['shopping_cart'])
    # if pid in request.session['shopCartDict']:
    #     request.session['shopCartDict'][pid] += int(qty)
    # else:
    request.session['shopCartDict'][pid] = int(qty)
    request.session.modified = True
    print(request.session['shopCartDict'])
    # productDictionary = {}
    # ##quantity = []
    # for k,v in request.session['shopCartDict'].items():
    #     productObject = hmod.ProductSpecification.objects.get(id=k)
    #     productDictionary[productObject] = int(v)


    # params['products'] = productDictionary
    # ##params['quantities'] = quantity
    # print(request.session['shopCartDict'])
    ##request.session.flush()
    return dmp_render_to_response(request, 'shoppingCart.html', params)

@view_function
def remove(request):
    params = {}

    pid = request.urlparams[0]
    print(">>>>>>>>>>>>")
    print(pid)
    del request.session['shopCartDict'][pid]
    request.session.modified = True

    productDictionary = {}
    ##quantity = []
    orderTotal = 0
    for k,v in request.session['shopCartDict'].items():
        productObject = hmod.SerializedProduct.objects.get(id=k)
        productDictionary[productObject] = int(v)
        orderTotal += (productObject.product_specification.price * v)

    params['orderTotal'] = orderTotal
    params['products'] = productDictionary
    ##params['quantities'] = quantity
    print(request.session['shopCartDict'])
    ##request.session.flush()
    return dmp_render_to_response(request, 'shoppingCart.html', params)
