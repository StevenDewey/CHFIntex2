from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django_mako_plus.controller.router import get_renderer
from django_mako_plus.controller import view_function
from django import forms
from django.forms import ModelChoiceField
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
import homepage.models as hmod


templater = get_renderer('homepage')


@view_function
# @permission_required('homepage.view_user', login_url='/homepage/invalid_permissions/')
def process_request(request):
    params = {}

    users= hmod.User.objects.all().order_by('id')
    params['users'] = users

    return templater.render_to_response(request, 'user.html', params)

@view_function
def create(request):
    params = {}

    # class MyModelChoiceField(ModelChoiceField):
    #     def label_from_instance(self, obj):
    #         return "%i" % obj.id

    class UserEditForm(forms.Form):
        username = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'id': "inputError1"}))
        password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))#, widget=forms.PasswordInput)
        first_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        last_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        email = forms.CharField(required=True, max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))



    form = UserEditForm()

    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            '''Create a new user'''
            user = hmod.User()
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']

            user.save()

            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/homepage')
        else:
            params['error'] = "<p class='bg-danger'>All fields are required</p>"
            params['form'] = form
            return templater.render_to_response(request, 'user.create.html', params)

    params['error'] = ''
    params['form'] = form
    return templater.render_to_response(request, 'user.create.html', params)


@view_function
# @permission_required('homepage.change_user', login_url='/homepage/invalid_permissions/')
def create_edit(request):
    params = {}

    try:
        user = hmod.User.objects.get(id=request.urlparams[0])
    except hmod.User.DoesNotExist:
        return HttpResponseRedirect('/homepage/user/')

    class MyModelChoiceField(ModelChoiceField):
        def label_from_instance(self, obj):
            return "%i" % obj.id

    class UserEditForm(forms.Form):
        username = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        password = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))#, widget=forms.PasswordInput)
        first_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        last_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        email = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        # security_question = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        # security_answer = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        # phone = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    form = UserEditForm(initial={
        'username': user.username,
        'password': user.password,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        # 'security_question': user.security_question,
        # 'security_answer': user.security_answer,
        # 'phone': user.phone,
    })

    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            # user.security_question = form.cleaned_data['security_question']
            # user.security_answer = form.cleaned_data['security_answer']
            # user.phone = form.cleaned_data['phone']

            user.save()

            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/homepage')

    params['form'] = form
    return templater.render_to_response(request, 'user.create.html', params)

@view_function
# @permission_required('homepage.change_user', login_url='/homepage/invalid_permissions/')
def edit(request):
    params = {}

    try:
        user = hmod.User.objects.get(id=request.urlparams[0])
    except hmod.User.DoesNotExist:
        return HttpResponseRedirect('/homepage/user/')

    class MyModelChoiceField(ModelChoiceField):
        def label_from_instance(self, obj):
            return "%i" % obj.id

    class UserEditForm(forms.Form):
        username = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        password = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))#, widget=forms.PasswordInput)
        first_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        last_name = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        email = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        phone = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        # security_question = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
        # security_answer = forms.CharField(required=True, max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    form = UserEditForm(initial={
        'username': user.username,
        'password': user.password,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone,
        # 'security_question': user.security_question,
        # 'security_answer': user.security_answer,
    })

    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone = form.cleaned_data['phone']
            # user.security_question = form.cleaned_data['security_question']
            # user.security_answer = form.cleaned_data['security_answer']
            user.save()

            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/homepage')

    params['form'] = form
    return templater.render_to_response(request, 'user.edit.html', params)


@view_function
@permission_required('homepage.delete_user', login_url='/homepage/invalid_permissions/')
def delete(request):

    '''delete an user'''
    try:
        user = hmod.User.objects.get(id=request.urlparams[0])
    except hmod.User.DoesNotExist:
        return HttpResponseRedirect('/homepage/user/')

    user.delete()

    return HttpResponseRedirect('/homepage/user/'.format(user.id))

@view_function
def check_username(request):
    username = request.REQUEST.get('u')

    #check to see if in database
    #make sure you take care of the case where I set my own username to the same username
    try:
        user = hmod.User.objects.get(username=username)# if exists:
        return HttpResponse('Exists')
    except hmod.User.DoesNotExist: # if does not exist
        return HttpResponse('DoesNotExist')

@view_function
def reset_username(request):
    username = request.REQUEST.get('u')

    #check to see if in database
    #make sure you take care of the case where I set my own username to the same username
    try:
        user = hmod.User.objects.get(username=username)# if exists:
        return HttpResponse('Exists')
    except hmod.User.DoesNotExist: # if does not exist
        return HttpResponse('DoesNotExist')
