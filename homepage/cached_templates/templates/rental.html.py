# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1428609050.782279
_enable_loop = True
_template_filename = 'C:\\Users\\Kevin\\Documents\\GitHub\\CHFIntex2\\homepage\\templates/rental.html'
_template_uri = 'rental.html'
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
        def content():
            return render_content(context._locals(__M_locals))
        rentals = context.get('rentals', UNDEFINED)
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
        rentals = context.get('rentals', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\r\n    <head>\r\n        <title>Rentals</title>\r\n    </head>\r\n    <div class="tableContain">\r\n        <h1>Rentals</h1>\r\n        <div id="DisplayProducts">\r\n            <div class="displaystuff">\r\n')
        for rental in rentals:
            __M_writer('                    <div class="productstuff">\r\n                        <div class="productDiv">\r\n                          <a href="/rental_detail/')
            __M_writer(str( rental.id ))
            __M_writer('"><img src="')
            __M_writer(str( rental.product_specification.photo.image ))
            __M_writer('"/></a>\r\n                          <div class="buyButton"><a href="/rental_detail/')
            __M_writer(str( rental.id ))
            __M_writer('">')
            __M_writer(str( rental.product_specification.name ))
            __M_writer('</a></div><br>\r\n                          <div class="center">\r\n                            <p class="bold">Price Per Day: </p>')
            __M_writer(str( rental.price_per_day ))
            __M_writer(' <br><br>\r\n                            <button data-pid="')
            __M_writer(str( rental.id ))
            __M_writer('" class="add_button btn btn-warning">Rent Now</button>\r\n                          </div>\r\n                        </div>\r\n                    </div>\r\n')
        __M_writer('            </div>\r\n        </div>\r\n    </div>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"uri": "rental.html", "source_encoding": "ascii", "filename": "C:\\Users\\Kevin\\Documents\\GitHub\\CHFIntex2\\homepage\\templates/rental.html", "line_map": {"64": 17, "65": 17, "66": 18, "35": 1, "68": 23, "40": 26, "74": 68, "46": 3, "59": 14, "67": 18, "53": 3, "54": 11, "55": 12, "56": 14, "57": 14, "58": 14, "27": 0, "60": 15, "61": 15, "62": 15, "63": 15}}
__M_END_METADATA
"""
