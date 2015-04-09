from django.conf import settings
from django import forms
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django_mako_plus.controller import view_function
from django_mako_plus.controller.router import get_renderer
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime
from django.core.mail import send_mail
import requests
from django_mako_plus.controller import view_function
from .. import dmp_render, dmp_render_to_response
import homepage.models as hmod

import homepage.models as hmod

templater = get_renderer('homepage')

############################################################
#### Display Checkout Form with Items in Shopping Cart
#@login_required(login_url='/homepage/login/',redirect_field_name='')
@view_function
# @login_required(login_url='/homepage/checkout.login/')
def process_request(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/accounts/login.logincheckoutptone/')
    params = {}

    return templater.render_to_response(request, 'checkout.html', params)

@view_function
def process_cc(request):
    params = {}

    # ptype = request.urlparams[0]

    API_URL = 'http://dithers.cs.byu.edu/iscore/api/v1/charges'
    API_KEY ='5ac6b61282edafc1b039a0cd314d11d9'

    #All of this data will be dynamic during INTEX_II. For now, it's hardcoded.
    r = requests.post(API_URL, data={
        'apiKey': API_KEY,
        'currency': 'usd',
        'amount': '5.99',#Get from form
        'type': 'Visa',
        'number': '4732817300654',#Get from form
        'exp_month': '10',#Get from form
        'exp_year': '15',#Get from form
        'cvc': '411',#Get from form
        'name': 'Cosmo Limesandal',#Get from form
        'description': 'Charge for cosmo@is411.byu.edu"',#Get from form
    })

    print(r.text)

    resp = r.json()
    if 'error' in resp: # error?
        print("ERROR: ", resp['error'])
        return HttpResponseRedirect('/homepage/checkout/')

    else:
        print(resp.keys())
        print(resp['ID'])

        if "rental" in request.session['ptype']:
            rentalProductDictionary = {}
            orderTotal = 0
            for k,v in request.session['rentalShopCartDict'].items():
                rentalProductObject = hmod.RentalProduct.objects.get(id=k)
                rentalProductDictionary[rentalProductObject] = int(v)
                orderTotal += rentalProductObject.price_per_day * v

            params['orderTotal'] = orderTotal
            params['rentals'] = rentalProductDictionary

            print(">>>>>>>>>>>>")
            print(request.session['rentalShopCartDict'])

            ##Jong's Email Idea:
            user_email = request.user.email
            emailbody = templater.render(request, 'checkout_rental_email.html', params)
            send_mail("Thank You -- CHF Receipt", emailbody, 'Support@chf2015.com', [user_email], html_message=emailbody, fail_silently=False)

            return HttpResponseRedirect('/homepage/thank_you/')

        else:
            productDictionary = {}
            orderTotal = 0
            for k,v in request.session['shopCartDict'].items():
                productObject = hmod.SerializedProduct.objects.get(id=k)
                productDictionary[productObject] = int(v)
                orderTotal += productObject.product_specification.price * v

            params['orderTotal'] = orderTotal
            params['products'] = productDictionary

            print(">>>>>>>>>>>>")
            print(request.session['shopCartDict'])

            ##Jong's Email Idea:
            user_email = request.user.email
            emailbody = templater.render(request, 'checkout_product_email.html', params)
            send_mail("Thank You -- CHF Receipt", emailbody, 'Support@chf2015.com', [user_email], html_message=emailbody, fail_silently=False)

            return HttpResponseRedirect('/homepage/thank_you/')
