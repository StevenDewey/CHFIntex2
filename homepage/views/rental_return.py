from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import HttpRequest
from django_mako_plus.controller.router import get_renderer
from django_mako_plus.controller import view_function
from datetime import datetime, timedelta
import homepage.models as hmod
from django import forms

from django.forms import ModelChoiceField
from django.contrib.auth.decorators import permission_required

templater = get_renderer('homepage')

@view_function
def process_request(request):
# def loginform(request):
    params = {}

    form = rentalReturnForm()

    if request.urlparams[0] == "success":
        params['success'] = "<h3>Success! Item returned</h3>"
    else:
        params['success'] = ""

    error = ''
    action = '/homepage/rental_return/'

    if request.method == 'POST':
        form = rentalReturnForm(request.POST)
        if form.is_valid():
            try:
                rentalitem = hmod.RentalItem.objects.get(id=form.cleaned_data['rentalID'])
                rentalitem.date_in = datetime.today()
                print('>>>>>>>>>>>>>>>>>>')
                print(rentalitem.id)
                print(rentalitem.date_in)
                rentalitem.save()

            except hmod.RentalItem.DoesNotExist:
                error = '<h3>Invalid rental id. Try again or give up.</h3>'
                params['error'] = error
                params['form'] = form
                params['action'] = action
                return templater.render_to_response(request, 'rental_return.html', params)

            return HttpResponseRedirect('/homepage/rental_return.fees/{}/'.format(rentalitem.order_id) + '{}/'.format(rentalitem.id))


    params['action'] = action
    params['error'] = error
    params['form'] = form
    return templater.render_to_response(request, 'rental_return.html', params)

class rentalReturnForm(forms.Form):
    rentalID = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        rentalItem = self.cleaned_data['rentalID']
        if rentalItem == None:
            raise forms.ValidationError('Incorrect Rental Item ID')

@view_function
def fees(request):
    params = {}

    p = request.urlparams[0]
    g = request.urlparams[1]
    form = feesForm(initial={'orderID': p,
                             'RentalItemID': g})
    action = '/homepage/rental_return.fees/{}/'.format(p) + '{}/'.format(g)
    # rentalitem = hmod.RentalItem.objects.get(id=request.urlparams[0])
    # print(rentalitem)

    ri = hmod.RentalItem.objects.get(id = g)
    # function to figure out the days late
    def days_between(d1, d2):
        return int((d1 - d2).days)
    # set the days late using the previous function
    dl = days_between(ri.date_in, ri.date_due)
    # make sure to never spit back a negative number of days late
    if dl <= 0:
        days_late = 0
    else:
        days_late = dl
    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 1')

    if request.method == 'POST':
        form = feesForm(request.POST)
        if form.is_valid():
            try:
                print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 4')
                lateFee = hmod.LateFee()
                lateFee.waived = form.cleaned_data['lateWaived']
                lateFee.days_late = days_late
                lateFee.amount = int(ri.rental_product.cost) * int(form.cleaned_data['feePercent']) * .01 * days_late
                # lateFee.order_id = hmod.Order.objects.get(id = p)
                lateFee.order_id = p
                lateFee.rental_item = ri
                lateFee.save()
                print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 5')
                damageFee = hmod.DamageFee()
                damageFee.amount = form.cleaned_data['damageFee']
                damageFee.waived = form.cleaned_data['waived']
                damageFee.description = form.cleaned_data['description']
                damageFee.order_id = form.cleaned_data['orderID']
                damageFee.rental_item_id = form.cleaned_data['RentalItemID']
                damageFee.save()
                print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 6')

            except hmod.RentalItem.DoesNotExist:
                error = '<h3>Invalid rental id. Try again or give up.</h3>'
                params['error'] = error
                params['form'] = form
                return templater.render_to_response(request, 'rental_return.html', params)

            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 10')
            return HttpResponseRedirect('/homepage/rental_return/{}/'.format('success'))

    print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< 2')
    params['days_late'] = days_late
    rental = hmod.RentalItem.objects.get(id=request.urlparams[0])
    params['rental'] = rental
    product = hmod.RentalProduct.objects.get(id=rental.rental_product.id)
    rentalItems = hmod.RentalItem.objects.get(rental_product = product.id)
    damages = hmod.DamageFee.objects.filter(rental_item = rentalItems.id)
    params['damages'] = damages
    params['success'] = ""
    error = ''
    params['error'] = error
    # params['rentalitem'] = rentalitem
    params['form'] = form
    params['action'] = action
    return templater.render_to_response(request, 'rental_return.fees.html', params)


class feesForm(forms.Form):
    feePercent = forms.ChoiceField(choices= [(x, x) for x in range(1, 100)])
    lateWaived = forms.BooleanField(required=False)
    damageFee = forms.ChoiceField(choices=[(x, x) for x in range(1, 50)])
    waived = forms.BooleanField(required=False)
    description = forms.CharField(widget=forms.Textarea)
    orderID = forms.CharField(widget=forms.HiddenInput(), initial='class')
    RentalItemID = forms.CharField(widget=forms.HiddenInput(), initial='class')

    def clean(self):
        damageFee = self.cleaned_data['damageFee']
        description = self.cleaned_data['description']

        if damageFee == None:
            raise forms.ValidationError('Incorrect Fee')
        if description == None:
            raise forms.ValidationError('description is required')