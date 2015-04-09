# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1428532920.440966
_enable_loop = True
_template_filename = 'C:\\Users\\Kevin\\Documents\\GitHub\\CHFIntex2\\homepage\\templates/base.htm'
_template_uri = 'base.htm'
_source_encoding = 'ascii'
import os, os.path, re
_exports = ['content']


from django_mako_plus.controller import static_files 


import datetime


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        STATIC_URL = context.get('STATIC_URL', UNDEFINED)
        def content():
            return render_content(context._locals(__M_locals))
        request = context.get('request', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\r\n')
        __M_writer('\r\n')
        static_renderer = static_files.StaticRenderer(self) 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['static_renderer'] if __M_key in __M_locals_builtin_stored]))
        __M_writer('\r\n')
        __M_writer('\r\n\r\n\r\n<!DOCTYPE html>\r\n\r\n<html>\r\n\r\n<head>\r\n\r\n\r\n')
        __M_writer('    <meta name="description" content="Colonial Heritage Foundation is a foundation based in Orem, UT. The foundation holds a\r\n    festival every year to showcase some of our American legacy from colonial times. The events include many artisans, activities, vintage\r\n    clothing items, and many things to do for the whole family. Many products and rental items are available online for purchase and checkout.">\r\n    <meta name="keywords" content="Colonial, Heritage, Foundation, Civil War, Freedom, Ye Olde America, American History">\r\n    <meta name="author" content="Colonial Heritage Foundation">\r\n    <meta charset="UTF-8">\r\n\r\n\r\n    <link rel="icon" type="image/jpeg" href="/static/homepage/media/flag1.jpg"/>\r\n\r\n')
        __M_writer('\r\n    <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>\r\n    <script src="')
        __M_writer(str( STATIC_URL ))
        __M_writer('homepage/media/jquery.form.js"></script>\r\n    <script src="')
        __M_writer(str( STATIC_URL ))
        __M_writer('homepage/media/jquery.loadmodal.js"></script>\r\n    <!-- Latest compiled and minified CSS -->\r\n    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">\r\n    <!-- Latest compiled and minified JavaScript -->\r\n    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/js/bootstrap.min.js"></script>\r\n    <!-- Optional theme -->\r\n    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap-theme.min.css">\r\n    <link rel="stylesheet" type="text/css" href="/static/homepage/styles/style.css"/>\r\n\r\n')
        __M_writer('    ')
        __M_writer(str( static_renderer.get_template_css(request, context)  ))
        __M_writer('\r\n\r\n</head>\r\n<body>\r\n\r\n<header class="top">\r\n    <nav class="navbar navbar-default">\r\n        <div class="container-fluid">\r\n            <!-- Brand and toggle get grouped for better mobile display -->\r\n            <div class="navbar-header">\r\n                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse"\r\n                        data-target="#bs-example-navbar-collapse-1">\r\n                    <span class="sr-only">Toggle navigation</span>\r\n                    <span class="icon-bar"></span>\r\n                    <span class="icon-bar"></span>\r\n                    <span class="icon-bar"></span>\r\n                </button>\r\n                <a class="navbar-brand" href="/homepage/">Colonial Heritage Foundation</a>\r\n            </div>\r\n\r\n            <!-- Collect the nav links, forms, and other content for toggling -->\r\n            <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">\r\n                <ul class="nav navbar-nav">\r\n                    <li class="dropdown" id="test1">\r\n                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">\r\n                            Shop<span class="caret"></span></a>\r\n                        <ul class="dropdown-menu" role="menu">\r\n                            <li><a href="/homepage/product/">Products</a></li>\r\n                            <li class="divider"></li>\r\n                            <li><a href="/homepage/rental/">Rentals</a></li>\r\n                            <li class="divider"></li>\r\n                            <li><a href="/homepage/mto_product/">Made-to-Order</a></li>\r\n                        </ul>\r\n                    </li>\r\n                    <li class="dropdown">\r\n                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">\r\n                            Events<span class="caret"></span></a>\r\n                        <ul class="dropdown-menu" role="menu">\r\n                            <li><a href="/homepage/event/">Events</a></li>\r\n                            <li class="divider"></li>\r\n                            <li><a href="/homepage/area/">Areas</a></li>\r\n                        </ul>\r\n                    </li>\r\n                    <li class="dropdown">\r\n                        <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">\r\n                            Admin<span class="caret"></span></a>\r\n                        <ul class="dropdown-menu" role="menu">\r\n                            <li><a href="/homepage/overdue_rental/">Overdue Items</a></li>\r\n                            <li class="divider"></li>\r\n                            <li><a href="/homepage/user/">Users</a></li>\r\n                            <li class="divider"></li>\r\n                            <li><a href="/homepage/rental_return/">Rental Return</a></li>\r\n                        </ul>\r\n                    </li>\r\n                </ul>\r\n')
        __M_writer('                                <ul class="nav navbar-nav navbar-right">\r\n                <li class="dropdown">\r\n                <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">\r\n')
        if request.user.is_authenticated():
            __M_writer('                    ')
            __M_writer(str( "Welcome, " + request.user.first_name +' '+ request.user.last_name ))
            __M_writer('\r\n                        <span class="caret"></span></a>\r\n                        <ul class = "dropdown-menu" role="menu">\r\n                            <li><a href="/homepage/account/')
            __M_writer(str( request.user.id ))
            __M_writer('/')
            __M_writer(str( request.user.address_id ))
            __M_writer('">Account</a></li>\r\n                            <li><a href="/homepage/login.logout">Sign Out</a></li>\r\n                        </ul>\r\n')
        else:
            __M_writer('                    ')
            __M_writer(str( "Not Signed In" ))
            __M_writer('\r\n                        <span class="caret"></span></a>\r\n                        <ul class="dropdown-menu" role="menu">\r\n                            <li><a href id="show_login_dialog" data-toggle="modal" data-target="#login_dialog">Sign In</a></li>\r\n                            <li><a href="/homepage/user.create/">Create Account</a></li>\r\n                        </ul>\r\n')
        __M_writer('                </li>\r\n            </ul>\r\n            </div>\r\n            <!-- /.navbar-collapse -->\r\n        </div>\r\n        <!-- /.container-fluid -->\r\n    </nav>\r\n</header>\r\n\r\n<div id="center">\r\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer('\r\n</div>\r\n\r\n')
        __M_writer('    ')
        __M_writer(str( static_renderer.get_template_js(request, context) ))
        __M_writer('\r\n<!-- Modal -->\r\n<div class="modal fade" id="shoppingCart" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\r\n    <div class="modal-dialog">\r\n        <div class="modal-content">\r\n            <div class="modal-header">\r\n                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\r\n                <h4 class="modal-title" id="myModalLabel">Shopping Cart</h4>\r\n            </div>\r\n            <div class="modal-body">\r\n\r\n            </div>\r\n            <div class="modal-footer">\r\n                <button type="button" class="btn btn-default" data-dismiss="modal">Continue Shopping</button>\r\n                <a href = "/homepage/checkout/"><button id="checkout_button" type="button" class="btn btn-primary">Checkout</button></a>\r\n            </div>\r\n        </div>\r\n    </div>\r\n</div>\r\n\r\n</body>\r\n<footer class="footer_center_bottom">\r\n    <span id="log_current_date">')
        __M_writer(str( datetime.datetime.now() ))
        __M_writer('</span>\r\n')
        __M_writer('    </footer>\r\n\r\n<!-- javascript -->\r\n')
        __M_writer('\r\n</html>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def content():
            return render_content(context)
        __M_writer = context.writer()
        __M_writer('\r\n        Site content goes here in sub-templates.\r\n    ')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "C:\\Users\\Kevin\\Documents\\GitHub\\CHFIntex2\\homepage\\templates/base.htm", "line_map": {"67": 134, "68": 138, "69": 138, "70": 138, "71": 160, "72": 160, "73": 164, "74": 168, "16": 4, "92": 86, "18": 6, "80": 132, "22": 0, "86": 132, "32": 2, "33": 4, "34": 5, "38": 5, "39": 8, "40": 19, "41": 30, "42": 32, "43": 32, "44": 33, "45": 33, "46": 43, "47": 43, "48": 43, "49": 104, "50": 107, "51": 108, "52": 108, "53": 108, "54": 111, "55": 111, "56": 111, "57": 111, "58": 114, "59": 115, "60": 115, "61": 115, "62": 122}, "source_encoding": "ascii", "uri": "base.htm"}
__M_END_METADATA
"""
