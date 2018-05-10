#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse


from django.views.debug import technical_500_response
import sys


class AuthRequiredMiddleware(object):
    def process_request(self, request):
        if not request.user.is_authenticated():
            #return HttpResponseRedirect(reverse('base')) # or http response
            return HttpResponseRedirect('/home/')
        return None


"""
Normal users will get your 500.html when debug = False, 
but If you are logged in as a super user then you get to see the stack trace in all its glory.
"""
class UserBasedExceptionMiddleware(object):
    def process_exception(self, request, exception):
        if request.user.is_superuser:
            return technical_500_response(request, *sys.exc_info())
