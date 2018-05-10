#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Update.B2 to support Jinja2 CUSTOM extensions @ 20161021 
from jinja2 import lexer, nodes
from jinja2.ext import Extension
from django.utils import timezone
from django.template.defaultfilters import date
from django.conf import settings
from datetime import datetime

"""
In Django templates when you want to output the current date or time, there's a tag named {% now %} for just this purpose, 
Jinja has no such statement, so I'll create a Jinja extension to mimic the same behavior as the Django template {% now %} tag. 
The Jinja {% now %} statement will function just like the Django template version and accept a format string, 
as well as the possibility to use the as keyword to define a variable with the value.

Listing 2 illustrates the source code for the custom Jinja extension that produces a Jinja {% now %} statemen
"""
class DjangoNow(Extension):
    tags = set(['now'])

    def _now(self, date_format):
        tzinfo = timezone.get_current_timezone() if settings.USE_TZ else None
        formatted = date(datetime.now(tz=tzinfo),date_format)
        return formatted


    def parse(self, parser):
        lineno = next(parser.stream).lineno
        token = parser.stream.expect(lexer.TOKEN_STRING)
        date_format = nodes.Const(token.value)
        call = self.call_method('_now', [date_format], lineno=lineno)
        token = parser.stream.current
        if token.test('name:as'):
            next(parser.stream)
            as_var = parser.stream.expect(lexer.TOKEN_NAME)
            as_var = nodes.Name(as_var.value, 'store', lineno=as_var.lineno)
            return nodes.Assign(as_var, call, lineno=lineno)
        else:
            return nodes.Output([call], lineno=lineno)
