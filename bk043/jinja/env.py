#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Update.1 to support Jinja2 globals @ 20161021 
from jinja2.environment import Environment
from django.contrib import messages
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.urlresolvers import reverse
#Update.B1 to support Jinja2 filters @ 20161021 

from bk043.jinja.filters import customcoffee, jinjaCheckGroup, has_group, squarerootintext, startswithvowel,\
        lexLessonType, lexFolderCodeType, lexFolderCodeLocation, lexFolderCodeStatus, td2DayHourMin

#Update.B2 to support Messages @ 201704
#from __future__ import absolute_import  # Python 2 only


class JinjaEnvironment(Environment):
    def __init__(self,**kwargs):
        super(JinjaEnvironment, self).__init__(**kwargs)
        #globals
        self.globals['static'] = staticfiles_storage.url
        self.globals['reverse'] = reverse
        self.globals['url'] = reverse
        self.globals['messages'] = messages
        self.globals['get_messages'] = messages.get_messages
        #self.globals['user'] = user

        self.globals['jinjaCheckGroup'] = jinjaCheckGroup

        #B.filters
        self.filters['customcoffee'] = customcoffee
        self.filters['jinjaCheckGroup'] = jinjaCheckGroup
        self.filters['has_group'] = has_group
        self.filters['squarerootintext'] = squarerootintext
        self.filters['startswithvowel'] = startswithvowel        
        
        #2018
        self.filters['td2DayHourMin'] = td2DayHourMin
        self.filters['lexLessonType'] = lexLessonType
        self.filters['lexFolderCodeType'] = lexFolderCodeType        
        self.filters['lexFolderCodeLocation'] = lexFolderCodeLocation
        self.filters['lexFolderCodeStatus'] = lexFolderCodeStatus


        #B.tests
        self.tests['has_group'] = has_group        
        self.tests['startswithvowel'] = startswithvowel        
