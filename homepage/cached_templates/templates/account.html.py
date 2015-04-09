# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1428612556.188265
_enable_loop = True
_template_filename = 'C:\\Users\\Kevin\\Documents\\GitHub\\CHFIntex2\\homepage\\templates/account.html'
_template_uri = 'account.html'
_source_encoding = 'ascii'
import os, os.path, re
_exports = ['content']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, 'base.htm', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        user = context.get('user', UNDEFINED)
        def content():
            return render_content(context._locals(__M_locals))
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\r\n\r\n<html>\r\n<head>\r\n\r\n</head>\r\n<body>\r\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer('\r\n</body>\r\n</html>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        user = context.get('user', UNDEFINED)
        def content():
            return render_content(context)
        request = context.get('request', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\r\n        <div class="page-header">\r\n            <h1> Your Account <small></small></h1>\r\n        </div>\r\n        <table class="table table-bordered table-hover">\r\n            <tr>\r\n                <th> Name </th>\r\n                <th> Email </th>\r\n                <th> Phone Number </th>\r\n                <th> Street </th>\r\n                <th> Street 2 </th>\r\n                <th> City </th>\r\n                <th> State </th>\r\n                <th> Zip </th>\r\n                <th> Country </th>\r\n            </tr>\r\n\r\n            <tr>\r\n                <td>')
        __M_writer(str( user.first_name + " " + user.last_name ))
        __M_writer('</td>\r\n                <td>')
        __M_writer(str( user.email ))
        __M_writer('</td>\r\n                <td>')
        __M_writer(str( user.phone ))
        __M_writer('</td>\r\n                <td>')
        __M_writer(str( user.address.street1 ))
        __M_writer('</td>\r\n                <td>')
        __M_writer(str( user.address.street2 ))
        __M_writer('</td>\r\n                <td>')
        __M_writer(str( user.address.city ))
        __M_writer('</td>\r\n                <td>')
        __M_writer(str( user.address.state ))
        __M_writer('</td>\r\n                <td>')
        __M_writer(str( user.address.zip_code ))
        __M_writer('</td>\r\n                <td>')
        __M_writer(str( user.address.country ))
        __M_writer('</td>\r\n            </tr>\r\n        </table>\r\n        <a href="/homepage/edit_account/')
        __M_writer(str( request.user.id ))
        __M_writer('/')
        __M_writer(str( request.user.address_id ))
        __M_writer('"><button id="edit_btn" type="button" class="btn btn-default">Edit</button></a>\r\n        <a href="/homepage/edit_account.password/')
        __M_writer(str( user.id ))
        __M_writer('/"><button id="change_password_btn" type="button" class="btn btn-default">Change Password</button></a>\r\n    ')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"64": 30, "65": 30, "66": 31, "67": 31, "68": 32, "69": 32, "70": 33, "71": 33, "72": 34, "73": 34, "74": 37, "75": 37, "76": 37, "77": 37, "78": 38, "79": 38, "85": 79, "27": 0, "36": 1, "41": 39, "47": 8, "55": 8, "56": 26, "57": 26, "58": 27, "59": 27, "60": 28, "61": 28, "62": 29, "63": 29}, "uri": "account.html", "filename": "C:\\Users\\Kevin\\Documents\\GitHub\\CHFIntex2\\homepage\\templates/account.html"}
__M_END_METADATA
"""
