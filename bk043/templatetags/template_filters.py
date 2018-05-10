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

"""
Check if user belongs to a group in django templates 
And in your template you can use it this way: 

{% if request.user|has_group:"mygroup" %} 
    <p>User belongs to my group 
{% else %} 
    <p>User doesn't belong to mygroup</p> 
{% endif %} 

http://www.abidibo.net/blog/2014/05/22/check-if-user-belongs-group-django-templates/#sthash.2jYtadbq.dpuf
"""
register = template.Library() 
@register.filter(name='has_group') 
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False 

@register.filter
def lower(value):
    return value.lower()


 
