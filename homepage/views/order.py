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

    orders = hmod.Order.objects.all().order_by('id')
    params['orders'] = orders

    return templater.render_to_response(request, 'order.html', params)


@view_function
@permission_required('homepage.change_order', login_url='/homepage/invalid_permissions/')
def edit(request):
    params = {}

    try:
        order = hmod.Order.objects.get(id=request.urlparams[0])
    except hmod.Order.DoesNotExist:
        return HttpResponseRedirect('/homepage/order/')

    class PersonModelChoiceField(ModelChoiceField):
        def label_from_instance(self, obj):
            return str(obj.id) + " - " + obj.given_name + " " + obj.family_name

    class OrderEditForm(forms.Form):
        order_date = forms.DateTimeField(required=True, widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
        phone = forms.CharField(max_length=12, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        date_packed = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control'}))
        date_paid = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control'}))
        date_shipped = forms.DateField(required=True, widget=forms.DateInput(attrs={'class': 'form-control'}))
        tracking_number = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        ship_address1 = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        ship_address2 = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        ship_city = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        ship_state = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        ship_zip = forms.IntegerField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        ship_country = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
        Agent_id = PersonModelChoiceField(
            queryset=hmod.Agent.objects.all(), empty_label=None,
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    form = OrderEditForm(initial={
        'order_date': order.order_date,
        'phone': order.phone,
        'date_packed': order.date_packed,
        'date_paid': order.date_paid,
        'date_shipped': order.date_shipped,
        'tracking_number': order.tracking_number,
        'ship_address1': order.ship_address1,
        'ship_address2': order.ship_address2,
        'ship_city': order.ship_city,
        'ship_state': order.ship_state,
        'ship_zip': order.ship_zip,
        'ship_country': order.ship_country,
        'Agent_id': order.Agent_id,
    })
    if request.method == 'POST':
        form = OrderEditForm(request.POST)
        if form.is_valid():
            order.order_date = form.cleaned_data['order_date']
            order.phone = form.cleaned_data['phone']
            order.date_packed = form.cleaned_data['date_packed']
            order.date_paid = form.cleaned_data['date_paid']
            order.date_shipped = form.cleaned_data['date_shipped']
            order.tracking_number = form.cleaned_data['tracking_number']
            order.ship_address1 = form.cleaned_data['ship_address1']
            order.ship_address2 = form.cleaned_data['ship_address2']
            order.ship_city = form.cleaned_data['ship_city']
            order.ship_state = form.cleaned_data['ship_state']
            order.ship_zip = form.cleaned_data['ship_zip']
            order.ship_country = form.cleaned_data['ship_country']
            order.Agent_id = form.cleaned_data['Agent_id']
            order.save()
            return HttpResponseRedirect('/homepage/order/')

    params['form'] = form
    return templater.render_to_response(request, 'order.edit.html', params)


@view_function
@permission_required('homepage.add_order', login_url='/homepage/invalid_permissions/')
def create(request):

    '''Creates a new order'''
    order = hmod.Order()
    order.order_date = '2015-01-01'
    order.phone = '555-555-5555'
    order.date_packed = '2015-01-01'
    order.date_paid = '2015-01-01'
    order.date_shipped = '2015-01-01'
    order.tracking_number = 0
    order.ship_address1 = 'Street Address'
    order.ship_address2 = 'Address 2'
    order.ship_city = 'City'
    order.ship_state = 'State'
    order.ship_zip = 00000
    order.ship_country = 'Country'
    order.Agent_id = hmod.Agent.objects.first().id
    order.save()

    return HttpResponseRedirect('/homepage/order.edit/{}/'.format(order.id))

@view_function
@permission_required('homepage.delete_order', login_url='/homepage/invalid_permissions/')
def delete(request):

    '''delete an order'''
    try:
        order = hmod.Order.objects.get(id=request.urlparams[0])
    except hmod.Order.DoesNotExist:
        return HttpResponseRedirect('/homepage/order/')

    order.delete()

    return HttpResponseRedirect('/homepage/order/'.format(order.id))
