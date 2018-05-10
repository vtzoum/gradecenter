#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import os, time
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse,HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
#from django.views.generic import CreateView, View
#from django.views.generic.edit import CreateView, DeleteView, UpdateView
#from django.forms.models import model_to_dict
from django.db.models import QuerySet
from django.db import IntegrityError, transaction

from models import Grader, Lesson, Teacher, School, SchoolToGrade, Specialty

""" 

M:N Relation > QuerySet Values to JSON 

"""
def jsonFolderCrud(request):
    
    dictData = []
    #action = request.POST.get('action', '') if ( request.method == 'POST' ) else request.GET.get( 'action', '' )
    #print action

    # GET * SELECT 
    if request.is_ajax() and request.method == 'GET':
        action = request.GET.get('action', None)
        print 'get', action
        
        if (action=="filter"):
            LessonID = request.GET.get('LessonID', None)
            #dictData = Folder.objects.get(LessonID=LessonID).graders.all().values()   #OK
            dictData = Folder.objects.filter(LessonID=LessonID).values()             
            jsonData = json.dumps(list(dictData))
            #print jsonData
            return HttpResponse(jsonData, content_type='application/json')
    
    # POST INS.UPD.DEL
    if request.is_ajax() and request.method == 'POST':
        action = request.POST.get('action', None)
        #print 'POST', action

        #INSERT COMMAND (need related LessonID )
        if (action=="insert"):
            LessonID = request.POST.get('LessonID', None)        
            no = request.POST.get('no', None)
            books = request.POST.get('books', None)#.title()
            type = request.POST.get('type', None)#.title()
            #status = request.POST.get('status', None)
            print 'Data:',  no, books, type
            no = Lesson.objects.get(id=LessonID).getNextFolderNo(type = type)
            print 'Data(new):',  no, books, type

            Folder(LessonID_id = LessonID, no = no, books = books, type = type).save()
            #t0.save() # Succeeds, but may be undone by transaction rollback
            #c.save() # Succeeds, but a.save() may have been undone
            dictData = "Success"
            #print dictData
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')
        
        # UPDATE
        if (action=="update"):
            id = request.POST.get('id', None)
            no = request.POST.get('no', None)
            books = request.POST.get('books', None)
            type = request.POST.get('type', None)
            #status = request.POST.get('status', None)

            record = FolderLesson.objects.filter(id=id)
            record.update( no = no, books = books, type = type,)
            #Folder.objects.filter(id=id).update(isCoordinator = helperStr2Bool(isCoordinator), isgraderC = helperStr2Bool(isgraderC), status = status, )           
            
            # return Lesson record
            dictData = record.values()
            jsonData = json.dumps(list(dictData))
            #print jsonData
            return HttpResponse(jsonData, content_type='application/json')


        #DELETE COMMAND
        if (action=="delete"):
            id = request.POST.get('id', None)
            record = Folder.objects.filter(id=id)
            try:
                record.delete()
                result = "Folder (%s) deleted successfully." %(record)
            except IntegrityError:
                transaction.rollback()   
                result = "Error Folder (%s) could not be deleted." %(record)
            return HttpResponse(result, content_type='application/json')


    #"Default SELECT(*) "
    dictData = Folder.objects.all().values()
    #print dictData
    jsonData = json.dumps(list(dictData))
    return HttpResponse(jsonData, content_type='application/json')



""" QuerySet Values to JSON """
def jsonLessonCrud(request):
    
    # Display on GET 
    if request.is_ajax() and request.method == 'GET':
        id  = request.GET.get('id', None)
        action = request.GET.get('action', None)
        
        if (action=="filter"):
            dictData = Lesson.objects.filter(id=id).values()
        else: 
            dictData = Lesson.objects.all().values()
        #print dictData
        jsonData = json.dumps(list(dictData))
        return HttpResponse(jsonData, content_type='application/json')

    # CRUD on POST 
    if request.is_ajax() and request.method == 'POST':
        action = request.POST.get('action', None)
        #dictData = Lesson.objects.all().values()

        #ADD
        if (action=="add"):
            #Fakeloi 1o 2o xeri (AB)
            #booksAB = models.IntegerField(default=0, blank=False)
            #booksABFolders = models.IntegerField(default=0, blank=False)    
            #booksC = request.POST.get('booksC', None)
            #booksCFolders = request.POST.get('booksCFolders', None)
            category = request.POST.get('category', None)
            name = request.POST.get('name', None)
            type = request.POST.get('type', None)     

            record = Folder(category = category, name = name, type = type)
            record.save()

            # return record            
            dictData = Lesson.objects.filter(id=record.id).values()             
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')
        
        # UPDATE 
        elif (action=="update"):
            id = request.POST.get('id', None)
            #Fakeloi 1o 2o xeri (AB)
            #booksAB booksABFolders 
            booksC = request.POST.get('booksC', None)
            booksCFolders = request.POST.get('booksCFolders', None)
            category = request.POST.get('category', None)
            name = request.POST.get('name', None)
            type = request.POST.get('type', None)            
            
            record = Lesson.objects.filter(id=id)
            record.update( booksC = booksC, booksCFolders = booksCFolders, category = category, name=name , type = type, )
            
            # return Lesson record
            dictData = record.values()
            jsonData = json.dumps(list(dictData))
            #print jsonData
            return HttpResponse(jsonData, content_type='application/json')

        #DELETE
        if (action=="delete"):
            id = request.POST.get('id', None)
            record = Lesson.objects.filter(id=id)
            try:
                record.delete()
                result = "Lesson (%s) deleted successfully." %(record.name)
            except IntegrityError:
                transaction.rollback()   
                result = "Error Lesson (%s) could not be deleted." %(record.name)
            return HttpResponse(result, content_type='application/json')

        
        # else: No POST Default 
    
    # DEFAULT 
    else: 
        dictData = Lesson.objects.all().values()
        jsonData = json.dumps(list(dictData))
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')
 

""" 
CRUD for SchoolToGrade 

code name  ddeCode ddeName type = IntegerField(choices=SCHOOL_TYPE, default=1)   
"""
def jsonSchoolToGradeCrud(request):
        
    if request.is_ajax() and request.method == 'GET':
        id = request.GET.get('id', None)
        action = request.GET.get('action', None)
        
        if (action=="filter"):
            dictData = SchoolToGrade.objects.filter(id=id).values()
        else: 
            dictData = SchoolToGrade.objects.all().values()
        #print dictData
        jsonData = json.dumps(list(dictData))
        return HttpResponse(jsonData, content_type='application/json')

    if request.is_ajax() and request.method == 'POST':
        action = request.POST.get('action', None)

        #ADD
        if (action=="add"):
            code = request.POST.get('code', None)
            name = request.POST.get('name', None)
            ddeCode = request.POST.get('ddeCode', None)
            ddeName = request.POST.get('ddeName ', None)
            type = request.POST.get('type', None)
                    
            record = SchoolToGrade(code = code , name = name, ddeCode = ddeCode, ddeName= ddeName, type = type).save()
            # return Lesson record            
            dictData = SchoolToGrade.objects.filter(id=record.id).values()             
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')

        #DELETE 
        if (action=="delete"):
            id = request.POST.get('id', None)
            record = SchoolToGrade.objects.filter(id=id)
            try:
                record.delete()
                result = "SchoolToGrade (%s) deleted successfully." %(record.name)
            except IntegrityError:
                transaction.rollback()   
                result = "Error SchoolToGrade (%s) could not be deleted." %(record.name)
            return HttpResponse(result, content_type='application/json')

        #UPDATE
        elif (action=="update"):
            id = request.POST.get('id', None)
            code = request.POST.get('code', None)
            name = request.POST.get('name', None)
            ddeCode = request.POST.get('ddeCode', None)
            ddeName = request.POST.get('ddeName', None)
            type = request.POST.get('type', None)

            record = SchoolToGrade.objects.filter(id=id)
            record.update( code = code , name = name, ddeCode = ddeCode, ddeName = ddeName, type = type )
            
            dictData = record.values()
            #print dictData
            jsonData = json.dumps(list(dictData))
            return HttpResponse(jsonData, content_type='application/json')


    # DEFAULT 
    else: 
        dictData = SchoolToGrade.objects.all().values()
        jsonData = json.dumps(list(dictData))
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')



""" 
CRUD for Specialty 
code name 
"""
def jsonSpecialtyCrud(request):
        
    if request.is_ajax() and request.method == 'GET':
        id = request.GET.get('id', None)
        action = request.GET.get('action', None)
        
        if (action=="filter"):
            dictData = Specialty.objects.filter(id=id).values()
        else: 
            dictData = Specialty.objects.all().values()
        #print dictData
        jsonData = json.dumps(list(dictData))
        return HttpResponse(jsonData, content_type='application/json')

    if request.is_ajax() and request.method == 'POST':
        action = request.POST.get('action', None)

        #ADD
        if (action=="add"):
            code = request.POST.get('code', None)
            name = request.POST.get('name', None)                    
            record = Specialty(code = code , name = name, ).save()
            dictData = Specialty.objects.filter(id=record.id).values()             
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')

        #DELETE 
        if (action=="delete"):
            id = request.POST.get('id', None)
            record = Specialty.objects.filter(id=id)
            try:
                record.delete()
                result = "Specialty (%s) deleted successfully." %(record.name)
            except IntegrityError:
                transaction.rollback()   
                result = "Error Specialty (%s) could not be deleted." %(record.name)
            return HttpResponse(result, content_type='application/json')

        #UPDATE
        elif (action=="update"):
            id = request.POST.get('id', None)
            code = request.POST.get('code', None)
            name = request.POST.get('name', None)
            record = Specialty.objects.filter(id=id)
            record.update( code = code , name = name, )            
            dictData = record.values()
            #print dictData
            jsonData = json.dumps(list(dictData))
            return HttpResponse(jsonData, content_type='application/json')


    # DEFAULT 
    else: 
        dictData = Specialty.objects.all().values()
        jsonData = json.dumps(list(dictData))
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')



""" 
CRUD for Specialty 
"""
def jsonSpecialtyCrudv0(request):
    
    if request.is_ajax() and request.method == 'GET':
        id = request.GET.get('id', None)
        action = request.GET.get('action', None)
        
        if (action=="filter"):
            dictData = SchoolToGrade.objects.filter(id=id).values()
        else: 
            dictData = SchoolToGrade.objects.all().values()
        #print dictData
        jsonData = json.dumps(list(dictData))
        return HttpResponse(jsonData, content_type='application/json')

    if request.is_ajax() and request.method == 'POST':
        action = request.POST.get('action', None)

        #ADD
        if (action=="add"):
            code = request.POST.get('code', None)
            name = request.POST.get('name', None)
                    
            record = Specialty(code = code , name = name )
            record.save()

            dictData = Specialty.objects.filter(id=record.id).values()             
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')

        #DELETE 
        if (action=="delete"):
            id = request.POST.get('id', None)
            record = Specialty.objects.filter(id=id)
            try:
                record.delete()
                result = "Specialty (%s) deleted successfully." %(record.name)
            except IntegrityError:
                transaction.rollback()   
                result = "Error Specialty (%s) could not be deleted." %(record.name)
            return HttpResponse(result, content_type='application/json')

        #UPDATE
        elif (action=="update"):
            id = request.POST.get('id', None)
            code = request.POST.get('code', None)
            name = request.POST.get('name', None)

            record = Specialty.objects.filter(id=id)
            record.update( code = code , name = name, )

            dictData = record.values()
            #print dictData
            jsonData = json.dumps(list(dictData))
            return HttpResponse(jsonData, content_type='application/json')
        else: 
            dictData = 'POST action Not Found'
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')
            #raise Http404
    # DEFAULT 
    else: 
        dictData = Specialty.objects.all().values()
        jsonData = json.dumps(list(dictData))
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')



""" 
CRUD for Teacher
fields: codeAfm codeGrad codeSpec name surname 
"""
def jsonTeacherCrud(request):
    
    # Display/Filter is only on GET
    if request.is_ajax() and request.method == 'GET':
        id = request.GET.get('id', None)
        action = request.GET.get('action', None)
        
        if (action=="filter"):
            dictData = Teacher.objects.filter(id=id).values()
        else: 
            dictData = Teacher.objects.all().values()
        #print dictData
        jsonData = json.dumps(list(dictData))
        return HttpResponse(jsonData, content_type='application/json')
    
    # CRUD is only on POST
    if request.is_ajax() and request.method == 'POST':
        action = request.POST.get('action', None)

        #ADD
        if (action=="add"):
            codeAfm = request.POST.get('codeAfm', None)
            codeGrad = request.POST.get('codeGrad', None)
            codeSpec = request.POST.get('codeSpec', None)
            surname = request.POST.get('surname', None)
            name = request.POST.get('name', None)
                    
            record = Teacher( codeAfm = codeAfm, codeGrad = codeGrad , codeSpec = codeSpec, surname = surname, name=name, ).save()
            # return Lesson record            
            dictData = Teacher.objects.filter(id=record.id).values()
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')

        #DELETE 
        if (action=="delete"):
            id = request.POST.get('id', None)
            record = Teacher.objects.filter(id=id)
            try:
                record.delete()
                result = "Teacher (%s) deleted successfully." %(record)
            except IntegrityError:
                transaction.rollback()   
                result = "Error Teacher (%s) could not be deleted." %(record)
            return HttpResponse(result, content_type='application/json')

        #UPDATE
        elif (action=="update"):
            id = request.POST.get('id', None)
            codeAfm = request.POST.get('codeAfm', None)
            codeGrad = request.POST.get('codeGrad', None)
            codeSpec = request.POST.get('codeSpec', None)
            surname = request.POST.get('surname', None)
            name = request.POST.get('name', None)

            record = Teacher.objects.filter(id=id)            
            record.update( codeAfm = codeAfm, codeGrad = codeGrad , codeSpec = codeSpec,surname = surname, name=name , )
            dictData = record.values()
            #print dictData
            jsonData = json.dumps(list(dictData))
            return HttpResponse(jsonData, content_type='application/json')
    
    # DEFAULT on View
    else: 
        dictData = Teacher.objects.all().values()
        jsonData = json.dumps(list(dictData))
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')
""" 
CRUD for Teacher 
"""
def jsonTeacherCrud_V0(request):
    
    if request.is_ajax():    
        #lg = request.GET.getlist('postData')
        action = request.GET.get('action', None)
        #INSERT COMMAND
        if (action=="insert"):
            codeAfm = request.GET.get('codeAfm', None)
            codeGrad = request.GET.get('codeGrad', None)
            codeSpec = request.GET.get('codeSpec', None)
            name = request.GET.get('name', None)
            surname = request.GET.get('surname', None)
            """
            try:
            except IntegrityError:
                transaction.rollback()
            """
            Teacher(name=name , surname = surname, codeAfm = codeAfm, codeGrad = codeGrad , codeSpec = codeSpec).save()
            #t0.save() # Succeeds, but may be undone by transaction rollback
            #c.save() # Succeeds, but a.save() may have been undone
	        #print ("New Record has id %d.\n", $mysqli->insert_id)
            dictData = "Success"
            #print dictData
            jsonData = json.dumps(dictData)
            #print jsonData
            return HttpResponse(jsonData, content_type='application/json')

        #UPDATE COMMAND
        if (action=="update"):
            id = request.GET.get('id', None)
            codeAfm = request.GET.get('codeAfm', None)
            codeGrad = request.GET.get('codeGrad', None)
            codeSpec = request.GET.get('codeSpec', None)
            name = request.GET.get('name', None)
            surname = request.GET.get('surname', None)
            Teacher.objects.filter(id=id).update(name=name , surname = surname, codeAfm = codeAfm, codeGrad = codeGrad , codeSpec = codeSpec ,)

        #DELETE COMMAND
        if (action=="delete"):
            id = request.GET.get('id', None)
            try:
                Teacher.objects.filter(id=id).delete()
            except IntegrityError:
                transaction.rollback()   
	            #result = "error"
	        #printf ("Deleted Record has id %d.\n", $_GET['EmployeeID']);
	        result = "success"
            #return HttpResponse(result, content_type='application/json')

        #SELECT is default
        else:
            dictData = Teacher.objects.all().values()
            #print dictData
            jsonData = json.dumps(list(dictData))
            return HttpResponse(jsonData, content_type='application/json')
    # all others error
    else: 
        raise Http404    
 
