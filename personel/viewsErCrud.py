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
from django.db import transaction
from django.db import DatabaseError, IntegrityError

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from models import Grader, Lesson, Teacher, School, SchoolToGrade, Specialty

from helpScripts import *


###################################
# FOLDER
###################################
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
        if (action=="add"):
            LessonID = request.POST.get('LessonID', None)        
            no = request.POST.get('no', None)
            books = request.POST.get('books', None)#.title()
            type = request.POST.get('type', None)#.title()
            #status = request.POST.get('status', None)
            print 'Data:',  no, books, type
            no = Lesson.objects.get(id=LessonID).getNextFolderNo(type = type)
            print 'Data(new):',  no, books, type

            try:    #with transaction.atomic():
                Folder(LessonID_id = LessonID, no = no, books = books, type = type).save()
                msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                msg = "Αδυναμία εισαγωγής εγγραφής!"
                helperMessageLog(request, msg, tag='error')

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
            try:    #with transaction.atomic():
                record = FolderLesson.objects.filter(id=id)
                record.update( no = no, books = books, type = type,)
                msg = "Επιτυχής ενημέρωση εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                msg = "Αδυναμία ενημέρωσης εγγραφής!"
                helperMessageLog(request, msg, tag='error')

            #Folder.objects.filter(id=id).update(isCoordinator = helperStr2Bool(isCoordinator), 
            #isgraderC = helperStr2Bool(isgraderC), status = status, )                       
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
                msg = "Επιτυχής διαγραφή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία διαγραφής εγγραφής!"
                helperMessageLog(request, msg, tag='error')
            
            return HttpResponse(result, content_type='application/json')


    #"Default SELECT(*) "
    dictData = Folder.objects.all().values()
    #print dictData
    jsonData = json.dumps(list(dictData))
    return HttpResponse(jsonData, content_type='application/json')



###################################
# LESSON
###################################
""" 
CRUD on Lesson
fields: 
"""
def jsonLessonCrud(request):
    
    # Display on GET 
    if request.is_ajax() and request.method == 'GET':
        id  = request.GET.get('id', None)
        action = request.GET.get('action', None)
        
        if (action=="filter"):
            dictData = Lesson.objects.filter(id=id).values()
        else: 
            dictData = Lesson.objects.all().order_by('type', 'name', 'category').values()

        
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
            #category = request.POST.get('category', None)
            name = request.POST.get('name', None)
            type = request.POST.get('type', None)     
            
            try:    #with transaction.atomic():
                record = Lesson(name = name, type = type)
                record.save()            
                msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                msg = "Αδυναμία εισαγωγής εγγραφής!"
                helperMessageLog(request, msg, tag='error')
            
            return HttpResponse(json.dumps({'msg':msg}), content_type='application/json')
        
        # UPDATE 
        elif (action=="update"):
            id = request.POST.get('id', None)
            #Fakeloi 1o 2o xeri (AB)
            #booksAB booksABFolders 
            booksC = request.POST.get('booksC', None)
            booksCFolders = request.POST.get('booksCFolders', None)
            name = request.POST.get('name', None)
            type = request.POST.get('type', None)         

            try:    #with transaction.atomic():
                record = Lesson.objects.filter(id=id)
                #record.update( booksC = booksC, booksCFolders = booksCFolders, name=name , type = type, )
                record.update( name=name , type = type, )
                msg = "Επιτυχής τροποποίηση εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                msg = "Αδυναμία τροποποίησης εγγραφής!"
                helperMessageLog(request, msg, tag='error')
            
            return HttpResponse(json.dumps({'msg':msg}), content_type='application/json')

        # UPDATE 
        elif (action=="updatefolderc"):
            id = request.POST.get('id', None)
            #Fakeloi 1o 2o xeri (AB)
            #booksAB booksABFolders 
            booksC = request.POST.get('booksC', None)
            booksCFolders = request.POST.get('booksCFolders', None)
            category = request.POST.get('category', None)
            name = request.POST.get('name', None)
            type = request.POST.get('type', None)            

            try:    #with transaction.atomic():
                record = Lesson.objects.filter(id=id)
                record.update( booksC = booksC, booksCFolders = booksCFolders, category = category, name=name , type = type, )
                msg = "Επιτυχής τροποποίηση εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                msg = "Αδυναμία τροποποίησης εγγραφής!"
                helperMessageLog(request, msg, tag='error')
            
            return HttpResponse(json.dumps({'msg':msg}), content_type='application/json')

        #DELETE
        if (action=="delete"):
            id = request.POST.get('id', None)
            record = Lesson.objects.filter(id=id)
            try:
                record.delete()
                msg = 'Επιτυχής διαγραφή εγγραφής!'
                helperMessageLog(request, msg, tag='info')
            except IntegrityError:
                transaction.rollback()   
                msg = 'Αδυναμία διαγραφής εγγραφής!'
                helperMessageLog(request, msg, tag='error')
                
            return HttpResponse(json.dumps({'msg':msg}), content_type='application/json')
        # else: No POST Default 
    # DEFAULT 
    else: 
        dictData = Lesson.objects.all().values()
        jsonData = json.dumps(list(dictData))
        return HttpResponse(jsonData, content_type='application/json')
 

""" 
QuerySet Values to JSON 
"""
def jsonLessonStatus(request):
       
    if request.is_ajax() and request.method == 'POST':
        id = request.POST.get('id', None)
        status = request.POST.get('status', None)
        #print id, status 
        
        if (id is None) or (status is None): 
            msg = 'Σφάλμα τιμών για το Μάθημα!'
            helperMessageLog(request, msg, tag='info')
            raise Http404
        
        l = Lesson.objects.get(id=id)
        """
        if lesson.status != status - 1:
            print 'Improper Action (To see staus 6-7)'
            raise Http404    
        """        
        (success, msg, tag) = l.changeStatus(int(status))
        helperMessageLog(request, msg, tag)
        #print "success:(%0), msg:%1, tag:%2" %(success, msg, tag)
        print success, msg, tag
        #print "ERROR: lesson.changeStatus(status):"
        #raise Http404    
                    
        #dictData = {'msg':'Status Changed'}        
        dictData = {'msg': msg}        
        jsonData = json.dumps(dictData)
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')
    else: 
        #dictData = {'msg':'Request Error'}
        msg = "Request Error!"     # Mallon xazo 
        jsonData = json.dumps(msg)
        return HttpResponse(jsonData, content_type='application/json')
        #raise Http404    


###################################
# SchoolToGrade 
###################################
""" 
CRUD for SchoolToGrade 
fields: code name  ddeCode ddeName type = IntegerField(choices=SCHOOL_TYPE, default=1)   

Added: support for native django messages even in JSON
MESSAGE CODES
-------------
debug	10  Development-related messages that will be ignored (or removed) in a production deployment
info	20	Informational messages for the user
success	25	An action was successful, e.g. "Contact info was sent successfully"
warning	30	A failure did not occur but may be imminent
error

"""
#@login_required
#@json_response(ajax_required=True, login_required=True) 
#@ajax_login_required
#@group_required('admins','editors')
#@group_required('Grammateia')
def jsonSchoolToGradeCrud(request):
        
    #OK Handle Mesages
    #messages.add_message(request, messages.INFO, 'All items on this page have free shipping.',fail_silently=True)
    #messages.info(request, 'jsonSchoolToGradeCrud.',fail_silently=True)
    #messages.info(request, 'All items on this page have free shipping.',fail_silently=False)
    
    if request.is_ajax() and request.method == 'GET':

        id = request.GET.get('id', None)
        action = request.GET.get('action', None)
        
        if (action=="filter"):
            dictData = SchoolToGrade.objects.filter(id=id).values()
        else: 
            dictData = SchoolToGrade.objects.all().values()
                
        #Handle Mesages
        #messages.warning(request, 'All items on this page have free shipping.',fail_silently=True) #OK

        #print dictData
        jsonData = json.dumps(list(dictData))
        return HttpResponse(jsonData, content_type='application/json')

    if request.is_ajax() and request.method == 'POST':
        action = request.POST.get('action', None)
        print "POST" , action

        #Handle Mesages
        #messages.add_message(request, messages.ERROR, 'POST.',fail_silently=True)
        #messages.success(request, 'All items on this page have free shipping.',fail_silently=True)
        #messages.warning(request, 'All items on this page have free shipping.',fail_silently=True) #OK

        #ADD
        if (action=="add"):
            code = request.POST.get('code', None)
            name = request.POST.get('name', None)
            ddeCode = request.POST.get('ddeCode', None)
            ddeName = request.POST.get('ddeName', None)
            type = request.POST.get('type', None)
            #2018
            address = request.POST.get('address', None)
            city = request.POST.get('city', None)
            tk = request.POST.get('tk', None)

            #print code , name,  ddeCode, ddeName, type 
                    
            try:    #with transaction.atomic():
                #record = SchoolToGrade(code = code , name = name, ddeCode = ddeCode, ddeName= ddeName, type = type)
                record = SchoolToGrade(code = code , name = name, ddeCode = ddeCode, type = type, address=address, city=city, tk=tk, )
                record.save()
                msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                msg = "Αδυναμία εισαγωγής εγγραφής!"
                helperMessageLog(request, msg, tag='error')

            # return Lesson record            
            return HttpResponse(json.dumps({'msg':msg}), content_type='application/json')

        #DELETE 
        if (action=="delete"):
            id = request.POST.get('id', None)
            record = SchoolToGrade.objects.filter(id=id)
            try:
                record.delete()
                msg = "Επιτυχής διαγραφή εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία διαγραφής εγγραφής!"
                helperMessageLog(request, msg, tag='error')
            
            return HttpResponse(json.dumps({'msg':msg}), content_type='application/json')

        #UPDATE
        elif (action=="update"):
            id = request.POST.get('id', None)
            code = request.POST.get('code', None)
            name = request.POST.get('name', None)
            ddeCode = request.POST.get('ddeCode', None)
            ddeName = request.POST.get('ddeName', None)
            type = request.POST.get('type', None)
            address = request.POST.get('address', None)
            city = request.POST.get('city', None)
            tk = request.POST.get('tk', None)

            try:
                record = SchoolToGrade.objects.filter(id=id)
                record.update( code = code , name = name, ddeCode = ddeCode, ddeName = ddeName, type = type,\
                        address=address, city=city, tk=tk, )
                msg = "Επιτυχής τροποποίηση εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία τροποποίησης εγγραφής!"
                helperMessageLog(request, msg, tag='error')
            
            return HttpResponse(json.dumps({'msg':msg}), content_type='application/json')

    # DEFAULT 
    else: 
        #Handle Mesages
        messages.alert(request, 'DEFAULT.',fail_silently=True)
        dictData = SchoolToGrade.objects.all().values()
        jsonData = json.dumps(list(dictData))
        #print jsonData        
        return HttpResponse(jsonData, content_type='application/json')



###################################
# Specialty 
###################################
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
                msg = 'Επιτυχής εισαγωγή εγγραφής!' 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = 'Αδυναμία εισαγωγής εγγραφής.'
                helperMessageLog(request, msg, tag='error')
            
            #dictData = Specialty.objects.filter(id=record.id).values()             
            #jsonData = json.dumps(dictData)
            #return HttpResponse(jsonData, content_type='application/json')
            return HttpResponse(json.dumps({'msg':msg}), content_type='application/json')

        #DELETE 
        if (action=="delete"):
            id = request.POST.get('id', None)
            record = Specialty.objects.filter(id=id)
            try:
                record.delete()
                msg = 'Επιτυχής διαγραφή εγγραφής!' 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = 'Αδυναμία διαγραφής εγγραφής.'
                helperMessageLog(request, msg, tag='error')
            
            return HttpResponse(json.dumps({'msg':msg}), content_type='application/json')
            #return HttpResponse(result, content_type='application/json')


        #UPDATE
        elif (action=="update"):
            id = request.POST.get('id', None)
            code = request.POST.get('code', None)
            name = request.POST.get('name', None)
            
            try:
                record = Specialty.objects.filter(id=id)
                record.update( code = code , name = name, )            
                msg = 'Επιτυχής ενημέρωση εγγραφής!' 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = 'Αδυναμία ενημέρωσης εγγραφής.'
                helperMessageLog(request, msg, tag='error')
            
            return HttpResponse(json.dumps({'msg':msg}), content_type='application/json')




    # DEFAULT 
    else: 
        dictData = Specialty.objects.all().values()
        jsonData = json.dumps(list(dictData))
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')



#CRUD for Specialty 
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

###################################
# Teacher
###################################
""" 
CRUD for Teacher
fields: codeAfm codeGrad codeSpec name surname 
2018 phoneMob
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
            phoneMob = request.POST.get('phoneMob', None)
            phoneHom = request.POST.get('phoneHom', None)

            try:
                record = Teacher( codeAfm = codeAfm, codeGrad = codeGrad , codeSpec = codeSpec,\
                        surname = surname, name=name,\
                        phoneMob=phoneMob, phoneHom=phoneHom, )
                record.save()
                msg = 'Επιτυχής εισαγωγή εγγραφής!' 
                helperMessageLog(request, msg, tag='info')
                #messages.success(request, msg, fail_silently=True)
            except DatabaseError:
                transaction.rollback()   
                msg = 'Αδυναμία εισαγωγής εγγραφής.'
                helperMessageLog(request, msg, tag='error')

            return HttpResponse(json.dumps({'msg':msg}), content_type='application/json')

        #DELETE 
        if (action=="delete"):
            id = request.POST.get('id', None)
            record = Teacher.objects.filter(id=id)
            try:
                record.delete()
                msg = 'Επιτυχής διαγραφή εγγραφής!' 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = 'Αδυναμία διαγραφής εγγραφής.'
                helperMessageLog(request, msg, tag='error')
            
            return HttpResponse(json.dumps({'msg':msg}), content_type='application/json')
            #return HttpResponse(result, content_type='application/json')

        #UPDATE
        elif (action=="update"):
            id = request.POST.get('id', None)
            codeAfm = request.POST.get('codeAfm', None)
            codeGrad = request.POST.get('codeGrad', None)
            codeSpec = request.POST.get('codeSpec', None)
            surname = request.POST.get('surname', None)
            name = request.POST.get('name', None)
            phoneMob = request.POST.get('phoneMob', None)
            phoneHom = request.POST.get('phoneHom', None)

            try:
                record = Teacher.objects.filter(id=id)            
                record.update( codeAfm = codeAfm, codeGrad = codeGrad , codeSpec = codeSpec,surname = surname, name=name,\
                        phoneMob=phoneMob, phoneHom=phoneHom)
                msg = 'Επιτυχής τροποποίηση εγγραφής!' 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = 'Αδυναμία τροποποίησης εγγραφής.'
                helperMessageLog(request, msg, tag='error')

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
View to return Teacher instances that are not currently assigned
as Graders for a Lesson 
| gets list of ids
| Uses fk_fields = json.loads(request.POST['jqxinputGraderNewTeacherArray'])
to get array fdata from ajax POst request via .stringify
| returns JSON response 
"""
def jsonTeacherCrudExclude(request):

    status = 'Success'
    if request.is_ajax() and request.method == 'POST':

        #jqxinputLesson = request.POST.get('jqxinputGraderNewLesson', None)
        #jqxinputTeacherArray = request.POST.getlist('jqxinputGraderNewTeacherArray[]', '')       # Received: [u'[7,6,1]'] AS STRING
        
        jqxinputTeacherArray = json.loads(request.POST['jqxinputGraderNewTeacherArray'])
        #print 'POST Received:', jqxinputLesson, jqxinputTeacherArray
        
        # CHECK Fail Conditions  | Pass to DB |  MUST CHECK FOR FAIL CONDITIONS
        #lessonIsNull = True  if jqxinputLesson == ''  else False 
        #teacherArrayIsNull = True  if jqxinputTeacherArray == ''  else False 
        
        """            
        if lessonIsNull or teacherArrayIsNull:
            status = 'Error'
            #responseData.append ( {'status': 'error', } )
        else:
            lesson = Lesson.objects.get( id = jqxinputLesson )        # pk = # get Lesson Data 
            print "Found in DB (LESSON):", lesson.name
            for jqxinputTeacher in jqxinputTeacherArray:
                teacher = Teacher.objects.get(id = jqxinputTeacher )  # get Teacher Data 
                #teacher = Teacher.objects.filter( id = jqxinputTeacher )
                print "Found in DB (TEACHER):", teacher.surname
                graderExists = False  if Grader.objects.filter(TeacherID = teacher, LessonID = lesson).count() == 0  else True 
                if not (graderExists):
                    print 'No GraderExists:', teacher,  lesson
                    # INSERT to DB > MUST CHECK FOR FAIL CONDITIONS
                    Grader(LessonID = lesson, TeacherID = teacher, ).save()
                    print 'INSERT Grader:', teacher,  lesson
                else: 
                    status = 'Errors'
        """                                
        # get unAssigned Teachers for Lesson
        dictData = Teacher.objects.exclude(id__in=jqxinputTeacherArray)
        #dictData = {'status': status, }
        jsonData = json.dumps(dictData)
        return HttpResponse(jsonData, content_type='application/json')
    else:
        raise Http404    
        #return HttpResponse(html)

""" 
CRUD for Teacher 
"""

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
            try:
            except IntegrityError:
                transaction.rollback()
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
 """

