#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import datetime
import decimal
import json
import os

from django.db.models.base import ModelState
from django.http import Http404, HttpResponse,HttpResponseRedirect, HttpResponseNotFound  
from django.core.exceptions import PermissionDenied


from functools import wraps


from django import template 
from django.contrib.auth.models import Group 
from django.contrib.auth.decorators import user_passes_test

from models import Acceptance, Booking, Grader, Folder, Lesson, School, SchoolToGrade, Specialty, Teacher

""" 

"""
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
    else:
      return repr(obj) # Don't know how to handle, convert to string
  return json.dumps(serialize(obj))

###################################
# UNTESTED MongoEncoder
###################################
"""
Calling it as simple as

data = json.dumps(data, cls=MongoEncoder)
"""
class MongoEncoder(json.JSONEncoder):
    def default(self, v):
        types = {
            'ObjectId': lambda v: str(v),
            'datetime': lambda v: v.isoformat()
        }
        vtype = type(v).__name__
        if vtype in types:
            return types[type(v).__name__](v)
        else:
            return json.JSONEncoder.default(self, v)



###################################
# CustomTypeEncoder
###################################
TYPES = { 'Teacher': Teacher,
    'Lesson': Lesson, 
    'Grader': Grader, 
    'Bookin': Booking, 
}

class CustomTypeEncoder(json.JSONEncoder):
    """A custom JSONEncoder class that knows how to encode core custom
    objects.

    Custom objects are encoded as JSON object literals (ie, dicts) with
    one key, '__TypeName__' where 'TypeName' is the actual name of the
    type to which the object belongs.  That single key maps to another
    object literal which is just the __dict__ of the object encoded."""

    def default(self, obj):
        if isinstance(obj, TYPES.values()):
            key = '__%s__' % obj.__class__.__name__
            return { key: obj.__dict__ }
        return json.JSONEncoder.default(self, obj)


    def CustomTypeDecoder(dct):
        if len(dct) == 1:
            type_name, value = dct.items()[0]
            type_name = type_name.strip('_')
            if type_name in TYPES:
                return TYPES[type_name].from_dict(value)
        return dct


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
# BOOKING LOGIC HELPERS
###################################
"""
"""
# booking logic helpers
def graderIsOwnerOfFolder (FolderID=None, GraderID=None):
    
    f = Folder.objects.get( id = FolderID)
    g = Grader.objects.get(id = GraderID)
    if g.currentFolder == f.id:
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
Check arguments and change Folder Status (and insert Booking)
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
    

#def doBooking (station=None, action=None, f=None):
"""
Check arguments and change Folder Status (and insert Booking)
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
            
    
