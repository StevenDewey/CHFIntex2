from datetime import datetime, timedelta
from django.core.mail import send_mail
import requests
from django.http import HttpResponseRedirect
from django_mako_plus.controller.router import get_renderer
from django_mako_plus.controller import view_function
from django import forms

import homepage.models as hmod

templater = get_renderer('homepage')

############################################################
#### Display Checkout Form with Items in Shopping Cart

@view_function
# @login_required(login_url='/homepage/checkout.login/')
def process_request(request):
    params = {}

    # this is where we add the shipping address to the database

    class AddressForm(forms.Form):

        street1 = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        street2 = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        city = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        state = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        zip_code = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        country = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    form = AddressForm()

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = hmod.Address()
            address.street1 = form.cleaned_data['street1']
            address.street2 = form.cleaned_data['street2']
            address.city = form.cleaned_data['city']
            address.state = form.cleaned_data['state']
            address.zip_code = form.cleaned_data['zip_code']
            address.country = form.cleaned_data['country']
            address.save()

            params['address_id'] = address.id
            params['error'] = ''
            params['form'] = form
            return templater.render_to_response(request, 'checkout.payment_info.html', params)

        else:
            params['error'] = "<p class='bg-danger'>Fields are required</p>"
            params['form'] = form
            return templater.render_to_response(request, 'checkout.ship_address.html', params)

    # return templater.render_to_response(request, 'checkout.payment_info.html', params)
    params['form'] = form
    return templater.render_to_response(request, 'checkout.ship_address.html', params)


@view_function
def payment_info(request):
    params = {}

    return templater.render_to_response(request, 'checkout.payment_info.html', params)


@view_function
def process_cc(request):
    params = {}

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

    resp = r.json()

    if 'error' in resp: # error?
        print("ERROR: ", resp['error'])
        return HttpResponseRedirect('/homepage/checkout/')

    else:
        a = hmod.Address.objects.all().order_by("-id").first()
        order = hmod.Order()
        order.phone = request.user.phone,
        order.order_date = datetime.today()
        order.date_paid = datetime.today()
        order.ships_to = a
        order.customer = request.user
        order.save()

        if "rental" in request.session['ptype']:
            rentalProductDictionary = {}
            orderTotal = 0
            for k,v in request.session['rentalShopCartDict'].items():
                rentalProductObject = hmod.RentalProduct.objects.get(id=k)
                rentalProductDictionary[rentalProductObject] = int(v)
                orderTotal += rentalProductObject.price_per_day * v
                ri = hmod.RentalItem()
                ri.date_out = datetime.today()
                ri.date_due = datetime.today()+timedelta(days=int(v))
                ri.rental_product = hmod.RentalProduct.objects.get(id=k)
                ri.amount = rentalProductObject.price_per_day * v
                ri.order = hmod.Order.objects.all().order_by("-id").first()
                ri.discount_percent = 0
                ri.save()

            params['orderTotal'] = orderTotal
            params['rentals'] = rentalProductDictionary

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
                si = hmod.SaleItem()
                si.quantity = v
                si.product = hmod.SerializedProduct.objects.get(id=k)
                si.amount = productObject.product_specification.price * v
                si.order = hmod.Order.objects.all().order_by("-id").first()
                si.save()

            params['orderTotal'] = orderTotal
            params['products'] = productDictionary

            print(">>>>>>>>>>>>")
            print(request.session['shopCartDict'])

            ##Jong's Email Idea:
            user_email = request.user.email
            emailbody = templater.render(request, 'checkout_product_email.html', params)
            send_mail("Thank You -- CHF Receipt", emailbody, 'Support@chf2015.com', [user_email], html_message=emailbody, fail_silently=False)

            return HttpResponseRedirect('/homepage/thank_you/')
