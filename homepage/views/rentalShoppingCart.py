from django.conf import settings
from django.http import HttpResponse
from django_mako_plus.controller import view_function
from .. import dmp_render, dmp_render_to_response
import homepage.models as hmod

@view_function
def process_request(request):
    params = {}

    rental = hmod.RentalProduct.objects.get(id=request.urlparams[0])

    params['rental'] = rental

    return dmp_render_to_response(request, 'rentalShoppingCart.html', params)

@view_function
def add(request):
    ##request.session.flush()
    ##print(request.session['shopCartDict'])
    params = {}

    request.session['ptype'] = "rental"

    if 'rentalShopCartDict' not in request.session:
        request.session['rentalShopCartDict'] = {}
    # print(request.session['shopping_cart'])
    # fav_color = request.session.pop('shopping_cart')

    pid = request.urlparams[0]
    dur = request.urlparams[1]

    # print(request.session['shopping_cart'])
    if pid in request.session['rentalShopCartDict']:
        request.session['rentalShopCartDict'][pid] += int(dur)
    else:
        request.session['rentalShopCartDict'][pid] = int(dur)
    request.session.modified = True
    rentalProductDictionary = {}
    ##quantity = []
    
    orderTotal = 0
    for k,v in request.session['rentalShopCartDict'].items():
        rentalProductObject = hmod.RentalProduct.objects.get(id=k)
        rentalProductDictionary[rentalProductObject] = int(v)
        orderTotal += (rentalProductObject.price_per_day * v)

    params['rentalProducts'] = rentalProductDictionary
    params['orderTotal'] = orderTotal
    ##params['quantities'] = quantity
    ##request.session.flush()
    return dmp_render_to_response(request, 'rentalShoppingCart.html', params)

@view_function
def updateDuration(request):
    params = {}

    pid = request.urlparams[0]
    dur = request.urlparams[1]

    # # print(request.session['shopping_cart'])
    # if pid in request.session['shopCartDict']:
    #     request.session['shopCartDict'][pid] += int(qty)
    # else:
    request.session['rentalShopCartDict'][pid] = int(dur)
    request.session.modified = True
    # productDictionary = {}
    # ##quantity = []
    # for k,v in request.session['shopCartDict'].items():
    #     productObject = hmod.ProductSpecification.objects.get(id=k)
    #     productDictionary[productObject] = int(v)


    # params['products'] = productDictionary
    # ##params['quantities'] = quantity
    # print(request.session['shopCartDict'])
    ##request.session.flush()
    return dmp_render_to_response(request, 'rentalShoppingCart.html', params)

@view_function
def remove(request):
    params = {}

    pid = request.urlparams[0]
    print(">>>>>>>>>>>>")
    print(pid)
    del request.session['rentalShopCartDict'][pid]
    request.session.modified = True

    rentalProductDictionary = {}
    ##quantity = []
    orderTotal = 0
    for k,v in request.session['rentalShopCartDict'].items():
        rentalProductObject = hmod.RentalProduct.objects.get(id=k)
        rentalProductDictionary[rentalProductObject] = int(v)
        orderTotal += (rentalProductObject.price_per_day * v)

    params['orderTotal'] = orderTotal
    params['rentalProducts'] = rentalProductDictionary
    ##params['quantities'] = quantity
    print(request.session['rentalShopCartDict'])
    ##request.session.flush()
    return dmp_render_to_response(request, 'rentalShoppingCart.html', params)
