#!/usr/bin/python
# -*- coding: utf-8 -*-

import json 
from random import choice
from reportlab.lib.colors import HexColor
from personel.models  import *

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

import datetime
from datetime import date, timedelta
import time
import StringIO
import xlsxwriter

from django.db.models import Avg, Sum, Max, Min, Count
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils.translation import ugettext, ugettext_lazy as _


from docx import Document
from docx.shared import Inches, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH

from personel.models import *
from personel.helpScripts import td2DayHourMin

#from reporting.utils import *
#from reporting.utils_chart import *
#from .utils import get_temperatures, get_wind_speed, get_str_days, get_random_colors, precip_prob_sum, get_percentage, legendcolors = get_random_colors(10)



####################################################
# To Optimize
####################################################
def label(ftype, fstatus):
    if fstatus==0:
        ls='0'
    elif fstatus==1:
        ls='1'
    elif fstatus==2:
        ls='2'
    if ftype==0:
        lt='A'
    elif ftype==1:
        lt='B'
    elif ftype==2:
        lt='C'
    return lt+ls
    	
#test
# label (0,1)


#################################################
# Tranforms Dict from Django Aggregates -> 
# for JQX Chart Data
#################################################
def lessonKey(name, type):
    return name + '('+str(type) +')'

def makeDict4ChartData(aDictL):
    #A.Get unique lesson names    
    #keys = [ i['LessonID__name'] for i in aDict]
    keys = []
    for i in aDictL:
        key = lessonKey (i['LessonID__name'], i['LessonID__type'])
        keys.append(key)
    #keys = [ i['LessonID__name'] for i in aDictL]
    keys = list(set(keys))
    #print keys
    
    #B.init DictL2 
    iDict = {}
    for k in keys:
        iDict[k] = dict.fromkeys(['AB','A0','A1','A2', 'B0','B1','B2', 'C0','C1','C2'], 0) # a nullDIct / Lesson
    print iDict 
    #print 'iDict-null--'*40
    pass
    #populate # d{lesson] <- counts / folder_types
    for i in aDictL:
        key1 = lessonKey (i['LessonID__name'], i['LessonID__type'])
        #key1 = i['LessonID__name']# lesson name as key1
        key2 = label(i['codeType'], i['codeStatus'])# label as key2
        d = iDict[key1]
        d[key2] = i['countCodeType']
        #d['AB'] = i['AB']
        print key1, key2,   i['countCodeType']
        print d
    pass
    fDictL = []
    for k, v in iDict.iteritems():
        d={}
        #d['Lesson'] = k.encode('utf-8')
        #d['Lesson'] = k.encode('iso8859-7')
        d['Lesson'] = json.dumps(k)         #OK
        d['data'] = v
        fDictL.append(d)
    pass
    print fDictL
    print 'fDictL--Less/Data-'*30
    #Final form
    for i in fDictL:
        i.update(i['data'])
        i.pop('data')
        #print i
    pass
    #print fDictL
    return fDictL

#TEst 
chartData = makeDict4ChartData(data)
chartData


"""    
DictL2 = [{'Lesson': 'A', 'AB':30,'A0':8,'A1':5,'A2':0, 'B0':6,'B1':4,'B2':7, 'C0':1,'C1':1,'C2':0}, 
            {'Lesson': 'B', 'AB':22,'A0':4,'A1':5,'A2':0, 'B0':4,'B1':4,'B2':5, 'C0':0,'C1':2,'C2':1},
        ]
"""   

########################################3
# CODE TO TEST
########################################3
#Lesson as filter
LessonID = None 
lesson = None
data = Folder.objects.all()
 
data = data.values('codeStatus', 'codeType', 'LessonID', 'LessonID__name', 'LessonID__type',)\
    .annotate(countCodeType=Count('codeType'), countCodeStatus=Count('codeStatus'), )\
    .order_by('LessonID__name', 'LessonID__type', 'codeType')

sums = data.values('codeType', 'countCodeType', 'codeStatus', 'LessonID', 'LessonID__name', 'LessonID__type',)\
    .order_by('LessonID','codeType')


print data

chartData = makeDict4ChartData(data)
"""    
fDict = [{'Lesson': 'A', 'AB':30,'A0':8,'A1':5,'A2':0, 'B0':6,'B1':4,'B2':7, 'C0':1,'C1':1,'C2':0}, 
            {'Lesson': 'B', 'AB':22,'A0':4,'A1':5,'A2':0, 'B0':4,'B1':4,'B2':5, 'C0':0,'C1':2,'C2':1},
        ]
"""

print chartData



