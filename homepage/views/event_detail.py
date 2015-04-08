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

    event = hmod.Event.objects.get(id=request.urlparams[0])
    areas = hmod.Area.objects.filter(event=event.id)

    params['event'] = event
    params['areas'] = areas
    return templater.render_to_response(request, 'event_detail.html', params)
