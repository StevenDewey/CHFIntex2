# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1428532923.110151
_enable_loop = True
_template_filename = 'C:\\Users\\Kevin\\Documents\\GitHub\\CHFIntex2\\homepage\\templates/login.loginform.html'
_template_uri = 'login.loginform.html'
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
    return runtime._inherit_from(context, '/homepage/templates/base_ajax.htm', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        def content():
            return render_content(context._locals(__M_locals))
        form = context.get('form', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\r\n\r\n')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer('\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def content():
            return render_content(context)
        form = context.get('form', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\r\n\r\n    <head>\r\n         <title>Login</title>\r\n    </head>\r\n\r\n    <form id="loginform" method="POST" action="/homepage/login.loginform">\r\n        <table>\r\n            ')
        __M_writer(str(form))
        __M_writer('\r\n        </table>\r\n        <div>\r\n            <input id="login_submit" type = "submit"/>\r\n            <a href="/homepage/user.create/">Or click here to create an account</a>\r\n            <br>\r\n            <a href="/password_reset/" style="margin-left: 64px">forgot password?</a>\r\n        </div>\r\n    </form>\r\n\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "C:\\Users\\Kevin\\Documents\\GitHub\\CHFIntex2\\homepage\\templates/login.loginform.html", "line_map": {"35": 1, "53": 3, "54": 11, "55": 11, "40": 21, "27": 0, "61": 55, "46": 3}, "source_encoding": "ascii", "uri": "login.loginform.html"}
__M_END_METADATA
"""
