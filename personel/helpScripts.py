#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import datetime
import decimal
import json
import os

from django.db import DatabaseError, IntegrityError, transaction
from django.db.models.base import ModelState
from django.http import Http404, HttpResponse,HttpResponseRedirect, HttpResponseNotFound  
from django.core.exceptions import PermissionDenied

from functools import wraps

from django import template 
from django.contrib import messages
from django.contrib.auth.models import Group 
from django.contrib.auth.decorators import user_passes_test

#from helpScripts import *
from models import Acceptance, Booking, Grader, Folder, Lesson, School, SchoolToGrade, Specialty, Teacher


""" 
Date: 2017-June 
Custom fuct. to count days in dbData dict for each Grader 
Because current Django impl. is SOMEHOW ....
"""
"""
def countDays(data):
    countDict = {}  # a Dict of Dicts
    for d in data:
        gid = d['GraderID_id']
        day = d['date']
        if gid not in countDict.keys():   # .count('date') > 1:
            countDict[gid]={}
            countDict[gid]['rec'].append(d)
        if countDict[gid]['']:
            if day not in countDict[gid]:
            countDict[gid]['date'].append(data[gid])
            countDict[gid].append(day)

    print countDict 
    #>>> countDict
    #{512: [u'2017-06-15', u'2017-06-16', u'2017-06-17', u'2017-06-18', u'2017-06-19'], 1: [u'2017-06-09',
"""

#GraderID__TeacherID__surname','GraderID__TeacherID__name','GraderID__TeacherID__afm
def countDays0(data):
    countDict = {}  # a Dict of Dicts
    for d in data:
        tid = d['GraderID__TeacherID__id']
        gsurname = d['GraderID__TeacherID__surname']
        gname = d['GraderID__TeacherID__name']
        gafm = d['GraderID__TeacherID__codeAfm']
        gcode = d['GraderID__TeacherID__codeGrad']
        date = d['date']
        
        gid = d['GraderID_id']
        #print gid, date
        if tid not in countDict.keys():   # .count('date') > 1:
            countDict[tid]={}
            countDict[tid]['dates']=[]
            countDict[tid]['surname']=gsurname
            countDict[tid]['name']=gname
            countDict[tid]['afm']=gafm
            countDict[tid]['code']=gcode

            countDict[tid]['GraderID_id']=gid

        if date not in countDict[tid]['dates']:
            countDict[tid]['dates'].append(date)
    return countDict

#Date: 2017-June 
def beep():
    print "\a"



#returns timedelta (hours, seconds) 
#td = datetime.timedelta(0,77) 
#td.total_seconds()
#td.seconds
#print "days (%2.2f) hours (%0.2f) minutes (%0.2f)" %(td.days, td.seconds//3600, (td.seconds//60)%60)
def td2DayHourMin(td):
    #return  u"(%2.0f)ΗΗ (%2.0f)ΩΩ (%2.0f)ΛΛ" %(td.days, td.seconds//3600, (td.seconds//60)%60)
    return  u"%2.0fH:%2.0fΩ:%2.0fΛ" %(td.days,td.seconds//3600,(td.seconds//60)%60)
    #>>> print('% 6.2f' % v)
    #return td.days, td.seconds//3600, (td.seconds//60)%60




#Date: 2017-May 
""" """
def helperMessageLog(request, msg='Null log', tag='info'):
    """
    Handles 3to1 statements for ajax messages & logging
    """
    if tag=='error':
        messages.error(request, msg, tag, fail_silently=True)
    elif tag=='info':
        messages.info(request, msg, tag, fail_silently=True)
    elif tag=='success':
        messages.warning(request, msg, tag, fail_silently=True)
    elif tag=='success':
        messages.warning(request, msg, tag, fail_silently=True)
    else: 
        messages.info(request, msg, tag, fail_silently=True)
    print msg


#Date: 2016-XXX 
""" """
def assignUserToGroup(userID, groupName):   
    user = Group.objects.get(id=userID)
    group = Group.objects.get(name=groupName)
    user.groups.add(group)
    

""" 
handle ... select_related json
from django.utils import simplejson
 def convert_to_json():
   uinfo = Userinfo.objects.filter(userId_id__in=inner_qs).values('userId__username', 'userImg', 'says', 'userId__first_name', 'city')σσ
   lusers = ValuesQuerySetToDict(users)
   response = simplejson.dumps(lusers)
   return response
"""
def valuesQuerySetToDict(vqs):
   return [item for item in vqs]

###################################
# HELP CONVERTERS
###################################
""" 
Dict of Values
""" 
def helperStr2Bool(val):
    return ast.literal_eval(val)

""" handle datetime JSON encoding errors"""
def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError
#print json.dumps(data, default=date_handler)


###################################
# OK: json_repr (needs optimization)
###################################
def json_repr(obj):
  """Represent instance of a class as JSON.
  Arguments:
  obj -- any object
  Return:
  String that reprent JSON-encoded object.
  """
  def serialize(obj):
    """Recursively walk object's hierarchy."""
    if isinstance(obj, (bool, int, long, float, basestring)):
      return obj
    elif isinstance(obj, dict):
      obj = obj.copy()
      for key in obj:
        obj[key] = serialize(obj[key])
      return obj
    elif isinstance(obj, list):
      return [serialize(item) for item in obj]
    elif isinstance(obj, tuple):
      return tuple(serialize([item for item in obj]))
    elif hasattr(obj, '__dict__'):
      return serialize(obj.__dict__)
    #Start / vtzoum added for datetime
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)
    elif isinstance(obj, ModelState):
        return None
    #End / vtzoum added for datetime
    else:
      return repr(obj) # Don't know how to handle, convert to string
  return json.dumps(serialize(obj))

"""

JSON: [{"actionTime": "datetime.datetime(2016, 8, 18, 4, 54, 13, tzinfo=<UTC>)", "GraderID_id": 46, "_GraderID_cache": {"status": 1, "currentFolder": "None", "_state": {"adding": false, "db": "default"}, "isCoordinator": false, "LessonID_id": 4, "TeacherID_id": 16, "id": 46, "isgraderC": true}, "_state": {"adding": false, "db": "default"}, "_FolderID_cache": {"no": 1, "_state": {"adding": false, "db": "default"}, "codeLocation": 0, "codeStatus": 4, "books": 25, "codeType": 1, "id": 1, "LessonID_id": 4}, "station": 0, "action": 0, "id": 2, "FolderID_id": 1}, {"actionTime": "datetime.datetime(2016, 8, 18, 4, 55, 26, tzinfo=<UTC>)", "GraderID_id": 46, "_GraderID_cache": {"status": 1, "currentFolder": "None", "_state": {"adding": false, "db": "default"}, "isCoordinator": false, "LessonID_id": 4, "TeacherID_id": 16, "id": 46, "isgraderC": true}, "_state": {"adding": false, "db": "default"}, "_FolderID_cache": {"no": 1, "_state": {"adding": false, "db": "default"}, "codeLocation": 0, "codeStatus": 4, "books": 25, "codeType": 1, "id": 1, "LessonID_id": 4}, "station": 1, "action": 1, "id": 3, "FolderID_id": 1}, {"actionTime": "datetime.datetime(2016, 8, 18, 4, 55, 47, tzinfo=<UTC>)", "GraderID_id": 46, "_GraderID_cache": {"status": 1, "currentFolder": "None", "_state": {"adding": false, "db": "default"}, "isCoordinator": false, "LessonID_id": 4, "TeacherID_id": 16, "id": 46, "isgraderC": true}, "_state": {"adding": false, "db": "default"}, "_FolderID_cache": {"no": 1, "_state": {"adding": false, "db": "default"}, "codeLocation": 0, "codeStatus": 4, "books": 25, "codeType": 1, "id": 1, "LessonID_id": 4}, "station": 1, "action": 0, "id": 4, "FolderID_id": 1}, {"actionTime": "datetime.datetime(2016, 8, 18, 4, 55, 53, tzinfo=<UTC>)", "GraderID_id": 46, "_GraderID_cache": {"status": 1, "currentFolder": "None", "_state": {"adding": false, "db": "default"}, "isCoordinator": false, "LessonID_id": 4, "TeacherID_id": 16, "id": 46, "isgraderC": true}, "_state": {"adding": false, "db": "default"}, "_FolderID_cache": {"no": 1, "_state": {"adding": false, "db": "default"}, "codeLocation": 0, "codeStatus": 4, "books": 25, "codeType": 1, "id": 1, "LessonID_id": 4}, "station": 0, "action": 1, "id": 5, "FolderID_id": 1}]
"""

###################################
# DateTimeEncoder
###################################
""" 
handle datetime JSON encoding errors V2 
Then use this class with your json dumps
b = json.dumps(a, cls = DateTimeEncoder)
"""
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
       if hasattr(obj, 'isoformat'):
           return obj.isoformat()
       elif isinstance(obj, decimal.Decimal):
           return float(obj)
       elif isinstance(obj, ModelState):
           return None
       else:
           return json.JSONEncoder.default(self, obj)


"""
V3
handle datetime JSON encoding errors V2 
Then use this class with your json dumps

b = json.dumps(data, cls = MyEncoder)
"""
class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))

        return json.JSONEncoder.default(self, obj)



###################################
# ARRAY INDEXERS
###################################

###################################
# BOOKING LOGIC HELPERS
###################################
"""
"""
# booking logic helpers
def graderIsOwnerOfFolder (FolderID=None, GraderID=None):
    
    f = Folder.objects.get( id = FolderID)
    g = Grader.objects.get(id = GraderID)
    #if g.currentFolder == f.no:
    if g.currentFolderID == f.id:
        return True        
    else: 
        return False
    #pass

"""
"""
def graderWasOwnerOfFolder (FolderID=None, GraderID=None):
    f = Folder.objects.get( id = FolderID)
    g = Grader.objects.get(id = GraderID)
    # exists previous αποθηκη(εισοδοσ, φακελοσ, βαθμολογ)
    if Booking.objects.filter(station=0, action=1, FolderID=FolderID, GraderID=GraderID).count()==1:
        return True
    else: 
        return False


"""
def graderIsOwnerOfFolder (FolderID=None, GraderID=None):
    
    f = Folder.objects.get( id = FolderID)
    g = Grader.objects.get(id=GraderID)
    if g.currentFolder == f.id:
        return True        
    else: 
        return False
    #pass
"""

"""
def graderWasOwnerOfFolder (FolderID=None, GraderID=None):
    f = Folder.objects.get( id = FolderID)
    g = Grader.objects.get(id=GraderID)
    # Exists previous ΑΠΟΘΗΚΗ(ΕΙΣΟΔΟΣ, ΦΑΚΕΛΟΣ, ΒΑΘΜΟΛΟΓ)
    if Registry.objects.filter(station=0, action=1, status=0, FolderID=FolderID, GraderID=GraderID ).count()==1:
        return True
    else: 
        return False
"""


# BOOKING LOGIC
#def doBooking (station=None, action=None, f=None):
"""
2017-May: 
Changed codeType/GRAD_TYPE/STATUS_TYPE encoding 
Added actionDuration handling for <<-- incoming actions

Check arguments and change Folder Status (and insert Booking)
GRAD_TYPE = ( (0, u'Φ(Α)'), (1, u'Φ(Β)'),(1, u'Φ(ΑΝΑ)'), )
GRAD_TYPE = ( (0, 'Κανονικός'), (1, 'Αναβαθμολόγηση'), )
LOCATION_TYPE = ( (0, 'Αποθήκη'), (1, 'Βαθμολογητής'), (2, 'Φύλαξη'), )    
STATUS_TYPE = ( (0, 'Αχρέωτος),  (1, 'Χρεωμένος(A)'), (2, 'Επιστροφή' ), )
codeStatus = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
codeType = models.PositiveSmallIntegerField(default=0, blank=False, null=False)    
codeLocation  = models.PositiveSmallIntegerField(default=0, blank=False, null=False)   # 0: 
"""
def doBookingV4 (request, station=None, action=None, FolderID=None, GraderID=None):

    #Handle Mesages
    #messages.success(request, 'SUCCESS!',fail_silently=False)
    #messages.warning(request, 'doBookingV3!',fail_silently=False) #OK

    if (station not in [0,1])  or  (action not in [0,1]):
        msg = "UNKNOWN ACTION/STATION!"                 
        helperMessageLog(request, msg, tag='error')
        return False

    # Go to DB
    status = 'Unkonwn'
    f = Folder.objects.get( id = FolderID)
    g = Grader.objects.get(id=GraderID)

    print 'station:',station, 'status:',f.codeStatus, 'action:',action , \
        'type:',f.codeType, 'currFID:',g.currentFolderID, 'WasOwn:',graderWasOwnerOfFolder (f.id, g.id)
    
    #ΑΠΟΘΗΚΗ - OUT 
    if f.codeType not in [0,1,2] :
        messages.error(request, 'Error. Μη αποδεκτός Τύπος Φακέλου!',fail_silently=False) #OK
        print "Error. Μη αποδεκτός Τύπος Φακέλου."
        return False


    #STATION: ΑΠΟΘΗΚΗ
    if (station == 0):
        #ACTION: -> (OUT)
        if (action == 0):
            print "ΑΠΟΘΗΚΗ - OUT"

            if  f.codeLocation != 0 :
                messages.error(request, 'Error. Ο Φάκελος ΔΕΝ είναι στην Αποθήκη!',fail_silently=False) #OK
                print "Error. Ο Φάκελος ΔΕΝ είναι στην Αποθήκη!"
                error = True
                return False
                #msg = "Αδυναμία Πράξης!"
                #helperMessageLog(request, msg, tag='error')
            
            if f.codeStatus not in [0] :
                messages.warning(request, 'Error. Ο Φάκελος ΔΕΝ είναι Διαθέσιμος!',fail_silently=False) #OK
                print "Error. Ο Φάκελος ΔΕΝ είναι Διαθέσιμος !"
                error = True
                return False

            if g.currentFolderID is not None:                 
                messages.warning(request, 'Error. Βαθμολογητής ΔΕΝ είναι Διαθέσιμος!',fail_silently=False) #OK
                print "Error: O Βαθμολογητής ΔΕΝ είναι Διαθέσιμος!"
                error = True
                return False
            
            # Grader Was Owner            
            if graderWasOwnerOfFolder (f.id, g.id):       
                messages.warning(request, 'Error: O Βαθμολογητής έχει βαθμολογησει ΞΑΝΑ τον ΙΔΙΟ Φάκελο!',fail_silently=False) #OK
                print "Error: O Βαθμολογητής έχει βαθμολογησει ΞΑΝΑ τον ΙΔΙΟ Φάκελο!"
                error = True
                return False
            
            # Folder = C and Grader not Allowed            
            if f.codeType == 2 and not g.isgraderC:             # Folder = C and Grader not Allowed
                messages.warning(request, 'Error. O Βαθμολογητής ΔΕΝ ΕΠΙΤΡΕΠΕΤΑΙ να βαθμολογησει τον Φάκελο (ΑΝΑΒΑΘΜΟΛΟΓΗΣΗ)!',fail_silently=False) #OK
                print "Error: O Βαθμολογητής ΔΕΝ ΕΠΙΤΡΕΠΕΤΑΙ να βαθμολογησει τον Φάκελο (ΑΝΑΒΑΘΜΟΛΟΓΗΣΗ)!"
                error = True
                return False
            
            else:                                           # PASS
                try:    #with transaction.atomic():
                    print "ΞΕΚΙΝΑ Η ΧΡΕΩΣΗ"
                    # make booking
                    Booking (FolderID = f , GraderID = g, action = action, station = station, wasTypeOf = f.codeType, \
                            operator=request.user, \
                            actionTime=datetime.datetime.now()).save()
                    #Update Folder Status
                    f.codeLocation = 1      # grader
                    f.codeStatus = 1        # book
                    f.save()
                    #Update Grader Status
                    g.currentFolder = f.no
                    g.currentFolderID = f.id
                    g.save()
                    msg = "Επιτυχής Πράξη!"                 
                    helperMessageLog(request, msg, tag='info')                    
                    return True
                except DatabaseError:
                    msg = "Αδυναμία Πράξης!"
                    helperMessageLog(request, msg, tag='error')
                    return False
                print 'Station(%s) Action(%s) Folder Status(%s)' % ('Αποθήκη', 'Χρέωση', '1-OUT')
        
        #ΑΠΟΘΗΚΗ 
        #ACTION: <- (IN) , Must set actionDuration here 
        elif (action == 1):
            print "ΑΠΟΘΗΚΗ - IN"
                        
            if (f.codeStatus not in [1]):
                messages.error(request, 'Error. O Φάκελος ΔΕΝ ΕΙΝΑΙ ΧΡΕΩΜΕΝΟΣ!',fail_silently=False) #OK
                print "Error. Ο Φάκελος ΔΕΝ ΕΙΝΑΙ ΧΡΕΩΜΕΝΟΣ!"
                error = True
                return False
            
            if  f.codeLocation != 1 :
                messages.error(request, 'Error. Ο Φάκελος ΔΕΝ είναι σε Βαθμολογητή!',fail_silently=False) #OK
                print "Error. Ο Φάκελος ΔΕΝ είναι σε Βαθμολογητή!"
                error = True
                return False
            
            #if g.currentFolder != f.no:
            if g.currentFolderID != f.id:
                messages.error(request, 'Error. O Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!',fail_silently=False) #OK
                print "Error: O Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!"
                error = True
                return False
            
            else:
                print 'make booking'              
                try:    #with transaction.atomic():
                    t0 = Booking.objects.filter(FolderID__id = f.id, GraderID__id = g.id, action = 0).order_by('-actionTime')[0].actionTime
                    #t0 = Booking.objects.get(FolderID__id = f.id, GraderID__id = g.id, action = 0).actionDuration
                    t1 = datetime.datetime.now()
                    tDurationNOMICRO=t1.replace(microsecond=0)-t0.replace(microsecond=0)                    
                    #print "time:-->", t0 , t1
                    Booking (FolderID = f , GraderID = g, action = action, station = station, wasTypeOf=f.codeType,\
                            operator=request.user, \
                            actionTime=datetime.datetime.now(), actionDuration=tDurationNOMICRO).save()                    
                    #Update Grader Status (release)
                    g.currentFolder = None  
                    g.currentFolderID = None  
                    g.save()                
                    #Update Folder Status+Type (# Status:return + Type: A-> B)
                    f.codeLocation = 0      # APOTHIKI 
                    if (f.codeType == 0 and f.codeStatus == 1): # Xrewmeno A => Axrewto B
                        f.codeType = 1                         # Update F(A) => F(B)
                        f.codeStatus = 0                       # Update Complete(A) => Axrewto(B)
                    else: 
                        f.codeStatus = 2                        # All others update to Complete
                    f.save()                            
                    msg = "Επιτυχής Πράξη!"                 
                    helperMessageLog(request, msg, tag='info')
                    return True
                except DatabaseError:
                    msg = "Αδυναμία Πράξης!"
                    helperMessageLog(request, msg, tag='error')
                    return False
                """                
                #Update Grader Status (release)
                g.currentFolder = None  
                g.save()                
                #Update Folder Status+Type (# Status:return + Type: A-> B)
                f.codeLocation = 0      # APOTHIKI 
                if (f.codeType == 0 and f.codeStatus == 1): # Xrewmeno A => Axrewto B
                    f.codeType = 1                         # Update F(A) => F(B)
                    f.codeStatus = 0                       # Update Complete(A) => Axrewto(B)
                else: 
                    f.codeStatus = 2                        # All others update to Complete
                f.save()                            
                #messages.success(request, 'Eπιτυχής ΠΡΑΞΗ!',fail_silently=False) #OK
                print 'Station(%s) Action(%s) Folder Status(%s)' % ('Αποθήκη', 'Παραλαβή', 'A->B Axre(B))')
                return True
                """                
                print 'Station(%s) Action(%s) Folder Status(%s)' % ('Αποθήκη', 'Παραλαβή', 'A->B Axre(B))')
    
    #STATION: ΦΥΛΑΞΗ
    elif (station == 1):
        print "ΦΥΛΑΞΗ"
        #ACTION: -> (OUT)
        if (action == 0):
            print "ΦΥΛΑΞΗ - OUT"
            if not f.codeStatus in [1]:
                messages.error(request, 'Error. O Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!',fail_silently=False) #OK
                print "Error. Ο Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!"
                error = True
                return False
            
            if f.codeLocation != 2:
                messages.error(request, 'Error. O Φάκελος ΔΕΝ ΕΙΝΑΙ στη ΦΥΛΑΞΗ!',fail_silently=False) #OK
                print "Error. Ο Φάκελος ΔΕΝ ΕΙΝΑΙ στη ΦΥΛΑΞΗ!"
                error = True
                return False
            
            #if g.currentFolder != f.no:
            if g.currentFolderID != f.id:
                messages.error(request, 'Error. O Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!',fail_silently=False) #OK
                print "Error: O Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!"
                error = True
                return False
            else:
                try:    #with transaction.atomic():
                    # make booking
                    Booking (FolderID = f , GraderID = g, action = action, station = station, wasTypeOf=f.codeType, \
                            actionTime=datetime.datetime.now(),\
                            operator=request.user).save()
                    f.codeLocation = 1
                    f.save()
                    msg = "Επιτυχής Πράξη!"                 
                    helperMessageLog(request, msg, tag='info')
                    return True
                except DatabaseError:
                    msg = "Αδυναμία Πράξης!"
                    helperMessageLog(request, msg, tag='error')
                    return False                
                print 'Station(%s) Action(%s) Folder Location(%s)' % ('Φύλαξη', 'Παράδοση(1)', '1')
            
        #ΦΥΛΑΞΗ
        #ACTION: <- (IN)
        elif (action == 1):
            print "ΦΥΛΑΞΗ - IN"
            if not f.codeStatus in [1]:
                messages.error(request, 'Error. O Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!',fail_silently=False) #OK
                print "Error. Ο Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!"
                error = True
                return False
            
            if f.codeLocation != 1:
                messages.error(request, 'Error. O Φάκελος ΔΕΝ είναι σε Βαθμολογητή!',fail_silently=False) #OK
                print "Error. Ο Φάκελος ΔΕΝ είναι σε Βαθμολογητή!"
                error = True
                return False
            
            #if g.currentFolder != f.no:
            if g.currentFolderID != f.id:
                messages.error(request, 'Error. O Βαθμολογητής ΔΕΝ έχει τον Φάκελο!',fail_silently=False) #OK
                print "Error. Ο Βαθμολογητής ΔΕΝ έχει τον Φάκελο."
                error = True
                return False
            
            # make booking
            else:
                try:    #with transaction.atomic():
                    # get latest TRANS 
                    t0 = Booking.objects.filter(FolderID__id = f.id, GraderID__id = g.id, action = 0).order_by('-actionTime')[0].actionTime
                    #t0 = Booking.objects.get(FolderID__id = f.id, GraderID__id = g.id, action = 0).order_by('actionTime').actionDuration
                    t1 = datetime.datetime.now()
                    #print "time:-->", t0 , t1
                    tDurationNOMICRO= t1.replace(microsecond=0)-t0.replace(microsecond=0)
                    
                    Booking (FolderID = f , GraderID = g, action = action, station = station, wasTypeOf=f.codeType, \
                            operator=request.user,\
                            actionTime=datetime.datetime.now(), actionDuration=tDurationNOMICRO).save()                    
                    #Booking (FolderID = f , GraderID = g, action = action, station = station, operator=request.user).save()                    
                    f.codeLocation = 2
                    f.save()
                    msg = "Επιτυχής Πράξη!"                 
                    helperMessageLog(request, msg, tag='info')
                    return True
                except DatabaseError:
                    msg = "Αδυναμία Πράξης!"
                    helperMessageLog(request, msg, tag='error')
                    return False                
                print 'Station(%s) Action(%s) Folder Location(%s)' % ('Φύλαξη', 'Παραλαβή(0)', '2')
    
    # in any othr case return False
    msg = "Passed IFS!"
    helperMessageLog(request, msg, tag='error')
    return False

    
# BOOKING LOGIC
#def doBooking (station=None, action=None, f=None):
"""
Check arguments and change Folder Status (and insert Booking)
GRAD_TYPE = ( (0, 'Κανονικός'), (1, 'Αναβαθμολόγηση'), )
LOCATION_TYPE = ( (0, 'Αποθήκη'), (1, 'Βαθμολογητής'), (2, 'Φύλαξη'), )    
STATUS_TYPE = ( (0, 'Αχρέωτος(A)'), (1, 'Αχρέωτος(Β)'), (2, 'Αχρέωτος(C)'), 
    (3, 'Χρεωμένος(A)'), (4, 'ΧρεωμένοςΒ)'), (5, 'Χρεωμένος(C)'), 
    (8, 'Επιστροφή' ), )
codeStatus = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
codeType = models.PositiveSmallIntegerField(default=0, blank=False, null=False)    
codeLocation  = models.PositiveSmallIntegerField(default=0, blank=False, null=False)   # 0: 
"""
def doBookingV3 (request, station=None, action=None, FolderID=None, GraderID=None):

    #Handle Mesages
    #messages.success(request, 'SUCCESS!',fail_silently=False)
    #messages.warning(request, 'doBookingV3!',fail_silently=False) #OK

    status = 'Unkonwn'
    f = Folder.objects.get( id = FolderID)
    g = Grader.objects.get(id=GraderID)

    print 'station:',station, 'status:',f.codeStatus, 'action:',action , \
        'type:',f.codeType, 'currFID:',g.currentFolderID, 'WasOwn:',graderWasOwnerOfFolder (f.id, g.id)
    
    #ΑΠΟΘΗΚΗ - OUT 
    if f.codeType not in [0,1] :
        messages.error(request, 'Error. Μη αποδεκτός Τύπος Φακέλου!',fail_silently=False) #OK
        print "Error. Μη αποδεκτός Τύπος Φακέλου."
        return False
    
    #STATION: ΑΠΟΘΗΚΗ
    if (station == 0):
        #ACTION: -> (OUT)
        if (action == 0):
            print "ΑΠΟΘΗΚΗ - OUT"
                              
            if  f.codeLocation != 0 :
                messages.error(request, 'Error. Ο Φάκελος ΔΕΝ είναι στην Αποθήκη!',fail_silently=False) #OK
                print "Error. Ο Φάκελος ΔΕΝ είναι στην Αποθήκη!"
                return False
            
            if f.codeStatus not in [0,1,2] :
                messages.warning(request, 'Error. Ο Φάκελος ΔΕΝ είναι Διαθέσιμος!',fail_silently=False) #OK
                print "Error. Ο Φάκελος ΔΕΝ είναι Διαθέσιμος !"
                return False

            if g.currentFolderID is not None:                 
                messages.warning(request, 'Error. Βαθμολογητής ΔΕΝ είναι Διαθέσιμος!',fail_silently=False) #OK
                print "Error: O Βαθμολογητής ΔΕΝ είναι Διαθέσιμος!"
                return False
                error = True
            
            # Grader Was Owner            
            if graderWasOwnerOfFolder (f.id, g.id):       
                messages.warning(request, 'Error: O Βαθμολογητής έχει βαθμολογησει ΞΑΝΑ τον ΙΔΙΟ Φάκελο!',fail_silently=False) #OK
                print "Error: O Βαθμολογητής έχει βαθμολογησει ΞΑΝΑ τον ΙΔΙΟ Φάκελο!"
                return False
                error = True
            
            # Folder = C and Grader not Allowed            
            if f.codeType == 1 and not g.isgraderC:             # Folder = C and Grader not Allowed
                messages.warning(request, 'Error. O Βαθμολογητής ΔΕΝ ΕΠΙΤΡΕΠΕΤΑΙ να βαθμολογησει τον Φάκελο (ΑΝΑΒΑΘΜΟΛΟΓΗΣΗ)!',fail_silently=False) #OK
                print "Error: O Βαθμολογητής ΔΕΝ ΕΠΙΤΡΕΠΕΤΑΙ να βαθμολογησει τον Φάκελο (ΑΝΑΒΑΘΜΟΛΟΓΗΣΗ)!"
                return False
                error = True
            
            else:                                           # PASS
                print "ΞΕΚΙΝΑ Η ΧΡΕΩΣΗ"
                # make booking
                #operator = request.user
                #gta = Game.objects.create(name="gta", owner=user)
                Booking (FolderID = f , GraderID = g, action = action, station = station, operator=request.user).save()
                #Update Folder Status
                f.codeLocation = 1      # grader
                f.codeStatus = f.codeStatus + 3   # this is hack due to coding
                f.save()
                #Update Grader Status
                g.currentFolder = f.no
                g.currentFolderID = f.id 
                g.save()
                messages.success(request, 'Eπιτυχής ΠΡΑΞΗ!',fail_silently=False) #OK
                print 'Station(%s) Action(%s) Folder Status(%s)' % ('Αποθήκη', 'Χρέωση', '1-OUT')
                #break
                return True
        
        #ΑΠΟΘΗΚΗ 
        #ACTION: <- (IN)
        elif (action == 1):
            print "ΑΠΟΘΗΚΗ - IN"
                        
            if (f.codeStatus not in [3,4,5]):
                messages.error(request, 'Error. O Φάκελος ΔΕΝ ΕΙΝΑΙ ΧΡΕΩΜΕΝΟΣ!',fail_silently=False) #OK
                print "Error. Ο Φάκελος ΔΕΝ ΕΙΝΑΙ ΧΡΕΩΜΕΝΟΣ!"
                return False
            
            if  f.codeLocation != 1 :
                messages.error(request, 'Error. Ο Φάκελος ΔΕΝ είναι σε Βαθμολογητή!',fail_silently=False) #OK
                print "Error. Ο Φάκελος ΔΕΝ είναι σε Βαθμολογητή!"
                return False
            
            #if g.currentFolder != f.no:             
            if g.currentFolderID != f.id:
                messages.error(request, 'Error. O Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!',fail_silently=False) #OK
                print "Error: O Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!"
                return False
            
            else:
                print 'make booking'
                Booking (FolderID = f , GraderID = g, action = action, station = station, operator=request.user).save()
                #Booking (FolderID = f , GraderID = g, action = action, station = station ).save()
                
                #Update Grader Status (release)
                g.currentFolder = None  
                g.currentFolderID = None  
                g.save()                
                #Update Folder Status+Type (# Status:return + Type: A-> B)
                f.codeLocation = 0      # APOTHIKI 
                if (f.codeType == 0 and f.codeStatus == 3): # Xrewmeno A => Axrewto B
                    f.codeStatus = 1                        # Update Complete(A) => Axrewto(B)
                else: 
                    f.codeStatus = 8                        # All others update to Complete
                f.save()                            
                messages.success(request, 'Eπιτυχής ΠΡΑΞΗ!',fail_silently=False) #OK
                print 'Station(%s) Action(%s) Folder Status(%s)' % ('Αποθήκη', 'Παραλαβή', 'A->B Axre(B))')
                return True
    
    #STATION: ΦΥΛΑΞΗ
    elif (station == 1):
        print "ΦΥΛΑΞΗ"
        #ACTION: -> (OUT)
        if (action == 0):
            print "ΦΥΛΑΞΗ - OUT"
            if not f.codeStatus in [3,4,5]:
                messages.error(request, 'Error. O Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!',fail_silently=False) #OK
                print "Error. Ο Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!"
                return False
            
            if f.codeLocation != 2:
                messages.error(request, 'Error. O Φάκελος ΔΕΝ ΕΙΝΑΙ στη ΦΥΛΑΞΗ!',fail_silently=False) #OK
                print "Error. Ο Φάκελος ΔΕΝ ΕΙΝΑΙ στη ΦΥΛΑΞΗ!"
                return False
            
            #if g.currentFolder != f.no:
            if g.currentFolderID != f.id:
                messages.error(request, 'Error. O Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!',fail_silently=False) #OK
                print "Error: O Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!"
                return False
            else:
                # make booking
                print 'make booking'
                Booking (FolderID = f , GraderID = g, action = action, station = station, operator=request.user).save()
                #Booking (FolderID = f , GraderID = g, action = action, station = station ).save()
                #Update Folder Status (Status: SAVE)
                f.codeLocation = 1
                #f.codeStatus = 
                f.save()
                messages.success(request, 'Eπιτυχής ΠΡΑΞΗ!',fail_silently=False) #OK
                print 'Station(%s) Action(%s) Folder Location(%s)' % ('Φύλαξη', 'Παράδοση(1)', '1')
                return True
            
        #ΦΥΛΑΞΗ
        #ACTION: <- (IN)
        elif (action == 1):
            print "ΦΥΛΑΞΗ - IN"
            if not f.codeStatus in [3,4,5]:
                messages.error(request, 'Error. O Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!',fail_silently=False) #OK
                print "Error. Ο Βαθμολογητής ΔΕΝ EXEI ΧΡΕΩΘΕΙ τον Φάκελο!"
                return False
            
            if f.codeLocation != 1:
                messages.error(request, 'Error. O Φάκελος ΔΕΝ είναι σε Βαθμολογητή!',fail_silently=False) #OK
                print "Error. Ο Φάκελος ΔΕΝ είναι σε Βαθμολογητή!"
                return False
            
            #if g.currentFolder != f.no:
            if g.currentFolderID != f.id:
                messages.error(request, 'Error. O Βαθμολογητής ΔΕΝ έχει τον Φάκελο!',fail_silently=False) #OK
                print "Error. Ο Βαθμολογητής ΔΕΝ έχει τον Φάκελο."
                return False

            # make booking
            else:
                Booking (FolderID = f , GraderID = g, action = action, station = station, operator=request.user).save()
                Booking (FolderID = f , GraderID = g, action = action, station = station ).save()
                #Update Folder Status (Status: OUT)
                f.codeLocation = 2
                f.save()                            
                messages.success(request, 'Eπιτυχής ΠΡΑΞΗ!',fail_silently=False) #OK
                print 'Station(%s) Action(%s) Folder Location(%s)' % ('Φύλαξη', 'Παραλαβή(0)', '2')
                return True
        # Error: UNAUTHORISED
        else:   
            messages.error(request, 'UNKNOWN ACTION!',fail_silently=False) #OK
            print "UNKNOWN ACTION"
            return False
    
    # Error: UNAUTHORISED
    else:   
        messages.error(request, 'UNAUTHORISED!',fail_silently=False) #OK
        print "PASSED IFS >> UNAUTHORISED"
        return False

# BOOKING LOGIC
#def doBooking (station=None, action=None, f=None):
"""
Check arguments and change Folder Status (and insert Booking)
"""

"""
def doBookingV2 (station=None, action=None, FolderID=None, GraderID=None):

    status = 'Unkonwn'
    f = Folder.objects.get( id = FolderID)
    g = Grader.objects.get(id=GraderID)

    print station, f.status , action , f.type, g.currentFolder, graderWasOwnerOfFolder (f.id, g.id)
    
    #ΑΠΟΘΗΚΗ
    print "1"
    if station == 0:
        print "2"
        
        # FolderIs(IDLE)+Action(OUT)
        if f.status == 0 and action == 0:
            print "00"
            
            if g.currentFolder is not None:                 # Grader is NOt available
                print "Error: Grader is NOT available!"
            # Grader Was Owner            
            elif graderWasOwnerOfFolder (f.id, g.id):       
                print "Error: Grader Was Owner!"
            # Folder = C and Grader not Allowed            
            elif f.type==2 and not g.isgraderC:             # Folder = C and Grader not Allowed
                print "Error: Grader not allowed to Grade C Folder!"
            else:                                           # PASS
                print "Start make booking"
                # make booking
                Booking (FolderID = f , GraderID = g, action = action, station = station ).save()
                #Update Folder Status
                f.status = 1
                f.save()
                #Update Grader Status
                g.currentFolder = f.id 
                g.save()
                print 'Station(%s) Action(%s) Folder Status(%s)' % ('Αποθήκη', 'Χρέωση', '1-OUT')
                #break
        
        # FolderIs(OUT)+Action(IN)        
        elif f.status == 1 and action == 1:
            # Grader NOT Owner
            if g.currentFolder != f.id:             
                print "Error: Grader is NOT owner of Folder !"
            else:
                # make booking
                Booking (FolderID = f , GraderID = g, action = action, station = station ).save()
                #Update Grader Status (release)
                g.currentFolder = None  
                g.save()                
                print 'make booking'
                #Update Folder Status+Type (# Status:return + Type: A-> B)
                if f.type == 0: #A
                    f.type = 1                          
                    f.status = 0                        
                    f.save()                            
                    print 'Station(%s) Action(%s) Folder Status(%s)' % ('Αποθήκη', 'Παραλαβή', 'A->B RETURN 90)')
                #Update Folder Status (# Status:complete)
                else: 
                    f.status = 4                        
                    f.save()                            
                    print 'Station(%s) Action(%s) Folder Status(%s)' % ('Αποθήκη', 'Παραλαβή', 'B COMPLETE (4)')
        #Error
        else:
            print "Error in Station 0."

    
    #ΦΥΛΑΞΗ
    if station == 1:
        
        # FolderIs (OUT)+Action( IN <- )
        if f.status == 1 and action == 1:
            # Grader NOT Owner
            if g.currentFolder != f.id:
                print "Error. Grader IS NOT owner of Folder !"
            else:
                # make booking
                Booking (FolderID = f , GraderID = g, action = action, station = station ).save()
                #Update Folder Status (Status: SAVE)
                f.status = 2                
                f.save()
                print 'Station(%s) Action(%s) Folder Status(%s)' % ('Φύλαξη', 'Παραλαβή', '2-SAVE')
        
        # FolderIs(SAVE)+Action(OUT ->)
        elif f.status == 2 and action == 0:
            # Grader NOT Owner
            if g.currentFolder != f.id:         
                print "Error. Grader IS NOT owner of Folder !"
            # make booking
            else:
                Booking (FolderID = f , GraderID = g, action = action, station = station ).save()
                #Update Folder Status (Status: OUT)
                f.status = 1                        
                f.save()                            
                print 'Station(%s) Action(%s) Folder Status(%s)' % ('Φύλαξη', 'Παράδοση', '1-OUT')
        
        # Error: UNAUTHORISED
        else:   
            print "Error in Station 1"

    
    print 'PASSED IFS'

"""
   
#def doBooking (station=None, action=None, f=None):
"""
Check arguments and change Folder Status (and insert Booking)
"""
"""
def doBooking (station=None, action=None, FolderID=None, GraderID=None):

    f = Folder.objects.get( id = FolderID)
    g = Grader.objects.get(id=GraderID)
    #ΑΠΟΘΗΚΗ
    if station == 0:
        if f.status == 0 and action == 0:   # FolderIs(IDLE)+Action(OUT)
            if g.currentFolder is None:     # Grader is available
                print "Grader is available!"
                # make booking
                Registry (FolderID = f , GraderID = g, action = action, station = station ).save()
                f.status = 1
                f.save()
                g.currentFolder = f.id 
                g.save()
                print 'Station(%s) Action(%s) Folder Status(%s)' % ('Αποθήκη', 'Χρέωση', '1-OUT')
                #break
            else: 
                print "Error: Grader NOT available!"
        elif f.status == 1 and action == 1: # FolderIs(OUT)+Action(IN)
            if g.currentFolder == f.id:
                print "Grader IS owner of Folder !"
                #break
                # make booking
                Registry (FolderID = f , GraderID = g, action = action, station = station ).save()
                g.currentFolder = None  # Grader release
                g.save()
                if f.type == 0: #A
                    f.type = 1                          # Folder type A-> B
                    f.status = 0                        # Folder return 
                    f.save()                            # Folder type A-> B
                    print 'Station(%s) Action(%s) Folder Status(%s)' % ('Αποθήκη', 'Παραλαβή', '3-RETURN')
                    #break
                else: 
                    f.status = 4                        # Folder Complete
                    f.save()                            # Folder type A-> B
                    print 'Station(%s) Action(%s) Folder Status(%s)' % ('Αποθήκη', 'Παραλαβή', '3-RETURN')
                    #break
            else: 
                print "Error: Grader NOT Owner!"
        else: 
            print "Error in Station 0."
            #break
        
    #ΦΥΛΑΞΗ
    if station == 1: 
        if f.status == 1 and action == 1: # FolderIs(OUT)+Action(IN)
            if g.currentFolder == f.id:
                print "Error. Grader IS owner of Folder !"
                #break
                # make booking
                Registry (FolderID = f , GraderID = g, action = action, station = station ).save()
                f.status = 2                # Folder SAVE
                f.save()       
                print 'Station(%s) Action(%s) Folder Status(%s)' % ('Φύλαξη', 'Παραλαβή', '2-SAVE')
                #break
            else:
                print "Error. Grader NOT owner of Folder !"
        
        elif f.status == 2 and action == 0: # FolderIs(SAVE)+Action(OUT)
            if g.currentFolder == f.id:
                print "Error. Grader IS owner of Folder !"
                #break
                # make booking
                Registry (FolderID = f , GraderID = g, action = action, station = station ).save()
                f.status = 1                        # Folder OUT
                f.save()                            # Folder OUT
                print 'Station(%s) Action(%s) Folder Status(%s)' % ('Φύλαξη', 'Παράδοση', '1-OUT')
                #break
            else:
                print "Error. Grader NOT owner of Folder !"
        
        else:   # UNAUTHORISED
            print "Error in Station 1"
            #break
            
"""





