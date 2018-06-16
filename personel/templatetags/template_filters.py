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


from personel.helpScripts import td2DayHourMin


################################
# MUST
################################                              
register = template.Library() 


################################
# TAGS
################################ 
"""
{% define "Create" as action %}
Would you like to {{action}} this item
"""
@register.assignment_tag
def define(val=None):
  return val

register = template.Library()
register.tag('define', define)

"""
Now you may use the get_addressee template tag in your templates:
{% get_addressee as addressee %}
<h1>hello {{addressee}}</h1>
"""
@register.assignment_tag
def get_addressee():
    return "World"

################################
# TAGS1 Assign var
################################   
class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''

def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.
    
    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}
        
    """
    #bits = token.contents.split()
    bits = token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    value = parser.compile_filter(bits[2])
    return AssignNode(bits[1], value)

register = template.Library()
register.tag('assign', do_assign)


################################
# TAG2 Set var =  val
# http://www.soyoucode.com/2011/set-variable-django-template
################################                              
"""
Then to use this in your template, you just do the following:
{% load set_var %}
 
{% set a = 3 %}
{% set b = some_context_variable %}
{% set c = "some string" %}
 
Value of a is {{a}}
Value of b is {{b}}
Value of c is {{c}}
"""
class SetVarNode(template.Node):
 
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value
 
    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""
 
def set_var(parser, token):
    """
        {% set <var_name>  = <var_value> %}
    """
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])
 
register.tag('set', set_var)


################################
# FILTERS
################################                              
@register.filter()
def boldcoffee(value):
    '''Returns input wrapped in HTML  tags'''
    return '%s' % value

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



###################################
# FILTERS
###################################
@register.filter(name='get_group') 
def get_group_id(user): 
    try:
        group_id = Group.objects.get(name=group_name).id
    except Group.DoesNotExist:
       group_id = None
    return group_id 

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
@register.filter(name='has_group') 
def has_group(user, group_name): 
    try:
        group = Group.objects.get(name=group_name) 
    except Group.DoesNotExist:
       group = None
    return True if group in user.groups.all() else False 

@register.filter
def lower(value):
    return value.lower()


################################
# 2018
################################ 
@register.filter(name='td2DayHourMin') 
def td2DayHourMin(time): 
    return td2DayHourMin(time)



