from django_mako_plus.controller import view_function
from django.http import HttpResponse, HttpResponseRedirect, Http404
import homepage.models as hmod

@view_function
def process_request(request):
    return HttpResponseRedirect('/homepage/')