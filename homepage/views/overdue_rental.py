from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django_mako_plus.controller.router import get_renderer
from django_mako_plus.controller import view_function
from datetime import datetime, timedelta
from django.core.mail import send_mail
import homepage.models as hmod
from django.contrib.auth.decorators import permission_required

templater = get_renderer('homepage')

@view_function
@permission_required('homepage.add_serializedproduct', login_url='/homepage/invalid_permissions/')
def process_request(request):
    params = {}

    overdue_rentals30 = hmod.RentalItem.objects.filter(date_due__gte = datetime.today()-timedelta(days=30), date_due__lte = datetime.today(), date_in = None).order_by('date_due')
    params['overdue_rentals30'] = overdue_rentals30
    overdue_rentals60 = hmod.RentalItem.objects.filter(date_due__gte = datetime.today()-timedelta(days=60), date_due__lte = datetime.today()-timedelta(days=30), date_in = None).order_by('date_due')
    params['overdue_rentals60'] = overdue_rentals60
    overdue_rentals90 = hmod.RentalItem.objects.filter(date_due__gte = datetime.today()-timedelta(days=90), date_due__lte = datetime.today()-timedelta(days=60), date_in = None).order_by('date_due')
    params['overdue_rentals90'] = overdue_rentals90
    overdue_rentals90p = hmod.RentalItem.objects.filter(date_due__lte = datetime.today()-timedelta(days=90), date_in = None).order_by('date_due')
    params['overdue_rentals90p'] = overdue_rentals90p
    complete = ' '
    params['complete'] = complete
    return templater.render_to_response(request, 'overdue_rental.html', params)

@view_function
def success(request):
    params = {}

    overdue_rentals30 = hmod.RentalItem.objects.filter(date_due__gte = datetime.today()-timedelta(days=30), date_due__lte = datetime.today()).order_by('date_due')
    params['overdue_rentals30'] = overdue_rentals30
    overdue_rentals60 = hmod.RentalItem.objects.filter(date_due__gte = datetime.today()-timedelta(days=60), date_due__lte = datetime.today()-timedelta(days=30)).order_by('date_due')
    params['overdue_rentals60'] = overdue_rentals60
    overdue_rentals90 = hmod.RentalItem.objects.filter(date_due__gte = datetime.today()-timedelta(days=90), date_due__lte = datetime.today()-timedelta(days=60)).order_by('date_due')
    params['overdue_rentals90'] = overdue_rentals90
    overdue_rentals90p = hmod.RentalItem.objects.filter(date_due__lte = datetime.today()-timedelta(days=90)).order_by('date_due')
    params['overdue_rentals90p'] = overdue_rentals90p
    complete = "<p class='bg-success'>Emails sent successfully!</p>"
    params['complete'] = complete

    return templater.render_to_response(request, 'overdue_rental.html', params)

@view_function
def batch_email(request):
    params = {}

    overdue_rentals = hmod.RentalItem.objects.filter(date_due__lte = datetime.today()).order_by('date_due')

    emailbody = templater.render(request, 'overdue_notification.html', params)

    for r in overdue_rentals:
        send_mail("Overdue Rental", emailbody, 'Support@chf2015.com', [r.order.customer.email], html_message=emailbody, fail_silently=False)


    return HttpResponseRedirect('/homepage/overdue_rental.success/')
