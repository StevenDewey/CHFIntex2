# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1428532920.415948
_enable_loop = True
_template_filename = 'C:\\Users\\Kevin\\Documents\\GitHub\\CHFIntex2\\homepage\\templates/event.html'
_template_uri = 'event.html'
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
        events = context.get('events', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\r\n\r\n<html>\r\n<body>\r\n<<<<<<< HEAD\r\n    ')
        if 'parent' not in context._data or not hasattr(context._data['parent'], 'content'):
            context['self'].content(**pageargs)
        

        __M_writer('\r\n</body>\r\n</html>\r\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_content(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        def content():
            return render_content(context)
        events = context.get('events', UNDEFINED)
        __M_writer = context.writer()
        __M_writer('\r\n\r\n        <head>\r\n            <title>Events</title>\r\n        </head>\r\n\r\n<div class="text-right">\r\n</div>\r\n    <div class="tableContain">\r\n    <h1>Events</h1>\r\n        <div id="Displayevents">\r\n            <div class="displaystuff">\r\n')
        for event in events:
            __M_writer('                <div class="eventstuff">\r\n                    <div class="eventDiv">\r\n                        <a href="/homepage/event_detail/')
            __M_writer(str( event.id ))
            __M_writer('">\r\n                          <img src="')
            __M_writer(str( event.photo.image ))
            __M_writer('"/>\r\n                          <div class="mid"> ')
            __M_writer(str( event.name ))
            __M_writer('</div>\r\n                        </a><br>\r\n                        <p><b>Dates:</b> ')
            __M_writer(str( event.start_date ))
            __M_writer(' - ')
            __M_writer(str( event.end_date ))
            __M_writer('</p>\r\n                        <p><b>Venue:</b> ')
            __M_writer(str( event.venue_name ))
            __M_writer('</p>\r\n                    </div>\r\n                </div>\r\n')
        __M_writer('            </div>\r\n        </div>\r\n    </div>\r\n ')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"filename": "C:\\Users\\Kevin\\Documents\\GitHub\\CHFIntex2\\homepage\\templates/event.html", "line_map": {"64": 25, "65": 25, "66": 26, "35": 1, "68": 30, "40": 33, "74": 68, "46": 6, "59": 22, "67": 26, "53": 6, "54": 18, "55": 19, "56": 21, "57": 21, "58": 22, "27": 0, "60": 23, "61": 23, "62": 25, "63": 25}, "source_encoding": "ascii", "uri": "event.html"}
__M_END_METADATA
"""
