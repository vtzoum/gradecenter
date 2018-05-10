#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import datetime
import decimal
import json
import os

from django.db.models.base import ModelState
from django.http import Http404, HttpResponse,HttpResponseRedirect, HttpResponseNotFound  
from django.core.exceptions import PermissionDenied

from functools import wraps

from django import template 
from django.contrib.auth.models import Group 

from django.contrib.auth.decorators import user_passes_test


try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

from django.http import HttpResponseForbidden, Http404

###################################
# VIEW DECORATORS
###################################
"""
Sometimes I don't want to reveal a staff-only view so I created this decorator,
using django.contrib.admin.views.decorators.staff_member_required as my boilerplate. 
Non staff members are kicked to the 404 curb.

Suggestion: Create a file, decorators.py in your project (or single app) 
and import like so: from myproject.app_name.decorators import staff_or_404.
"""

def staff_or_404(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, raising a 404 if necessary.
    """
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            # The user is valid. Continue to the admin page.
            return view_func(request, *args, **kwargs)

        else:   
            raise Http404

    return wraps(view_func)(_checklogin)

from django.core.exceptions import PermissionDenied
"""
Decorator for views that checks that the user is logged in and is a staff
member, raising a 403 if necessary.
"""
def staff_or_403(view_func):
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            # The user is valid. Continue to the admin page.
            return view_func(request, *args, **kwargs)

        else:   
            raise PermissionDenied
            return HttpResponseForbidden('Forbidden')
            #raise Http404

    return wraps(view_func)(_checklogin)


def staff_or_401(view_func):
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            # The user is valid. Continue to the admin page.
            return view_func(request, *args, **kwargs)

        else:   
            return HttpResponse('Unauthorized', status=401)
            #raise Http404

    return wraps(view_func)(_checklogin)




"""
This snippet provides a @group_required decorator. You can pass in multiple groups, for example:

@group_required('admins','editors')
def myview(request, id):
...
Note: the decorator is based on the snippet here but extends it 
checking first that the user is logged in before testing for group membership - 
user_passes_test does not check for this by default.

It is important to check that the user is first logged in, 
as anonymous users trigger an AttributeError when the groups filter is executed.
"""
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    
    return user_passes_test(in_groups)

""" My try """
def group_required_or_403(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        raise PermissionDenied
        return HttpResponse('Unauthorized', status=401)
    
    return user_passes_test(in_groups)



"""
JSON decorator for views handling ajax requests   

Here is the view:
@ajax_login_required
def ajax_update_module(request, module_slug, action):
    # Etc ...
    return HttpResponse(json, mimetype='application/json')

And here is the JavaScript (jQuery):
$.post('/restricted-url/', data, function(json) {
    if (json.not_authenticated) {
        alert('Not authorized.');  // Or something in a message DIV
        return;
    }
    // Etc ...
});
"""
def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        #else#1
        raise PermissionDenied
        #else#2
        json = json.dumps({ 'not_authenticated': True })
        return HttpResponse(json, mimetype='application/json')
    return wrapper


"""
A view decorator that sends the user back to the last page after the view
logic executes. Useful for actions that don't change the page the user is 
looking at. One example is clicking on a link to mark a message as read.
The messages view is refreshed, with that item marked as read.
"""
from django.http import HttpResponseRedirect
def back_to_referrer(f):
    
    def new_f(*args, **kwargs):        
        f(*args, **kwargs)
        request = args[0]
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
            
    return new_f


""" 
JSON decorator for views handling ajax requests   

Sample usage for using decorator 
@json_response(ajax_required=True, login_required=True) 
def subscribe(request): 
    return {"status":"success"}

Converts a function returning dict into json response. 
Does is_ajax check and user authenticated check if set in flags. 
When function returns HttpResponse does nothing.σ

"""
class json_response(object):
    def __init__(self, login_required = False, ajax_required = False):
        self.login_required = login_required
        self.ajax_required = ajax_required
    def __call__(self, func):
        class_args = self
        def decorator(request, *args, **kwargs):
            if class_args.login_required and not request.user.is_authenticated():
                objects = {
                    "status": "error",
                    "msg": "User not authenticated"
                }
            elif class_args.ajax_required and not request.is_ajax():
                objects = {
                    "status": "error",
                    "msg": "Request gone wrong :("
                }
            else:
                objects = func(request, *args, **kwargs)
            
            if isinstance(objects, HttpResponse):
                return objects
            try:
                data = simplejson.dumps(objects)
                if 'callback' in request.REQUEST:
                    # a jsonp response!
                    data = '%s(%s);' % (request.REQUEST['callback'], data)
                    return HttpResponse(data, "text/javascript")
            except:
                data = json.dumps(str(objects))
            return HttpResponse(data, "application/json")
        
        return decorator

 
