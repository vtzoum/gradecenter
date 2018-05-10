#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import os, time
from django.contrib import messages
from django.core import serializers
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.http import Http404, HttpResponse,HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
#from django.views.generic import CreateView, View
#from django.views.generic.edit import CreateView, DeleteView, UpdateView
#from django.forms.models import model_to_dict
from django.db.models import QuerySet
from django.db import DatabaseError, IntegrityError, transaction

from models import Acceptance, Grader, Folder, Lesson, School, SchoolToGrade, Specialty, Teacher
from models import AcceptanceJoinTables, BookingJoinTables, GraderJoinTables

from helpScripts import * 


###################################
# BOOKING
# uses doBookingV2 (station, action, FolderID, GraderID)
###################################
def jsonBookingPost(request):
    
    #messages.add_message(request, messages.INFO, 'All items on this page have free shipping.',fail_silently=True)
    #messages.warning(request, 'jsonBookingPost!',fail_silently=True) #OK
    #print "jsonBookingPost> GET MESSAGES"
    #print messages.get_messages(request)


    #POST Requests
    status = 'Success'
    if request.is_ajax() and request.method == 'POST':        
        #messages.warning(request, 'jsonBookingPost!',fail_silently=True) #OK        
        # Take data
        actionPOST = request.POST.get("jqxinputAction", None)
        GraderID = request.POST.get("jqxinputGraderID", None)
        FolderID = request.POST.get("jqxinputFolderID", None)
        station = request.POST.get("jqxinputStation", None)
        print 'Station:%s GraderID:%s FolderID:%s actionPOST:%s' %(station, GraderID , FolderID, actionPOST)
        
        # Check Folder Status Vs Action
        folder = Folder.objects.get( id = FolderID )
        action = folder.getAction(station)
        print 'actionPOST:%s folder.getAction: %s' %(actionPOST, action)
        
        """
        if (folder.status == 0 || folder.status == 2)
            action =  0   #OUT
        elif (folder.status == 1)
            action =  1   #IN
        else  
            action =  -1 #UNKNOWN - STOP
        """

        # Do Booking > new encoding 2017-May
        status = doBookingV4 (request, int(station), int(actionPOST), FolderID, GraderID)
        # Do Booking > old encoding
        #status = doBookingV3 (request, int(station), int(actionPOST), FolderID, GraderID)
        
        # Return data
        dictData = {'status': status, }
        #print dictData
        jsonData = json.dumps(dictData)
        return HttpResponse(jsonData, content_type='application/json')                    




from django.core import serializers

###################################
# BOOKING (JSON) CRUD
###################################
""" 
CRUD for M:N Relation Booking 
Uses QuerySet Values to JSON 
fields: 
"""
def jsonBookingCrud(request):

    #Mesages
    #messages.warning(request, 'jsonBookingCrud',fail_silently=True) #OK
    
    dictData = []
    if request.is_ajax() and request.method == 'GET':
        id = request.GET.get('id', None)
        GraderID = request.GET.get('GraderID', None)
        # may2017: added LessonID filter for barcode-box support
        FolderID = request.GET.get('FolderID', None)
        action = request.GET.get('action', None)
        #print "action(%s), id(%d), GraderID(%d), FolderID(%d)" %(action, id)
        print "action:",action, " id", id, " GraderID:", GraderID, " FolderID:", FolderID

        if (action=="filter"):     
            dictData = BookingJoinTables(GraderID)
        else: 
            dictData = BookingJoinTables()
        
        # may2017: added FolderID filter for barcode-box support
        # could use the same approach for DraderID as well
        if (FolderID is not None):
            dictData = dictData.filter(FolderID=FolderID)

        #print 'Booking filter:', dictData
        
        jsonData = json_repr(list(dictData))
        #jsonData = serializers.serialize("json", list(dictData))
        #jsonData = json.dumps(list(dictData), default=date_handler)  # handle datetime JSON ser.
        #print 'JSON:',jsonData
        return HttpResponse(jsonData, content_type='application/json')

    #POST Requests
    if request.is_ajax() and request.method == 'POST':
        action = request.POST.get('action', None)
        id = request.POST.get('id', None)
        GraderID = request.POST.get('GraderID', None)
        print action, id, GraderID

        #ADD a single rentry (via post)
        if (action=="add"):

            actionPOST = request.POST.get("jqxinputAction", None)
            GraderID = request.POST.get("jqxinputGrader", None)
            FolderID = request.POST.get("jqxinputFolder", None)
            station = request.POST.get("jqxinputStation", None)
            # Check Folder Status Vs Action
            folder = Folder.objects.get( id = FolderID )
            action = folder.getAction()
            print 'Station:%s GraderID:%s FolderID:%s Action:%s' %(station, GraderID , FolderID, action)
            print 'actionPOST:%s action: %s' %(actionPOST)
            """
            if (folder.status == 0 || folder.status == 2)
                action =  0   #OUT
            elif (folder.status == 1)
                action =  1   #IN
            else  
                action =  -1 #UNKNOWN - STOP
            """
            # Do Booking 
            status = doBookingV3 (request, station, action, FolderID, GraderID)
            dictData = {'status': status, }
            #print dictData
            jsonData = json.dumps(list(dictData))  
            return HttpResponse(jsonData, content_type='application/json')                    


        #DELETE-LAST-ENTRY. We expect the correct id here
        # must check if related-rec. exist in DB
        #DELETE-LAST-ENTRY. We expect the correct id here
        # must check if related-rec. exist in DB
        elif (action=="delete") or (action=="deletelast"):
            #id = request.POST.get('id', None)
            id = request.POST.get('id', None)
            record = Booking.objects.get(id=id)
            print record
            (action, station) = (record.action, record.station)
            #record = Booking.objects.filter(GraderID=GraderID).order_by('-actionTime')[0]
            try:
                f = Folder.objects.get(id=record.FolderID.id)
                g = Grader.objects.get(id=record.GraderID.id)
                
                if station==0 and action==0:                # Apothiki -->                    
                    # update folder
                    #f.update(codeStatus=0)                 # 
                    f.codeStatus = 0                        # back to unassigned
                    f.codeLocation = 0                      # back to Apothiki
                    f.save()                 
                    # update grader
                    g.currentFolder= None                  # null Grader folder_id
                    g.currentFolderID= None                  # null Grader folder_id
                    g.save()                 
                    #msg = "Επιτυχής Πράξη!"                 
                    print "A Apothiki --> :back to Apothiki "
                elif station==0 and action==1:              # Apothiki <--
                    # update folder status 
                    if f.codeType==1 and f.codeStatus==0 :  # f(b)/unbooked: change to f(a)
                        f.codeType = 0                      # back to f(a) because it is f(b)
                    elif f.codeType==1 and f.codeStatus==2 : # f(b)/completed: do nothing
                        pass                                # back to f(a) because it is f(b)
                    
                    f.codeStatus = 1                        # back to booked
                    f.codeLocation = 1                      # back to grader
                    f.save()
                    #Update Grader Status
                    g.currentFolderID= f.id                   # null Grader folder_id
                    g.currentFolder = f.no                  # back to folder_id
                    g.save()

                    #msg = "Επιτυχής Πράξη!"
                    print "A2: Apothiki <-- : back to grader "

                elif station==1 and action==0:         # Filaxi -->
                    f.codeLocation = 2                 # back to Filaxi 
                    f.save()
                    print "A3 Filaxi-->: back to Filaxi"

                elif station==1 and action==1:         # Filaxi <--
                    f.codeLocation = 1                 # back to grader
                    f.save()
                    print "A4 Filaxi<--: back to grader"
                
                # delete
                record.delete()
                msg = "Επιτυχής διαγραφή εγγραφής Booking (id=%s) (delete/last)!" %(str(id))     #%(record.actionTime)
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()
                msg = "Αδυναμία διαγραφής εγγραφής! (delete/last)!"
                helperMessageLog(request, msg, tag='error')
            #dictData = {'msg':'Delete success!'}
            jsonData = json.dumps(msg)  
            return HttpResponse(jsonData, content_type='application/json')                    


    # DEFAULT 
    else: 
        dictData = BookingJoinTables()
        #print dictData
        jsonData = json_repr(list(dictData))
        #jsonData = serializers.serialize("json", list(dictData))
        #jsonData = json.dumps(list(dictData), default=date_handler)  # handle datetime JSON ser.
        #print jsonData 
        return HttpResponse(jsonData, content_type='application/json')




###################################
# ACCEPTANCE (JSON) CRUD
###################################
""" 
CRUD on FK:LessonID for M:N Relation Acceptance
fields: 
"""
def jsonAcceptanceCrud(request):
    
    dictData = []
    if request.is_ajax() and request.method == 'GET':
        id = request.GET.get('id', None)
        LessonID = request.GET.get('LessonID', None)
        action = request.GET.get('action', None)
        print action, id, LessonID

        if (action=="filter"):     # on LessonID
            dictData = AcceptanceJoinTables(LessonID)
        else: 
            dictData = AcceptanceJoinTables()
        print 'join:', dictData
        
        #print dictData
        jsonData = json_repr(list(dictData))            
        #jsonData = json.dumps(list(dictData), default=date_handler)  # handle datetime JSON ser.
        return HttpResponse(jsonData, content_type='application/json')

    if request.is_ajax() and request.method == 'POST':
        action = request.POST.get('action', None)
        id = request.POST.get('id', None)
        LessonID = request.POST.get('LessonID', None)
        #print action
        print action, id, LessonID

        #ADD a single rentry (via post)
        if (action=="add"):        # on LessonID
            LessonID = request.POST.get('jqxinputAcceptanceNewLesson', None)
            SchoolToGradeID = request.POST.get('jqxinputAcceptanceNewSchoolToGrade', None)

            lesson = Lesson.objects.get( id = LessonID )        
            school = SchoolToGrade.objects.get(id = SchoolToGradeID )  
            AcceptanceExists = False  if Acceptance.objects.filter(SchoolToGrade = school, LessonID = lesson).count() == 0  else True 
            if not (AcceptanceExists):
                try:    
                    Acceptance(LessonID = lesson, SchoolToGrade = school, ).save()
                    #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                    msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                    helperMessageLog(request, msg, tag='info')
                    status = 'Success'
                except DatabaseError:
                    transaction.rollback()   
                    msg = "Αδυναμία εισαγωγής εγγραφής!"
                    helperMessageLog(request, msg, tag='error')
            else: 
                #print 'AcceptanceExists:', lesson, school
                msg = "Υπάρχει ήδη σχετική εγγραφή (AcceptanceExists:(%-%))!" %(lesson, school)
                helperMessageLog(request, msg, tag='info')
                status = 'Error'
            
            dictData = {'status': status, }
            jsonData = json.dumps(list(dictData), default=date_handler)  # handle datetime JSON ser.
            return HttpResponse(jsonData, content_type='application/json')                    

        #ADD
        if (action=="addarray"):        # on LessonID
            status = 'Success'
            LessonID = request.POST.get('jqxinputAcceptanceNewLesson', None)
            SchoolToGradeArray = json.loads(request.POST['jqxinputAcceptanceNewTeacherArray'])
            #print 'POST Received:', jqxinputLesson, jqxinputTeacherArray        
            # CHECK Fail Conditions  | Pass to DB |  MUST CHECK FOR FAIL CONDITIONS
            LessonIDIsNull = True  if jqxinputLesson == ''  else False 
            SchoolToGradeArrayIsNull = True  if SchoolToGradeArray == ''  else False 
            
            if LessonIDIsNull or SchoolToGradeArrayIsNull:
                msg = "Ανύπαρκτα στοιχεία Μαθήματος ή Σχoλείου!"
                helperMessageLog(request, msg, tag='info')
                status = 'Error'
            else:
                lesson = Lesson.objects.get( id = LessonID )        # pk = # get Lesson Data 
                #print "Found in DB (LESSON):", lesson.name
                for SchoolToGradeID in SchoolToGradeArrayIsNull:
                    school = SchoolToGrade.objects.get(id = SchoolToGradeID )  # get Teacher Data 
                    #print "Found in DB (TEACHER):", teacher.surname
                    AcceptanceExists = False  if Acceptance.objects.filter(SchoolToGrade = school, LessonID = lesson).count() == 0  else True 
                    if not (AcceptanceExists):
                        #print 'No AcceptanceExists:', teacher,  lesson
                        # INSERT to DB > MUST CHECK FOR FAIL CONDITIONS
                        try:    
                            Acceptance(LessonID = lesson, SchoolToGrade = school, ).save()
                            #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                            #msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                            #helperMessageLog(request, msg, tag='info')
                        except DatabaseError:
                            transaction.rollback()   
                            msg = "Αδυναμία εισαγωγής εγγραφής!"
                            helperMessageLog(request, msg, tag='error')
                    else: 
                        print 'AcceptanceExists:', lesson, school
                        msg = "Υπάρχει ήδη σχετική εγγραφή! (AcceptanceExists)!"                 
                        helperMessageLog(request, msg, tag='info')
                        status = 'Error'

            #<!-- User Inputs -->
            #dictData = {'jqxinputLesson':jqxinputLesson, 'jqxinputTeacherArray': jqxinputTeacherArray, }
            dictData = {'status': status, }
            jsonData = json.dumps(list(dictData), default=date_handler)  # handle datetime JSON ser.
            return HttpResponse(jsonData, content_type='application/json')                    

        #ADD entry for all Schools at once (on LessonID)
        # BUT ist is called via Lesson.DoStatus or such 
        elif (action=="addfull"):
            LessonID = request.POST.get('LessonID', None)
            lesson = Lesson.objects.get( id = LessonID )        # pk = # get Lesson Data 
            if lesson.status == 0:
                # make a record for each school 
                for school in SchoolToGrade.objects.all():
                    try:    
                        Acceptance ( LessonID = lesson, SchoolToGradeID = school ).save() 
                        #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                        #msg = "Επιτυχής εισαγωγή εγγραφής! (addfull)"              
                        #helperMessageLog(request, msg, tag='info')
                    except DatabaseError:
                        transaction.rollback()   
                        msg = "Αδυναμία εισαγωγής εγγραφής!"
                        helperMessageLog(request, msg, tag='error')

                    #,  books = , booksAbscent = , booksZero = , status = ,  statusTime = , )
                lesson.status = 1
                lesson.save()
                #messages.info(request, 'Επιτυχής εισαγωγή μαζικών εγγραφών! (Addfull)',fail_silently=True)
                msg = "Επιτυχής εισαγωγή μαζικών εγγραφών! (Addfull)"
                helperMessageLog(request, msg, tag='info')
                return True

        #UPDATE
        elif (action=="update"):
            id = request.POST.get('id', None)
            books = request.POST.get('books', None)
            booksAbscent = request.POST.get('booksAbscent', None)
            booksZero = request.POST.get('booksZero', None)
            status = request.POST.get('status', None)
            notes = request.POST.get('notes', None)
            #print id, books, booksAbscent, booksZero, status
            #Folder.objects.filter(id=id).update(isCoordinator = helperStr2Bool(isCoordinator), isgraderC = helperStr2Bool(isgraderC), status = status, )           

            try:    
                record = Acceptance.objects.filter(id=id)
                record.update(books = books, booksAbscent = booksAbscent, booksZero = booksZero, status = status, notes = notes, )
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής τροποποίηση εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία τροποποίησης εγγραφής!"
                helperMessageLog(request, msg, tag='error')

            dictData = record.values()
            #print dictData
            jsonData = json.dumps(list(dictData), default=date_handler)  # handle datetime JSON ser.
            return HttpResponse(jsonData, content_type='application/json')
                                    

        #DELETE 
        elif (action=="delete"):
            id = request.POST.get('id', None)
            record = Acceptance.objects.filter(id=id).delete()
            try:
                record.delete()
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής διαγραφής εγγραφής!"
                helperMessageLog(request, msg, tag='info')
            except IntegrityError:
                transaction.rollback()  
                msg= "Αδυναμία διαγραφής εγγραφής!"
                helperMessageLog(request, msg, tag='info')

            dictData = {'msg':msg}
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')

    # DEFAULT 
    else: 
        dictData = AcceptanceJoinTables()        
        jsonData = json_repr(list(dictData))
        #jsonData = json.dumps(list(dictData), default=date_handler)  # handle datetime JSON ser.
        return HttpResponse(jsonData, content_type='application/json')


###################################
# GRADER
###################################
""" 
CRUD on FK:LessonID for M:N Relation Grader 
fields: 
"""
#def jsonGraderFKLessonCrud(request):
def jsonGraderCrud(request):
    
    dictData = []
    if request.is_ajax() and request.method == 'GET':
        id = request.GET.get('id', None)
        LessonID = request.GET.get('LessonID', None)
        action = request.GET.get('action', None)
        print action, LessonID

        if (action=="filter"):     # on LessonID
            dictData = GraderJoinTables(LessonID)
        else: 
            dictData = GraderJoinTables()
        #print dictData
        jsonData = json_repr(list(dictData))
        #jsonData = json.dumps(list(dictData))
        #jsonData = json.dumps(list(dictData), default=date_handler)  # handle datetime JSON ser.
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')

    if request.is_ajax() and request.method == 'POST':
        action = request.POST.get('action', None)        
        print action

        #ADD
        if (action=="add"):        # on LessonID
            #status = 'Success'
            jqxinputLesson = request.POST.get('jqxinputGraderNewLesson', None)
            jqxinputTeacherArray = json.loads(request.POST['jqxinputGraderNewTeacherArray'])
            #print 'POST Received:', jqxinputLesson, jqxinputTeacherArray        
            # CHECK Fail Conditions  | Pass to DB |  MUST CHECK FOR FAIL CONDITIONS
            lessonIsNull = True  if jqxinputLesson == ''  else False 
            teacherArrayIsNull = True  if jqxinputTeacherArray == ''  else False 
            
            if lessonIsNull or teacherArrayIsNull:
                msg = 'Ανύπαρκτα στοιχεία Μαθήματος ή Καθηγητών!'
                helperMessageLog(request, msg, tag='info')                
                #messages.error(request, msg, fail_silently=True)
                #status = 'Error'
            else:
                lesson = Lesson.objects.get( id = jqxinputLesson )        # pk = # get Lesson Data 
                #print "Found in DB (LESSON):", lesson.name
                (i, j)  = (0, 0)
                for jqxinputTeacher in jqxinputTeacherArray:
                    teacher = Teacher.objects.get(id = jqxinputTeacher )  # get Teacher Data 
                    #print "Found in DB (TEACHER):", teacher.surname
                    graderExists = False  if Grader.objects.filter(TeacherID = teacher, LessonID = lesson).count() == 0  else True 
                    if not (graderExists):
                        try:
                            Grader(LessonID = lesson, TeacherID = teacher, ).save()
                            i +=1
                        except DatabaseError:
                            transaction.rollback()   
                            msg = "Αδυναμία εισαγωγής εγγραφής!"
                            helperMessageLog(request, msg, tag='error')
                    else: 
                        j +=1

                # Handle display of 2 messages 
                if i >0 :                
                    msg = 'Επιτυχής εισαγωγή (%d) εγγραφών!' %(i)
                    helperMessageLog(request, msg, tag='info')                
                if j >0 :                 
                    msg = 'Υπήρξαν (%d) σχετικές εγγραφές!' %(j) #%(teacher.name,  lesson.name)
                    helperMessageLog(request, msg, tag='warning')                

            #dictData = {'jqxinputLesson':jqxinputLesson, 'jqxinputTeacherArray': jqxinputTeacherArray, }
            jsonData = json.dumps("ΟΚ")
            return HttpResponse(jsonData, content_type='application/json')                    

        #UPDATE
        elif (action=="update"):
            id = request.POST.get('id', None)
            isCoordinator = request.POST.get('isCoordinator', None).title()
            isgraderC = request.POST.get('isgraderC', None).title()
            status = request.POST.get('status', None)

            try:    
                record = Grader.objects.filter(id=id)
                record.update (isCoordinator = helperStr2Bool(isCoordinator), 
                    isgraderC = helperStr2Bool(isgraderC), status = status, )
                #'Αδυναμία εισαγωγής | τροποποίησης | διαγραφής | εγγραφής.'
                msg = "Επιτυχής τροποποίηση  εγγραφής!"                 
                helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία τροποποίησης εγγραφής!"
                helperMessageLog(request, msg, tag='error')
                
            dictData = record.values()
            jsonData = json.dumps(list(dictData))
            return HttpResponse(jsonData, content_type='application/json')
        
        #DELETE 
        elif (action=="delete"):
            id = request.POST.get('id', None)
            try:
                record = Grader.objects.filter(id=id).delete()
                msg = 'Επιτυχής διαγραφής εγγραφής!' #%(record.name)
                helperMessageLog(request, msg, tag='info')
                
            except DatabaseError:
                transaction.rollback()   
                msg = 'Αδυναμία διαγραφής εγγραφής!' 
                helperMessageLog(request, msg, tag='info')
                
            jsonData = json.dumps(msg)  #jsonData = json.dumps(status)
            return HttpResponse(jsonData, content_type='application/json')

    # DEFAULT 
    else: 
        dictData = GraderJoinTables()
        jsonData = json_repr(list(dictData))
        #jsonData = json.dumps(list(dictData), default=date_handler)  # handle datetime JSON ser.
        #jsonData = json.dumps(list(dictData))
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')


""" 
ajaxForm POST | returns JSON response 
Uses fk_fields = json.loads(request.POST['jqxinputGraderNewTeacherArray'])
to get array fdata from ajax POst request via .stringify
"""
def formPostGraderAddV0(request):

    status = 'Success'
    if request.is_ajax() and request.method == 'POST':

        jqxinputLesson = request.POST.get('jqxinputGraderNewLesson', None)
        #jqxinputTeacherArray = request.POST.getlist('jqxinputGraderNewTeacherArray[]', '')       # Received: [u'[7,6,1]'] AS STRING
        jqxinputTeacherArray = json.loads(request.POST['jqxinputGraderNewTeacherArray'])
        #print 'POST Received:', jqxinputLesson, jqxinputTeacherArray
        
        # CHECK Fail Conditions  | Pass to DB |  MUST CHECK FOR FAIL CONDITIONS
        lessonIsNull = True  if jqxinputLesson == ''  else False 
        teacherArrayIsNull = True  if jqxinputTeacherArray == ''  else False 
        
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
        #<!-- User Inputs -->
        #dictData = {'jqxinputLesson':jqxinputLesson, 'jqxinputTeacherArray': jqxinputTeacherArray, }
        dictData = {'status': status, }
        jsonData = json.dumps(dictData)
        #print 'jsonData:', jsonData
        return HttpResponse(jsonData, content_type='application/json')
    else:
        raise Http404    
        #return HttpResponse(html)


