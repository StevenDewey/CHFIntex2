from django.conf import settings
from django.http import HttpResponse
from django_mako_plus.controller import view_function
from .. import dmp_render, dmp_render_to_response
import homepage.models as hmod

@view_function
def process_request(request):
    template_vars = {}
    return dmp_render_to_response(request, 'username.html', template_vars)


@view_function
def check_username(request):
    username = request.REQUEST.get('u')
    print('>>>>>>>>>>>>>>>>>' + username)

    #check to see if in database
    #make sure you take care of the case where I set my own username to the same username
    try:
        user = hmod.User.objects.get(username=username)# if exists:
        return HttpResponse('0')
    except hmod.User.DoesNotExist: # if does not exist
        return HttpResponse('1')
