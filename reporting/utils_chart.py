#!/usr/bin/python
# -*- coding: utf-8 -*-

import json 
from random import choice
from reportlab.lib.colors import HexColor
from personel.models  import *

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext


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
        lt='0'
    elif ftype==1:
        lt='1'
    elif ftype==2:
        lt='2'
    return lt+ls
    	
#test
# label (0,1)


#################################################
# Tranforms Dict from Django Aggregates -> 
# for JQX Chart Data
#################################################
def lessonKey(name, type):
    lex = SchoolToGrade.lexSchoolToGradeType(SchoolToGrade,type)
    return name + '('+lex[:4] +')'
    #return name + '('+str(type) +')'

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
        #iDict[k] = dict.fromkeys(['AB','A0','A1','A2', 'B0','B1','B2', 'C0','C1','C2'], 0) # a nullDIct / Lesson
        iDict[k] = dict.fromkeys(['AB','C', '00','01','02', '10','11','12', '20','21','22'], 0) # a nullDIct / Lesson
    #print iDict 
    #print 'iDict-null--'*40
    pass
    #populate # d{lesson] <- counts / folder_types
    for i in aDictL:
        key1 = lessonKey (i['LessonID__name'], i['LessonID__type'])
        #key1 = i['LessonID__name']# lesson name as key1
        key2 = label(i['codeType'], i['codeStatus'])# label as key2
        d = iDict[key1]
        d[key2] = i['countCodeType']
        d['AB'] = i['LessonID__booksABFolders']
        d['C'] = i['LessonID__booksCFolders']
        #print key1, key2,   i['countCodeType']
        #print d
    pass
    fDictL = []
    for k, v in iDict.iteritems():
        d={}
        #d['Lesson'] = k.encode('utf-8')
        #d['Lesson'] = k.encode('iso8859-7')
        d['LessonID__name'] = json.dumps(k)         #OK
        d['data'] = v
        fDictL.append(d)
    pass
    #print fDictL
    #print 'fDictL--Less/Data-'*30
    #Final form
    for i in fDictL:
        i.update(i['data'])
        i.pop('data')
        i['02'] = i['AB'] -i['00'] -i['01']  # Update A-Complete via Simple arithmetics
        #print i
    pass
    #print fDictL
    #print 'fDictL--FINAL-'*30
    return fDictL

#TEst 
#chartData = makeDict4ChartData(data)
#chartData



def makeDict4ChartData__PIE(aDictL):
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
        #iDict[k] = dict.fromkeys(['AB','A0','A1','A2', 'B0','B1','B2', 'C0','C1','C2'], 0) # a nullDIct / Lesson
        iDict[k] = dict.fromkeys(['AB','00','01','02', '10','11','12', '20','21','22'], 0) # a nullDIct / Lesson
    #print iDict 
    #print 'iDict-null--'*40
    pass
    #populate # d{lesson] <- counts / folder_types
    for i in aDictL:
        key1 = lessonKey (i['LessonID__name'], i['LessonID__type'])
        #key1 = i['LessonID__name']# lesson name as key1
        key2 = label(0, i['codeStatus'])# label as key2
        d = iDict[key1]
        d[key2] = i['countCodeStatus']
        #d['AB'] = i['AB']
    pass
    fDictL = []
    for k, v in iDict.iteritems():
        d={}
        d['Lesson'] = json.dumps(k)         #OK
        d['data'] = v
        fDictL.append(d)
    #print fDictL
    return fDictL



#TEst 
#fDict = makeDict4ChartData(DictLB)
"""    
DictL2 = [{'Lesson': 'A', 'AB':30,'A0':8,'A1':5,'A2':0, 'B0':6,'B1':4,'B2':7, 'C0':1,'C1':1,'C2':0}, 
            {'Lesson': 'B', 'AB':22,'A0':4,'A1':5,'A2':0, 'B0':4,'B1':4,'B2':5, 'C0':0,'C1':2,'C2':1},
        ]
"""   




