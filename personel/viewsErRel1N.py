#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import os, time
from django.contrib import messages
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
from django.db import transaction
from django.db import DatabaseError, IntegrityError

from models import Folder, Grader, Lesson, School, SchoolToGrade, Specialty, Teacher
from helpScripts import helperMessageLog


""" 
M:N Relation > QuerySet Values to JSON 

"""
def jsonFolderCrud(request):
    
    dictData = []
    # GET * SELECT 
    if request.is_ajax() and request.method == 'GET':
        action = request.GET.get('action', None)

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

        #INSERT COMMAND (need related LessonID ) | only add C type folders
        if (action=="add"):        # on LessonID
            LessonID = request.POST.get('LessonID', None)
            no = request.POST.get('no', None)
            books = request.POST.get('books', None)#.title()
            codeType = request.POST.get('codeType', None)
            #status = request.POST.get('status', None)
            print 'Data:',  no, books, codeType
            # Apaitoume oi fakeloi na exoun synexomeh arithmisi
            # akoma kai gia diafortikous typous
            # px fA/fANA. Ayto to allazoume efkola an theloume 
            # TO kanoume giati volevei sta reports
            # alliws tha kanoume aali coding ...
            #no = Lesson.objects.get(id=LessonID).getNextFolderNo(codeType)

            try:    #with transaction.atomic():
                lesson = Lesson.objects.get(id=LessonID)
                no = lesson.getNextFolderNo(-1)   # count F(AB) / even for F(ANA)
                print 'Data(new):',  no, books, codeType
                record = Folder(LessonID_id = LessonID, no = no, books = books, codeType = codeType)
                record.save()
                record.codeBarcode ='%04d-%010d' %(int(LessonID), int(record.id))
                record.save()
                # Need to Update Lesson Data HERE aka mum Books, Folders etc.
                if codeType=='0':    # F(A)
                    print "F(A)"
                    #lesson.update(booksAB=booksAB+books,  booksABFolders=booksABFolders+1)
                    lesson.booksAB = lesson.booksAB + int(books)
                    lesson.booksABFolders = lesson.booksABFolders + 1
                    lesson.save()
                elif codeType=='1':    # F(B)
                    #lesson.booksAB += books 
                    #lesson.booksABFolders += 1
                    pass
                elif codeType=='2':    # F(ANA)
                    lesson.booksC = lesson.booksC + int(books)
                    lesson.booksCFolders = lesson.booksCFolders + 1
                    lesson.save()

                msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
                #messages.info(request, msg, fail_silently=True)                
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία εισαγωγής εγγραφής!"
                helperMessageLog(request, msg, tag='error')
                #messages.error(request, msg, fail_silently=True)                

            #dictData = Lesson.objects.filter(id=record.id).values()             
            #print dictData
            #jsonData = json.dumps(list(dictData))
            jsonData = json.dumps({'msg': msg})
            return HttpResponse(jsonData, content_type='application/json')
        
        # UPDATE
        if (action=="update"):
            id = request.POST.get('id', None)
            no = request.POST.get('no', None)
            books = request.POST.get('books', None)
            codeType = request.POST.get('codeType', None)
            #lexType = request.POST.get('lexType', None)
            #CodeStatus = request.POST.get('CodeStatus ', None)
            #CodeLocation = request.POST.get('CodeLocation', None)
            #print "FOLDER-UPDATE %s - %s - codeType:%s lexType:%s" %(no, books, codeType, lexType)
            
            try:    #with transaction.atomic():
                record = Folder.objects.filter(id=id)
                record.update( no = no, books = books, codeType = codeType,)
                msg = "Επιτυχής τροποποίηση εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
                #messages.info(request, msg, fail_silently=True)                
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία τροποποίησης εγγραφής!"
                helperMessageLog(request, msg, tag='error')
                #messages.error(request, msg, fail_silently=True)                

            #Folder.objects.filter(id=id).update(isCoordinator = helperStr2Bool(isCoordinator), isgraderC = helperStr2Bool(isgraderC), status = status, )                       
            # return Lesson record
            #dictData = record.values()
            #jsonData = json.dumps(list(dictData))
            jsonData = json.dumps({'msg': msg})
            #print jsonData
            return HttpResponse(jsonData, content_type='application/json')

        #DELETE COMMAND
        if (action=="delete"):
            id = request.POST.get('id', None)
            try:
                record = Folder.objects.get(id=id)
                # update related lesson
                lesson = Lesson.objects.get(id=record.LessonID.id)
                print "codeType:%s" %(record.codeType)
                print "lesson:%d" %(lesson.id)
                if record.codeType==0:    # F(A)
                    print "delete codeType:%s" %(record.codeType)
                    #lesson.update(booksAB=booksAB+books,  booksABFolders=booksABFolders+1)
                    lesson.booksAB = lesson.booksAB - int(record.books)
                    lesson.booksABFolders = lesson.booksABFolders - 1
                    lesson.save()
                elif record.codeType==1:    # F(B)
                    pass
                elif record.codeType==2:    # F(ANA)
                    print "delete codeType:%s" %(record.codeType)
                    lesson.booksC = lesson.booksC - int(record.books)
                    lesson.booksCFolders = lesson.booksCFolders - 1
                    lesson.save()
                
                record.delete()
                msg = "Επιτυχής διαγραφής Φακέλου (%s) !" %(record)             
                helperMessageLog(request, msg, tag='info')

                #messages.info(request, msg, fail_silently=True)                
            except IntegrityError:
                transaction.rollback()   
                msg = "Αδυναμία διαγραφής Φακέλου (%s) !" %(record)
                helperMessageLog(request, msg, tag='error')
                #messages.error(request, msg, fail_silently=True)                
            jsonData = json.dumps({'msg': msg})
            return HttpResponse(jsonData, content_type='application/json')


    #"Default SELECT(*) "
    dictData = Folder.objects.all().values()
    #print dictData
    jsonData = json.dumps(list(dictData))
    return HttpResponse(jsonData, content_type='application/json')


""" QuerySet Values to JSON """
def jsonLessonCrud(request):

    #Handle Mesages
    #messages.success(request, 'All items on this page have free shipping.',fail_silently=False)
    #messages.warning(request, 'All items on this page have free shipping.',fail_silently=True) #OK

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

            try:
                record = Folder(category = category, name = name, type = type)
                record.save()
                msg = "Επιτυχής εισαγωγή Φακέλου (%s) !" %(record)             
                helperMessageLog(request, msg, tag='info')
            except IntegrityError:
                transaction.rollback()   
                msg = "Αδυναμία εισαγωγής Φακέλου (%s) !" %(record)
                helperMessageLog(request, msg, tag='error')
            #jsonData = json.dumps({'msg': msg})
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
            
            try:
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                record = Lesson.objects.filter(id=id)
                record.update( booksC = booksC, booksCFolders = booksCFolders, category = category, name=name , type = type, )
                msg = "Επιτυχής τροποποίηση Φακέλου (%s) !" %(record)             
                helperMessageLog(request, msg, tag='info')
            except IntegrityError:
                transaction.rollback()   
                msg = "Αδυναμία τροποποίησης Φακέλου (%s) !" %(record)
                helperMessageLog(request, msg, tag='error')
            
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
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                record.delete()
                msg = "Επιτυχής διαγραφή Φακέλου (%s) !" %(record)             
                helperMessageLog(request, msg, tag='info')
            except IntegrityError:
                transaction.rollback()   
                msg = "Αδυναμία διαγραφής Φακέλου (%s) !" %(record)
                helperMessageLog(request, msg, tag='error')
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

            try:
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                record = SchoolToGrade(code = code , name = name, ddeCode = ddeCode, ddeName= ddeName, type = type).save()
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία εισαγωγής εγγραφής!"
                helperMessageLog(request, msg, tag='error')

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
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής διαγραφή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία διαγραφής εγγραφής!"
                helperMessageLog(request, msg, tag='error')            
            return HttpResponse(result, content_type='application/json')

        #UPDATE
        elif (action=="update"):
            id = request.POST.get('id', None)
            code = request.POST.get('code', None)
            name = request.POST.get('name', None)
            ddeCode = request.POST.get('ddeCode', None)
            ddeName = request.POST.get('ddeName', None)
            type = request.POST.get('type', None)

            try:
                record = SchoolToGrade.objects.filter(id=id)
                record.update( code = code , name = name, ddeCode = ddeCode, ddeName = ddeName, type = type )
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής τροποποίηση εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία τροποποίησης εγγραφής!"
                helperMessageLog(request, msg, tag='error')            
            
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
            try:   
                record = Specialty(code = code , name = name, ).save()
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία εισαγωγής εγγραφής!"
                helperMessageLog(request, msg, tag='error')

            dictData = Specialty.objects.filter(id=record.id).values()                         
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')

        #DELETE 
        if (action=="delete"):
            id = request.POST.get('id', None)
            record = Specialty.objects.filter(id=id)
            try:
                record.delete()
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής διαγραφή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία διαγραφής εγγραφής!"
                helperMessageLog(request, msg, tag='error')
            return HttpResponse(result, content_type='application/json')

        #UPDATE
        elif (action=="update"):
            id = request.POST.get('id', None)
            code = request.POST.get('code', None)
            name = request.POST.get('name', None)

            try:
                record = Specialty.objects.filter(id=id)
                record.update( code = code , name = name, )
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής τροποποίηση εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία τροποποίησης εγγραφής!"
                helperMessageLog(request, msg, tag='error')
            
            dictData = record.values()
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
                    
            try:    
                record = Specialty(code = code , name = name )
                record.save()
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία εισαγωγής εγγραφής!"
                helperMessageLog(request, msg, tag='error')

            dictData = Specialty.objects.filter(id=record.id).values()             
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')

        #DELETE 
        if (action=="delete"):
            id = request.POST.get('id', None)
            
            try:
                record = Specialty.objects.filter(id=id)
                record.delete()
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής διαγραφή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία διαγραφής εγγραφής!"
                helperMessageLog(request, msg, tag='error')
            return HttpResponse(result, content_type='application/json')

        #UPDATE
        elif (action=="update"):
            id = request.POST.get('id', None)
            code = request.POST.get('code', None)
            name = request.POST.get('name', None)

            try:
                record = Specialty.objects.filter(id=id)
                record.update( code = code , name = name, )
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής τροποποίηση εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία τροποποίησης εγγραφής!"
                helperMessageLog(request, msg, tag='error')

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
                    
            try:    
                record = Teacher( codeAfm = codeAfm, codeGrad = codeGrad , codeSpec = codeSpec, surname = surname, name=name, ).save()
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία εισαγωγής εγγραφής!"
                helperMessageLog(request, msg, tag='error')
                        
            dictData = Teacher.objects.filter(id=record.id).values()
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')

        #DELETE 
        if (action=="delete"):
            id = request.POST.get('id', None)
            
            try:
                record = Teacher.objects.filter(id=id)
                record.delete()
                msg = "Επιτυχής διαγραφή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία διαγραφής εγγραφής!"
                helperMessageLog(request, msg, tag='error')
            return HttpResponse(msg, content_type='application/json')

        #UPDATE
        elif (action=="update"):
            id = request.POST.get('id', None)
            codeAfm = request.POST.get('codeAfm', None)
            codeGrad = request.POST.get('codeGrad', None)
            codeSpec = request.POST.get('codeSpec', None)
            surname = request.POST.get('surname', None)
            name = request.POST.get('name', None)

            try:
                record = Teacher.objects.filter(id=id)            
                record.update( codeAfm = codeAfm, codeGrad = codeGrad , codeSpec = codeSpec,surname = surname, name=name , )
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής τροποποίηση εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία τροποποίησης εγγραφής!"
                helperMessageLog(request, msg, tag='error')

            dictData = record.values()
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
 
