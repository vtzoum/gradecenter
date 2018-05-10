#!/usr/bin/env python
# -*- coding: utf-8 -*-

#python manage.py shell

from personel.models import * 
from personel.helpScripts import * 
'''
SOS Field DEPENDENCIES in MODELS 

class Meta:
    unique_together = (('first_name', 'last_name'),)
'''

#////////////////////////
# BOOKING > RELATION M:N 
#////////////////////////
from personel.models import * 
from personel.helpScripts import * 

l = Lesson.objects.get(id=4)        # 
f = Folder.objects.get( id = 1)  # ΒΙΟΛΟΓΙΑ - Φ1
g = Grader.objects.get(id=46)       # ΑΘΑΝΑΣΟΠΟΥΛΟΥ


#OK
Booking.objects.all().values()
Booking.objects.filter( GraderID = g).all().values()   
Booking.objects.filter( GraderID = 46).all().values()

#////////////////////////
# FOLDER 
#////////////////////////
#RELATED > 
Folder.objects.get(id=1).bookings.all()       # Grader
Grader.objects.get(id=46).folder_set.all()
Grader.objects.get(id=46).folder_set.all().values()
Grader.objects.get(id=46).booking_set.all().values()


#////////////////////////
# BOOKING LOGIC
#////////////////////////
#def doBooking (station=None, action=None, f=None):
"""
Check arguments and change Folder Status (and insert Booking)
GRAD_TYPE = ( (0, 'Κανονικός'), (1, 'Αναβαθμολόγηση'), )
LOCATION_TYPE = ( (0, 'Αποθήκη'), (1, 'Βαθμολογητής'), (2, 'Φύλαξη'), )    
STATUS_TYPE = ( (0, 'Αχρέωτος(A)'), (1, 'Αχρέωτος(Β)'), (2, 'Αχρέωτος(C)'), 
    (3, 'Χρεωμένος(A)'), (4, 'ΧρεωμένοςΒ)'), (5, 'Χρεωμένος(C)'), 
    (, 'Επιστροφή' ), )
codeStatus = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
codeType = models.PositiveSmallIntegerField(default=0, blank=False, null=False)    
codeLocation  = models.PositiveSmallIntegerField(default=0, blank=False, null=False)   # 0: 

def doBookingV3 (station=None, action=None, FolderID=None, GraderID=None):
"""

from personel.models import * 
from personel.helpScripts import * 

""" run the tests """
f = Folder.objects.get( id = 1)     # βιολογια - φ1
g = Grader.objects.get(id=46)       # αθανασοπουλου
#def doBookingV3 (station=None, action=None, FolderID=None, GraderID=None):

doBookingV3 (0, 0, 1, 46)     # xrewsi:ok
doBookingV3 (0, 0, 1, 46)     # xrewsi pali: is error 
doBookingV3 (1, 1, 1, 47)     # filaksi:paradosi:notowner: is error 
doBookingV3 (1, 1, 1, 46)     # filaksi:paradosi:owner: ok

doBookingV3 (0, 1, 1, 46)     # apothiki:paralavi:owner: error (is in filaksi)
doBookingV3 (1, 0, 1, 47)     # filaksi:paralavi:notowner: is error 
doBookingV3 (1, 0, 1, 46)     # filaksi:paralavi:owner: ok 
doBookingV3 (0, 1, 1, 46)     # apothiki:paralavi:owner: ok now


#test
print graderwasowneroffolder (1, 46)  # wasowner is true



l = Lesson.objects.get(id=1)            # 
f = Folder.objects.get( id = 28)     
g = Grader.objects.get(id=289)          # 
u = User.objects.get(id=11)          # 

#A --> OUT
Booking (FolderID=f, GraderID=g, action=0,station=0, wasTypeOf=f.codeType,operator=u, actionTime=datetime.datetime.now()).save()

#F <--
t0 = Booking.objects.filter(FolderID__id = f.id, GraderID__id = g.id, action = 0).order_by('-actionTime')[0].actionTime
t1 = datetime.datetime.now()
# Update to ERASE MICROSECOND
#datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
tdur=t1.replace(microsecond=0) - t0.replace(microsecond=0)
Booking (FolderID=f, GraderID=g, action=1,station=1, wasTypeOf=f.codeType,operator=u,actionTime=datetime.datetime.now(), actionDuration=tdur).save() 
#F -->
Booking (FolderID=f, GraderID=g, action=0, station=1, wasTypeOf=f.codeType, actionTime=datetime.datetime.now(),operator=u).save()



