# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1428567117.135832
_enable_loop = True
_template_filename = 'C:\\Users\\David\\Documents\\GitHub\\CHFIntex2\\homepage\\templates/product.html'
_template_uri = 'product.html'
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
        products = context.get('products', UNDEFINED)
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
        products = context.get('products', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\r\n<head>\r\n    <title>Products</title>\r\n</head>\r\n')
        __M_writer('<div class="text-right">\r\n  <input id="search"/> <button class="filter btn btn-info" >Search</button> <div id="results"></div>\r\n')
        __M_writer('</div>\r\n    <div class="tableContain">\r\n    <h1>Products</h1>\r\n        <div id="DisplayProducts">\r\n            <div class="displaystuff">\r\n')
        for product in products:
            __M_writer('                <div class="productstuff">\r\n                    <div class="productDiv">\r\n                        <a href="/homepage/product_detail/')
            __M_writer(str( product.id ))
            __M_writer('"><img src="')
            __M_writer(str( product.product_specification.photo.image ))
            __M_writer('"/></a>\r\n                        <div class="buyButton"><a  class="bold" href="/homepage/product_detail/')
            __M_writer(str( product.id ))
            __M_writer('">')
            __M_writer(str( product.product_specification.name ))
            __M_writer('</a></div><br>\r\n                        <div class="center">\r\n                          <p class="bold">Price: </p>')
            __M_writer(str( product.product_specification.price ))
            __M_writer(' <br><br>\r\n                          <button data-pid="')
            __M_writer(str( product.id ))
            __M_writer('" class="add_button btn btn-warning">Buy Now</button>\r\n                        </div>\r\n                    </div>\r\n                </div>\r\n')
        __M_writer('            </div>\r\n        </div>\r\n    </div>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "filename": "C:\\Users\\David\\Documents\\GitHub\\CHFIntex2\\homepage\\templates/product.html", "line_map": {"64": 20, "65": 20, "66": 22, "67": 22, "68": 23, "69": 23, "70": 28, "76": 70, "27": 0, "35": 1, "40": 31, "46": 3, "53": 3, "54": 8, "55": 11, "56": 16, "57": 17, "58": 19, "59": 19, "60": 19, "61": 19, "62": 20, "63": 20}, "uri": "product.html"}
__M_END_METADATA
"""
