#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Update.1 to support Jinja2 filters @ 20161021 

import jinja2

import ast
import datetime
import decimal
import json
import os

from django import template
from django.contrib.auth.models import Group 
from django.core.exceptions import PermissionDenied
from django.db.models.base import ModelState
from django.http import Http404, HttpResponse,HttpResponseRedirect, HttpResponseNotFound  

from functools import wraps


from personel.helpScripts import td2DayHourMin
from personel.models import *


def customcoffee(value,arg="muted"):
    return jinja2.Markup('%s' % (arg,value))

import math

def squarerootintext(value):
    return "The square root of %s is %s" % (value,math.sqrt(value))

def startswithvowel(value):
    if value.lower().startswith(("a", "e", "i", "o","u")):
        return True
    else:
        return False     



#############################################
# 2018 
#############################################
def lexLessonType(id):
    return Lesson.lexLessonType(Lesson,id)

def lexFolderCodeType(id):
    return Folder.lexCodeType(Folder,id)


def lexFolderCodeLocation(id):
    return Folder.lexCodeLocation(Folder,id)


def lexFolderCodeStatus(id):
    return Folder.lexCodeStatus(Folder,id)


#############################################
# 
#############################################
def has_group(user, group_name): 
    try:
        group = Group.objects.get(name=group_name) 
    except Group.DoesNotExist:
       group = None
    return True if group in user.groups.all() else False 


#############################################
# Returns tuple (name, StationID)
#############################################
def jinjaCheckGroup(user): 

    user_groups = user.groups.all().values_list('name')
    print "user_groups:", user_groups 

    group = Group.objects.get(name="Grammateia") 
    if ("Admin",) in user_groups:
        return (u'ΔΙΑΧΕΙΡΙΣΤΗΣ', 2)
        #return <input id='StationID' name='ΓΡΑΜΜΑΤΕΙΑ' value='2' type="hidden"/>
        #{% set stationID=2 %}

    elif ("Grammateia",) in user_groups:
        return (u'ΓΡΑΜΜΑΤΕΙΑ', 2)
        #return <input id='StationID' name='ΓΡΑΜΜΑΤΕΙΑ' value='2' type="hidden"/>
        #{% set stationID=2 %}

    elif ("Filaxi",) in user_groups:
        return (u'ΦΥΛΑΞΗ', 1)
        #<input id='StationID' name='ΦΥΛΑΞΗ' value='1' type="hidden"/>
        #{% set stationID=1 %}

    elif ("Apothiki",) in user_groups:
        return (u'ΑΠΟΘΗΚΗ', 0)
        #<input id='StationID' name='ΑΠΟΘΗΚΗ' value='0' type="hidden"/>
        #{% set stationID=0 %}

    else:
        return ('Error', -1)
        #<input id='StationID' name='Error' value='-1' type="hidden"/>
        #{% set stationID=-1 %}


#def lower(value):
#    return value.lower()

