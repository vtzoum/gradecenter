#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import os, time

from django.conf import settings 
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse

from django.db import DatabaseError, IntegrityError, transaction
from django.db.models import QuerySet

from django.forms import *
from django.forms.models import model_to_dict

from django.http import Http404, HttpResponse,HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import CreateView, DeleteView, UpdateView, View

from models import Grader, Lesson, Teacher, School, SchoolToGrade, Specialty

from helpScripts import helperMessageLog 

"""
@csrf_exempt
def jsonFileUploadCSVImport(request):
    
    errorData = []
    successData = []
    responseData = []
    if request.is_ajax():
        actionP = request.POST.get('action', 'error')
        filename = request.POST.get('jqxinputFileName', '')
        idxName = request.POST.get('jqxinputIdxName', '')
        idxFirstRow = request.POST.get('jqxinputFirstRow', '')
        print actionP, filename, idxName, idxFirstRow
        
        #2.CHECK-IMPORT
        #3.DO-IMPORT
        #filename = 'uploads/LessonsCSV.csv'
        if (actionP =='checkimport') or  (actionP =='doimport'):       
            ext = filename.split('.')[-1]
            if ext not in ['xls', 'xlsx', 'csv']:
                #return "File %s is not CSV, XLS, XLSX" % ( filename)
                errorData.append("File %s is not CSV, XLS, XLSX" % (filename) )
                #raise Http404    
                       
            dataReader = csv.reader(open(filename), delimiter=',', quotechar='"')
            #dataReader = csv.reader(codecs.open(csv_filepathname, ‘rU’, ‘utf-16’))

            for row in dataReader:
                if row[0] != 'ΜΑΘΗΜΑ': # Ignore header
                    #Lesson(name = lessonName).save()
                    lessonExists = False  if Lesson.objects.filter(name = row[0]).count() == 0  else True 
                    if lessonExists:
                        errorData.append ( "Lesson %s exist." % (row[0]))
                    else:
                        #success.append ( "Lesson %s will be inserted." % (row[0]))
                        successData.append ({'name': row[0]})
                        #newLesson = Lesson()
                        #newLesson.name =  row[0]
                        #newLesson.save()
            
            dictData = {'status': 'OK', 'errorData': errorData, 'data': successData}
            #print dictData 
            jsonData = json.dumps(dictData)
            print jsonData
            return HttpResponse(jsonData, content_type='application/json')

        # 1.UPLOAD-CSV  default TO CHANGE 
        else:  
            if 'fileToUpload'not in request.FILES:
                return HttpResponse("Error", content_type='application/json')
            
            if request.FILES['fileToUpload'].size > 200000:
                return HttpResponse("File too Large", content_type='application/json')

            if not handle_uploaded_file(request.FILES['fileToUpload']):
                return HttpResponse("File Write", content_type='application/json')
                                
            #Respond
            msg = "success: File Write OK"
            toFilename = getUploadedFileName((request.FILES['fileToUpload'].name))
            #'data': {'name':"ΝΕΟΕΛΛΗΝΙΚΗ ΓΛΩΣΣΑ"}, {'name':"ΑΡΧΑΙΑ ΕΛΛΗΝΙΚΑ",}]}
            jsonResponse = json.dumps( {'msg':msg, 'filename': toFilename, 
                'data': [{'name':"ΝΕΟΕΛΛΗΝΙΚΗ ΓΛΩΣΣΑ"}, {'name':"ΑΡΧΑΙΑ ΕΛΛΗΝΙΚΑ",}] } )
            #jsonData = json.dumps(list(dictData))
            print jsonResponse
            return HttpResponse(jsonResponse, content_type='application/json')
    
    else: 
        dictData = {'success': 'ERROR', 'error': 'ERROR'}
        jsonData = json.dumps(dictData)
        return HttpResponse(jsonData, content_type='application/json')
    #raise Http404    
    #return render(request, 'upload.html', {'form': form})
"""

""" Import Lessons to DB using an uploaded CSV file """
@csrf_exempt
def jsonFileCSVImportLesson(request):
    
    responseData = []
    status = 'Success'
    #errorsFound = True
    if request.is_ajax():
        actionP = request.POST.get('action', 'error')
        filename = request.POST.get('jqxinputFileName', '')
        #idxName = request.POST.get('jqxinputIdxName', '')
        #idxFirstRow = request.POST.get('jqxinputFirstRow', '')
        print actionP, filename #, idxName, idxFirstRow
        
        #2.CHECK-IMPORT
        #3.DO-IMPORT
        #filename = 'uploads/LessonsCSV.csv'
        if (actionP =='checkimport') or  (actionP =='doimport'):       
            ext = filename.split('.')[-1]
            if ext not in ['xls', 'xlsx', 'csv']:
                #return "File %s is not CSV, XLS, XLSX" % ( filename)
                #errorData.append("File %s is not CSV, XLS, XLSX" % (filename) )
                raise Http404    
                       
            dataReader = csv.reader(open(filename, mode='r'), delimiter=',', quotechar='"')
            #dataReader = csv.reader(codecs.open(csv_filepathname, ‘rU’, ‘utf-16’))
            next(dataReader, None)  # skip the headers
            (msg, tag) = ('', 'info')
            for row in dataReader:  #exclude 1st row
            #for row in dataReader:
                #if row[0] != 'ΜΑΘΗΜΑ': # Ignore header
                #Lesson(name = lessonName).save()
                lessonName, lessonCategory, lessonType = row[0], row[1], row[2]
                nameIsNull = True  if lessonName == ''  else False 
                categoryIsNull = True  if lessonCategory == ''  else False 
                typeIsNull = True  if lessonType == ''  else False 
                
                # check on Table constraint
                lessonExists = False  if Lesson.objects.filter(name = lessonName, category=lessonCategory, type=lessonType).count() == 0  else True 
                
                # Dry run
                if nameIsNull or categoryIsNull or typeIsNull or lessonExists:
                    (status, tag) = ('error', 'error')
                    #responseData.append ( {'name': lessonName, 'type': lessonType , 'status': 'error' })
                else:
                    (status, tag) = ('OK', 'info')
                    #responseData.append ( {'name': lessonName, 'type': lessonType , 'status': 'success' })
                    #msg = msg + ('Lesson (%s) with type (%s) has errors!' %(lessonName, lessonType))

                    # Import in DB 
                    if (actionP =='doimport'):         
                        try:
                            Lesson(name = lessonName, category = lessonCategory, type = lessonType).save()
                            status = 'OK'
                            msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                        except DatabaseError:
                            (status, tag) = ('error', 'error')

                responseData.append ( {'name': lessonName, 'category': lessonCategory , 'type': lessonType , 'status': status })

                """
                if nameIsNull or categoryIsNull or lessonExists:
                    status = 'error'
                    tag = 'error'
                    #msg = msg + ('Lesson (%s) with type (%s) has errors!' %(lessonName, lessonType))
                    responseData.append ( {'name': lessonName, 'type': lessonType , 'status': 'error' })
                else:
                    responseData.append ( {'name': lessonName, 'type': lessonType , 'status': 'success' })
                    #msg = msg + ('Lesson (%s) with type (%s) has errors!' %(lessonName, lessonType))

                    if (actionP =='doimport'):         # Now, do Import in DB 
                        try: 
                            Lesson(name = lessonName, category = lessonCategory, type = lessonType).save()
                            msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                            #helperMessageLog(request, msg, tag='info')
                        except DatabaseError:
                            #msg = "Αδυναμία εισαγωγής εγγραφής!"
                            tag = 'error'
                            msg = msg + ('Αδυναμία εισαγωγής εγγραφής (%s)!' %(lessonName))
                            #helperMessageLog(request, msg, tag='error')
                """
        
            helperMessageLog(request, msg, tag)
            dictData = {'status': status, 'data': responseData}
            #print dictData
            jsonData = json.dumps(dictData)
            #print jsonData
            return HttpResponse(jsonData, content_type='application/json')
    else: 
        raise Http404    

""" 
Import Lessons to DB using an uploaded CSV file 
"""
@csrf_exempt
def jsonFileCSVImportSchoolToGrade(request):

    responseData = []
    status = 'ΟΚ! ΔΕΝ παρουσιάστηκαν Σφάλματα!'
    #errorsFound = True
    if request.is_ajax():
        actionP = request.POST.get('action', 'error')
        filename = request.POST.get('jqxinputFileName', '')
        print actionP, filename #, idxName, idxFirstRow
        
        #2.CHECK-IMPORT #3.DO-IMPORT
        #filename = 'uploads/LessonsCSV.csv'
        if (actionP =='checkimport') or (actionP =='doimport'):       
            ext = filename.split('.')[-1]
            if ext not in ['xls', 'xlsx', 'csv']:
                #return "File %s is not CSV, XLS, XLSX" % ( filename)
                #errorData.append("File %s is not CSV, XLS, XLSX" % (filename) )
                raise Http404    
                       
            dataReader = csv.reader(open(filename, mode='r'), delimiter=',', quotechar='"')
            next(dataReader, None)  # skip the headers
            (msg, tag) = ('', 'info')
            for row in dataReader:  #exclude 1st row
                schoolCode, schoolName, schoolType, schoolTypeLex, schoolDdeCode, schoolDdeName, = row[0], row[1], row[2], row[3],row[4], row[5], 
                #print schoolCode, schoolName, schoolDdeCode, schoolDdeName, 
                codeIsNull = True  if schoolCode == ''  else False 
                nameIsNull = True  if schoolName == ''  else False 
                ddeCodeIsNull = True  if schoolDdeCode == ''  else False 
                ddeNameIsNull = True  if schoolDdeName == ''  else False 
                schoolExists = False  if SchoolToGrade.objects.filter(code = schoolCode).count() == 0  else True 
                
                # Dry run
                if codeIsNull or nameIsNull or ddeCodeIsNull or schoolExists:
                    (status, tag) = ('error', 'error')

                    #status = 'Παρουσιάστηκαν Σφάλματα!'
                    # grid msg
                else:
                    (status, tag) = ('OK', 'info')

                    # Import in DB 
                    if (actionP =='doimport'):
                        try:
                            SchoolToGrade(code = schoolCode, name = schoolName, type = schoolType, 
                                    ddeCode = schoolDdeCode, ddeName =  schoolDdeName, ).save()
                            print "SCHOOL-TO-GRADE  IMPORT:", schoolCode, schoolName, schoolDdeCode, schoolDdeName
                            (status, msg, tag) = ('OK', "Επιτυχής εισαγωγή εγγραφής!", 'info')
                        except DatabaseError:
                            (status, msg, tag) = ('error', "Αδυναμία εισαγωγή εγγραφής!", 'error')
                            
                #responseData.append ( {'name': schoolName, 'type': lessonType , 'status': status })
                responseData.append ( {'code': schoolCode, 'name': schoolName , 'type': schoolType,\
                    'ddeCode': schoolDdeCode, 'ddeName': schoolDdeName, 'status': status })                    
                    
            # page ajax
            helperMessageLog(request, msg, tag)

            dictData = {'status': status, 'data': responseData}
            #print dictData
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')
    else: 
        raise Http404    


""" 
Import Specialty Records to DB using an uploaded CSV file 
"""
@csrf_exempt
def jsonFileCSVImportSpecialty (request):

    responseData = []
    status = 'ΟΚ! ΔΕΝ παρουσιάστηκαν Σφάλματα!'
    #errorsFound = True
    if request.is_ajax():
        actionP = request.POST.get('action', 'error')
        filename = request.POST.get('jqxinputFileName', '')
        print actionP, filename #, idxName, idxFirstRow
        
        #2.CHECK-IMPORT #3.DO-IMPORT
        #filename = 'uploads/LessonsCSV.csv'
        if (actionP =='checkimport') or (actionP =='doimport'):       
            ext = filename.split('.')[-1]
            if ext not in ['xls', 'xlsx', 'csv']:
                #return "File %s is not CSV, XLS, XLSX" % ( filename)
                #errorData.append("File %s is not CSV, XLS, XLSX" % (filename) )
                raise Http404    
                       
            dataReader = csv.reader(open(filename, mode='r'), delimiter=',', quotechar='"')
            next(dataReader, None)  # skip the headers
            (msg, tag) = ('', 'info')
            for row in dataReader:  #exclude 1st row
                code, name, = row[0], row[1]
                #print schoolCode, schoolName, schoolDdeCode, schoolDdeName, 
                codeIsNull = True  if code == ''  else False 
                nameIsNull = True  if name == ''  else False 
                specialtyExists = False  if Specialty.objects.filter(code = code).count() == 0  else True 
                if codeIsNull or nameIsNull or specialtyExists:
                    (status, tag) = ('error', 'error')
                else:
                    (status, tag) = ('OK', 'info')
                    if (actionP =='doimport'):         # Now, do Import in DB 
                        try:
                            Specialty (code = code, name = name, ).save()
                            print "SPECIALTY IMPORT:", code, name
                            (status, msg, tag) = ('OK', "Επιτυχής εισαγωγή εγγραφής!", 'info')
                        except DatabaseError:
                            (status, msg, tag) = ('error', "Αδυναμία εισαγωγή εγγραφής!", 'error')
                # 
                responseData.append ( {'code': code, 'name': name , 'status': status })

            # page ajax
            helperMessageLog(request, msg, tag)                                    
            dictData = {'status': status, 'data': responseData}
            #print dictData
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')
    else: 
        raise Http404    

""" Import Lessons to DB using an uploaded CSV file """
@csrf_exempt
def jsonFileCSVImportTeacher(request):

    responseData = []
    status = 'Success'
    #errorsFound = True
    if request.is_ajax():
        actionP = request.POST.get('action', 'error')
        filename = request.POST.get('jqxinputFileName', '')
        #idxName = request.POST.get('jqxinputIdxName', '')
        #idxFirstRow = request.POST.get('jqxinputFirstRow', '')
        print actionP, filename #, idxName, idxFirstRow
        
        #2.CHECK-IMPORT
        #3.DO-IMPORT
        #filename = 'uploads/LessonsCSV.csv'
        if (actionP =='checkimport') or  (actionP =='doimport'):       
            ext = filename.split('.')[-1]
            if ext not in ['xls', 'xlsx', 'csv']:
                #return "File %s is not CSV, XLS, XLSX" % ( filename)
                #errorData.append("File %s is not CSV, XLS, XLSX" % (filename) )
                raise Http404    
                       
            dataReader = csv.reader(open(filename, mode='r'), delimiter=',', quotechar='"')
            next(dataReader, None)  # skip the headers
            (msg, tag) = ('', 'info')
            for row in dataReader:  #exclude 1st row
                #t = Teacher(name='Βασίλης', surname='Τζουμάκας', codeAfm = '10000000', codeGrad = '02000000', codeSpec = 'ΠΕ19-01',)
                codeAfm, surname, name, codeSpec, codeGrad , phoneMob = row[0], row[1], row[2], row[3], row[4], row[5],
                #print teacherAFM, teacherSurname, teacherName, teacherCodeSpec, teacherCodeGrad  
                codeAfmIsNull = True  if codeAfm == ''  else False 
                surnameIsNull = True  if surname == ''  else False 
                nameIsNull = True  if name == ''  else False 
                codeGradIsNull = True  if codeGrad == ''  else False 
                codeSpecIsNull = True  if codeSpec == ''  else False 
                phoneMobIsNull = True  if phoneMob == ''  else False 

                teacherExists = False  if Teacher.objects.filter( codeAfm = codeAfm ).count() == 0  else True 
                if codeAfmIsNull or codeGradIsNull or nameIsNull or surnameIsNull or teacherExists:
                    (status, tag) = ('error', 'error')
                else:
                    (status, tag) = ('OK', 'info')
                    if (actionP =='doimport'):         # Now, do Import in DB 
                        try:
                            print "TEACHER IMPORT:", codeAfm, surname, name, codeGrad, codeSpec, codeSpec, phoneMob
                            Teacher(codeAfm = codeAfm, codeGrad = codeGrad, codeSpec = codeSpec, surname = surname, name = name, phoneMob=phoneMob).save()

                            (status, msg, tag) = ('OK', "Επιτυχής εισαγωγή εγγραφής!", 'info')
                        except DatabaseError:
                            (status, msg, tag) = ('error', "Αδυναμία εισαγωγή εγγραφής!", 'error')
                            
                responseData.append ( {'codeAfm': codeAfm, 'codeGrad': codeGrad, 'codeSpec': codeSpec, 'surname': surname , 'name': name, 'phoneMob':phoneMob, 'status': status })

            # page ajax
            helperMessageLog(request, msg, tag)
            
            dictData = {'status': status, 'data': responseData}
            #print dictData
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')
    else: 
        raise Http404    


""" FileUpload + CSV + Django DB QuerySet 
# request.FILES['fileToUpload'] | .content_type .name . read() .size .tmp_name(
?)

from django.conf import settings 
document_root=settings.STATIC_ROOT)
"""
@csrf_exempt
def jsonFileUpload(request):

    if request.method == 'POST':                
        # part 1. file upload
        if 'fileToUpload'not in request.FILES:
            return HttpResponse("Error", content_type='application/json')
        
        if request.FILES['fileToUpload'].size > 200000:
            return HttpResponse("File too Large", content_type='application/json')

        #toFilename = "%s/%s.%s" % ( 'uploads', baseName, ext)
        if not handle_uploaded_file(request.FILES['fileToUpload']):
            return HttpResponse("File Write", content_type='application/json')
                            
        # part 2. respond 
        #if action 
        msg = "success: File Write OK"
        toFilename = getUploadedFileName((request.FILES['fileToUpload'].name))
        #jsonData = {'msg':msg, 'filename': toFilename, 'data': {'name':"ΝΕΟΕΛΛΗΝΙΚΗ ΓΛΩΣΣΑ"}, {'name':"ΑΡΧΑΙΑ ΕΛΛΗΝΙΚΑ",}]}
        #print jsonData
        dictData = {'msg':msg, 'filename': toFilename, 'data': [{'name':"ΝΕΟΕΛΛΗΝΙΚΗ ΓΛΩΣΣΑ"}, {'name':"ΑΡΧΑΙΑ ΕΛΛΗΝΙΚΑ",}]}
        #dictData = {"msg": "OK"}
        #jsonResponse = json.dumps({'msg':msg, 'filename': toFilename, 'data': [{'name':"ΝΕΟΕΛΛΗΝΙΚΗ ΓΛΩΣΣΑ"}, {'name':"ΑΡΧΑΙΑ ΕΛΛΗΝΙΚΑ",}]})
        jsonResponse = json.dumps(dictData)
        print jsonResponse
        #return JsonResponse (dictData)
        return HttpResponse(jsonResponse, content_type='application/json')


""" Handle uploaded bytes from Temp to Local """
def handle_uploaded_file(myf):
    toFilename = getUploadedFileName(myf.name)
    
    """
    Code to handle existing file deletion
    def avatar_file_name(instance, filename):
        imgname = 'whatever.xyz'
        fullname = os.path.join(settings.MEDIA_ROOT, imgname)
        if os.path.exists(fullname):
            os.remove(fullname)
        return imgname
    """

    with open(toFilename, 'wb+') as destination:
        for chunk in myf.chunks():
            destination.write(chunk)
    #return (toFilename, True)
    return True

""" 
Handle uploaded bytes from Temp to Local 

from django.conf import settings 
document_root=settings.STATIC_ROOT)
"""
def getUploadedFileName(filename):
    UploadDir = settings.UPLOAD_DIR
    baseName = filename.split('.')[0]
    ext = filename.split('.')[-1]
    timeStamp = time.strftime("%Y%m%d-%H%M%S")    
    #print baseName, ext, timeStamp    
    #toFilename = "%s/%s-%s.%s" % ( 'uploads', baseName, timeStamp, ext)
    return "%s/%s-%s.%s" % ( UploadDir, baseName, timeStamp, ext)
    #return "%s/%s.%s" % ( UploadDir, baseName, ext)
    #return "%s/%s.%s" % ( 'uploads', baseName, ext)

 
