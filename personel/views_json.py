#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
import csv
import json
import os, time
from urlparse import urlparse, parse_qs
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse,HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.core.serializers.json import DjangoJSONEncoder

from models import Acceptance, Booking, Dde, Folder, Grader, Lesson, Teacher, School
# Na dw pali


from django.forms.models import model_to_dict
from django.db.models import QuerySet
from django.db import IntegrityError
from django.db import transaction
from django.forms import *
from django.contrib import messages

from helpScripts import *



###################################
#LOHGIN REDIRECT >>> NO JASON 
###################################
def loginSuccess(request):
    """
    Redirects users based on whether they are in the admins group
    """
    print 'Login Success'

    if request.user.groups.filter(name="Apothiki").exists():
        # user is an admin
        print 'user is Apothiki'
        return redirect("/booking")
    elif request.user.groups.filter(name="Filaxi").exists():
        print 'user is Filaxi'
        return redirect("/booking")
    else:
        print 'ELSE'
        return redirect("other_view")

###################################
#GRID+DATAADAPTER test View
###################################
"""  """
#if request.is_ajax():
def jsonGridDataadapter(request):
    #action = request.GET.get('action', None)
    print "KEYS:", request.GET.keys()
    print "VALUES:", request.GET.values()
    searchField = request.GET.get('name_startsWith', '');
    #if 'Delete' in request.POST.values():
    dictData = Teacher.objects.filter(name__startswith = searchField).values().order_by('name') 
    #startswith contains
    #print dictData
    jsonData = json.dumps(list(dictData))
    return HttpResponse(jsonData, content_type='application/json')
 
###################################
# WIDGET to-use Data from DB (JSON)
###################################
""" 
QuerySet Values to JSON 
"""
def jsonDBTableDataDDE(request):
    if request.is_ajax():
        #dictData = SchoolToGrade.objects.filter(post__genders=1).exclude(post=None).order_by('-sort').distinct()
        #dictData = SchoolToGrade.objects.values('ddeCode', 'ddeName').order_by('ddeName').distinct()
        dictData = Dde.objects.values().order_by('name')
        #print dictData
        jsonData = json.dumps(list(dictData))
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')
    else: 
        raise Http404    
 

""" 
QuerySet Values to JSON 
"""
def jsonDBTableDataSpecialty(request):
    if request.is_ajax():
        #print 'JSON'
        dictData = Specialty.objects.values().order_by('code')
        #print dictData
        jsonData = json.dumps(list(dictData))
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')
    else: 
        #jsonData = json.dumps(['Null'])
        raise Http404    
 


###################################
# ACCEPTANCE
###################################
""" 
M:N Table + table-B data (aka _related)
Uses QuerySet Values to JSON 
"""
def jsonAcceptance(request):
    
    dictData = []
    if request.is_ajax() and request.method == 'GET':
        action = request.GET.get('action', '')
        print action        
        #print request.GET.get('filterscount', 'error')    
        if (action=="filter"):          
            LessonID = request.GET.get('LessonID', None)
            if LessonID is None:
                print "LessonID is None"
                raise Http404    
            dictData = RelatedAcceptanceInfo(LessonID)
            '''
            dictData = [ { "id":1, "books":10 , "booksAbscent":0 , "booksZero":0 , "status":1 , "statusTime":0  , 
                "SchoolToGradeID":0  , "code": 100  , "name":'LYKEIO'  , "type":0 } ] 
            '''            
            print dictData
            jsonData = json.dumps(list(dictData), default=date_handler)  # handle datetime JSON ser.
            #jsonData = json.dumps(list(relData))
            print jsonData
            return HttpResponse(jsonData, content_type='application/json')

    if request.is_ajax() and request.method == 'POST':
        action = request.POST.get('action', None)
        if (action == 'update'):
            #print "data:", data  
            id = request.POST.get('id', None)
            books = request.POST.get('books', None)
            booksAbscent = request.POST.get('booksAbscent', None)
            booksZero = request.POST.get('booksZero', None)
            status = request.POST.get('status', None)
            print id, books, booksAbscent, booksZero, status
            #Folder.objects.filter(id=id).update(isCoordinator = helperStr2Bool(isCoordinator), isgraderC = helperStr2Bool(isgraderC), status = status, )           
            Acceptance.objects.filter(id=id).update(books = books, booksAbscent = booksAbscent, booksZero = booksZero, status = status, )
            #print Grader.objects.filter(id=id).values()
            #return HttpResponse(result, content_type='application/json')        
            dictData = {'msg':'success'}
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')        
        """
        """
    #"Default SELECT(*) "
    print  "Default SELECT(*)"
    dictData = RelatedAcceptanceInfo()
    '''
    dictData = [ { "id":1, "books":10 , "booksAbscent":0 , "booksZero":0 , "status":1 , "statusTime":0  , 
        "SchoolToGradeID":0  , "code": 100  , "name":'LYKEIO'  , "type":0 } ] 
    '''
    print dictData
    jsonData = json.dumps(list(dictData), default=date_handler)  # handle datetime JSON ser.
    #jsonData = json.dumps(list(dictData))
    print jsonData
    return HttpResponse(jsonData, content_type='application/json')




""" Model to JSON """
def jsonModel(request):

    if request.is_ajax():
        # assuming dictDatais a model instance
        #serialized_obj = serializers.serialize('json', [ dictData, ])
        #print serialized_obj
        #prices = Price.objects.filter(product=product).values_list('price', 'valid_from')
        #prices_json = json.dumps(list(prices), cls=DjangoJSONEncoder)
        #jsonData = json.dumps(list(dictData), cls=DjangoJSONEncoder)
        #jsonData = json.dumps(list(dictData))
        #simplejson.dumps(list(people))
        """        
        json_res = []
        for record in records:
            json_obj = dict(myproperty = record.myproperty,)
            json_res.append(json_obj)
        return HttpResponse(json.dumps(json_res), mimetype='application/json')
        """


""" QuerySet to JSON """
def jsonQuerySet(request):
    
    if request.is_ajax():
        dictData = Teacher.objects.all().order_by('-name')
        print isinstance(dictData, QuerySet)
        data = serializers.serialize('json', dictData)
        return HttpResponse(data, content_type="application/json")


""" QuerySet Values to JSON """
def jsonQuerySetValues(request):
    
    if request.is_ajax():
        dictData = Teacher.objects.all().values()
        #print dictData 
        jsonData = json.dumps(list(dictDataValues))
        print jsonData
        return HttpResponse(jsonData, content_type='application/json')
    else: 
        raise Http404    



""" M:N Relation > QuerySet Values to JSON """
def jsonGraderMNV0(request):
    
    dictData = []
    if request.is_ajax() and request.method == 'GET':
        action = request.GET.get('action', '')
        print action
        #/jsongrader/action=filter&LessonID=5?filterscount=0&groupscount=0&sortorder=&pagenum=0&pagesize=10&recordstartindex=0&recordendindex=10&_=1469974862876
        # SELECT ... WHERE LessonID ... OR TeacherID ...
        if (action=="filter"):
            #print "# SELECT ... WHERE LessonID ... OR TeacherID ..."
            LessonID = request.GET.get('LessonID', None)
            #dictData = Lesson.objects.get(id=LessonID).graders.all().values()   #OK
            dictData = RelatedGraderInfo(LessonID)
            jsonData = json.dumps(list(dictData))
            #print jsonData
            return HttpResponse(jsonData, content_type='application/json')

    if request.is_ajax() and request.method == 'POST':
        action = request.POST.get('action', '')
        if (action=="update"):
            #data = request.POST.get('data', None)
            #print "data:", data  
            id = request.POST.get('id', None)
            isCoordinator = request.POST.get('isCoordinator', None).title()
            isgraderC = request.POST.get('isgraderC', None).title()
            status = request.POST.get('status', None)
                                    
            #Grader.objects.filter(id=id).update(isCoordinator = ast.literal_eval(isCoordinator), isgraderC = ast.literal_eval(isgraderC), status = status, )           
            Grader.objects.filter(id=id).update(isCoordinator = helperStr2Bool(isCoordinator), isgraderC = helperStr2Bool(isgraderC), status = status, )           
            #Grader.objects.filter(id=id).update(isCoordinator = isCoordinator, isgraderC = isgraderC, status = status, )
            #print Grader.objects.filter(id=id).values()
            #return HttpResponse(result, content_type='application/json')        
            dictData = {'msg':'success'}
            jsonData = json.dumps(dictData)
            #print jsonData
            return HttpResponse(jsonData, content_type='application/json')


        if (action=="delete"):
            id = request.POST.get('id', None)
            try:
                Grader.objects.filter(id=id).delete()
            except IntegrityError:
                transaction.rollback()   
	            #result = "error"
            dictData = {'msg':'Delete success!'}
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')

    #"Default SELECT(*) "
    dictData = RelatedGraderInfo()
    #print dictData
    jsonData = json.dumps(list(dictData))
    #print jsonData
    return HttpResponse(jsonData, content_type='application/json')


""" M:N Relation > QuerySet Values to JSON """
def jsonGrader(request):
    
    if request.is_ajax():    
        action = request.GET.get('action', 'error')
        print action
        print request.GET.get('LessonID', 'error')
        print request.GET.get('filterscount', 'error')
        #/jsongrader/action=filter&LessonID=5?filterscount=0&groupscount=0&sortorder=&pagenum=0&pagesize=10&recordstartindex=0&recordendindex=10&_=1469974862876

        # SELECT ... WHERE LessonID ... OR TeacherID ...
        if (action=="filter"):
            #print "# SELECT ... WHERE LessonID ... OR TeacherID ..."
            LessonID = request.GET.get('LessonID', None)
            #TeacherID = request.GET.get('TeacherID', None)
            dictData = Lesson.objects.get(id=LessonID).graders.all().values()   #
            #dictData = Grader.objects.filter(LessonID=LessonID).values()       # OK
        else: 
            #print "Default SELECT(*) "
            dictData = Lesson.objects.graders.all().values()                    #
            #dictData = Grader.objects.all().values()                           # OK
        
        #print dictData
        jsonData = json.dumps(list(dictData))
        print jsonData
        return HttpResponse(jsonData, content_type='application/json')
    else: 
        raise Http404    


""" QuerySet Values to JSON """
def jsonLessonStatus(request):
       
    if (not request.is_ajax()) and (not request.method == 'POST') :
        print "Request NOT ajax()) OR request NOT POST'"
        raise Http404
        
    if request.is_ajax() and request.method == 'POST':
        id = request.POST.get('id', None)
        status = request.POST.get('status', None)
        print id, status 
        if (id is None or status is None): 
            print "NONE"
            raise Http404
        
        l = Lesson.objects.get(id=id)
        """
        if lesson.status != status - 1:
            print 'Improper Action (To see staus 6-7)'
            raise Http404    
        """        
        if not l.changeStatus(int(status)):
            print "ERROR: lesson.changeStatus(status):"
            raise Http404    
                    
        dictData = {'msg':'Status Changed'}        
        jsonData = json.dumps(dictData)
        #jsonData = json.dumps(list(dictData))
        print jsonData
        return HttpResponse(jsonData, content_type='application/json')
    else: 
        dictData = {'msg':'Error'}
        jsonData = json.dumps(dictData)
        return HttpResponse(jsonData, content_type='application/json')
        #raise Http404    

""" 
M:N Table + table-B data (aka _related)
Uses QuerySet Values to JSON 
"""
"""
def jsonBooking(request):
    
    dictData = []
    #print action

    if request.is_ajax() and request.method == 'GET':
        action = request.GET.get('action', '')
        print action        
        #print request.GET.get('filterscount', 'error')
        #/jsongrader/action=filter&LessonID=5?filterscount=0&groupscount=0&sortorder=&pagenum=0&pagesize=10&recordstartindex=0&recordendindex=10&_=1469974862876
        # SELECT ... WHERE LessonID ... OR TeacherID ...
    
        if (action=="filter"):          
            #print "# SELECT ... WHERE LessonID ... OR TeacherID ..."
            GraderID = request.GET.get('GraderID', None)
            print GraderID
            #dictData = Folder.objects.get(LessonID=LessonID).graders.all().values()   #OK
            dictData = RelatedBookingInfo(GraderID)
            print dictData
            jsonData = json.dumps(list(dictData), default=date_handler)  # handle datetime JSON ser.
            #jsonData = json.dumps(list(relData))
            print jsonData
            return HttpResponse(jsonData, content_type='application/json')

    if request.is_ajax() and request.method == 'POST':
        action = request.POST.get('action', '')
        if (action=="update"):
            #data = request.POST.get('data', None)
            #print "data:", data  
            id = request.POST.get('id', None)
            no = request.POST.get('no', None).title()
            books = request.POST.get('books', None).title()
            type = request.POST.get('type', None).title()
            typeChar = request.POST.get('typeChar', None).title()
            status = request.POST.get('status', None)

            #Folder.objects.filter(id=id).update(isCoordinator = helperStr2Bool(isCoordinator), isgraderC = helperStr2Bool(isgraderC), status = status, )           
            Folder.objects.filter(id=id).update(no = no, books = books, type = type, typeChar = typeChar, status = status, )
            #print Grader.objects.filter(id=id).values()
            #return HttpResponse(result, content_type='application/json')        
            dictData = {'msg':'success'}
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')
        
        if (action=="delete"):
            id = request.POST.get('id', None)
            try:
                Grader.objects.filter(id=id).delete()
            except IntegrityError:
                transaction.rollback()   
	            #result = "error"
            dictData = {'msg':'Delete success!'}
            jsonData = json.dumps(dictData)
            return HttpResponse(jsonData, content_type='application/json')
    #"Default SELECT(*) "
    print  "Default SELECT(*)"
    dictData = RelatedBookingInfo()
    print dictData
    #all_objects = list(Restaurant.objects.all()) + list(Place.objects.all())
    #jsonData = json.dumps(list(dictData), cls = MyEncoder)
    jsonData = json.dumps(list(dictData), default=date_handler)  # handle datetime JSON ser.
    #jsonData = json.dumps(list(dictData))
    print jsonData
    return HttpResponse(jsonData, content_type='application/json')

"""

""" QuerySet Values to JSON """
def jsonLesson(request):
    if request.is_ajax():
        dictData = Lesson.objects.all().values()
        #print dictData
        jsonData = json.dumps(list(dictData))
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')
    else: 
        raise Http404    
 
""" QuerySet Values to JSON """
def jsonTeacher(request):
    if request.is_ajax():
        dictData = Teacher.objects.all().values()
        #print dictData
        jsonData = json.dumps(list(dictData))
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')
    else: 
        raise Http404    
 



''' View to server listbox Data'''
def jsonDataNCB(request):
    if request.is_ajax():
        dictArrayData = [{"CompanyName":"Ana Trujillo","ContactName":"Ana Trujillo","ContactTitle":"Owner","Address":"Avda.","City":"Mxico D.F.","Country":"Mexico"},
                {"CompanyName":"Antonio Moreno","ContactName":"Antonio Moreno","ContactTitle":"Owner","Address":"Mataderos 2312","City":"Mxico D.F.","Country":"Mexico"},
                {"CompanyName":"Around","ContactName":"Thomas Hardy","ContactTitle":"Sales","Address":"120 Hanover Sq.","City":"London","Country":"UK"},]
        #jsonData = json.dumps(dictArrayData)
        # As Dict Not As Array 
        dictArrayDataX2 = {"msg":"Success", "data": dictArrayData, }  
        print dictArrayDataX2
        jsonData = json.dumps(dictArrayDataX2)
        print jsonData
        return HttpResponse(jsonData, content_type='application/json')
    else:
        # check this if ERROR
        raise Http404    
 

def jsonDataNC(request):
    if request.is_ajax():
        dictData = [{"CompanyName":"Alfreds Futterkiste","ContactName":"Maria Anders","ContactTitle":"Sales Representative","Address":"Obere Str. 57","City":"Berlin","Country":"Germany"},{"CompanyName":"Ana Trujillo Emparedados y helados","ContactName":"Ana Trujillo","ContactTitle":"Owner","Address":"Avda. de la Constitucin 2222","City":"Mxico D.F.","Country":"Mexico"},{"CompanyName":"Antonio Moreno Taquera","ContactName":"Antonio Moreno","ContactTitle":"Owner","Address":"Mataderos 2312","City":"Mxico D.F.","Country":"Mexico"},{"CompanyName":"Around the Horn","ContactName":"Thomas Hardy","ContactTitle":"Sales Representative","Address":"120 Hanover Sq.","City":"London","Country":"UK"},{"CompanyName":"Berglunds snabbkp","ContactName":"Christina Berglund","ContactTitle":"Order Administrator","Address":"Berguvsvgen 8","City":"Lule","Country":"Sweden"},{"CompanyName":"Blauer See Delikatessen","ContactName":"Hanna Moos","ContactTitle":"Sales Representative","Address":"Forsterstr. 57","City":"Mannheim","Country":"Germany"},{"CompanyName":"Alfreds Futterkiste","ContactName":"Maria Anders","ContactTitle":"Sales Representative","Address":"Obere Str. 57","City":"Berlin","Country":"Germany"},{"CompanyName":"Ana Trujillo Emparedados y helados","ContactName":"Ana Trujillo","ContactTitle":"Owner","Address":"Avda. de la Constitucin 2222","City":"Mxico D.F.","Country":"Mexico"},{"CompanyName":"Antonio Moreno Taquera","ContactName":"Antonio Moreno","ContactTitle":"Owner","Address":"Mataderos 2312","City":"Mxico D.F.","Country":"Mexico"},{"CompanyName":"Around the Horn","ContactName":"Thomas Hardy","ContactTitle":"Sales Representative","Address":"120 Hanover Sq.","City":"London","Country":"UK"},{"CompanyName":"Berglunds snabbkp","ContactName":"Christina Berglund","ContactTitle":"Order Administrator","Address":"Berguvsvgen 8","City":"Lule","Country":"Sweden"},{"CompanyName":"Blauer See Delikatessen","ContactName":"Hanna Moos","ContactTitle":"Sales Representative","Address":"Forsterstr. 57","City":"Mannheim","Country":"Germany"},{"CompanyName":"Alfreds Futterkiste","ContactName":"Maria Anders","ContactTitle":"Sales Representative","Address":"Obere Str. 57","City":"Berlin","Country":"Germany"},{"CompanyName":"Ana Trujillo Emparedados y helados","ContactName":"Ana Trujillo","ContactTitle":"Owner","Address":"Avda. de la Constitucin 2222","City":"Mxico D.F.","Country":"Mexico"},{"CompanyName":"Antonio Moreno Taquera","ContactName":"Antonio Moreno","ContactTitle":"Owner","Address":"Mataderos 2312","City":"Mxico D.F.","Country":"Mexico"},{"CompanyName":"Around the Horn","ContactName":"Thomas Hardy","ContactTitle":"Sales Representative","Address":"120 Hanover Sq.","City":"London","Country":"UK"},{"CompanyName":"Berglunds snabbkp","ContactName":"Christina Berglund","ContactTitle":"Order Administrator","Address":"Berguvsvgen 8","City":"Lule","Country":"Sweden"},{"CompanyName":"Blauer See Delikatessen","ContactName":"Hanna Moos","ContactTitle":"Sales Representative","Address":"Forsterstr. 57","City":"Mannheim","Country":"Germany"}]
        #print dictData
        jsonData = json.dumps(dictData)
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')
    else:
        # check this if ERROR
        raise Http404    
 

def jsonData(request):
    if request.is_ajax():
        arrData = ["Affogato", "Americano", "Bicerin", "Breve", "Cafe Bombon", "Cafe au lait", 
                "Caffe Corretto", "Cafe Crema", "Caffe Latte", "Caffe macchiato", "Cafe melange", "Coffee milk", 
                "Cafe mocha", "Cappuccino", "Carajillo", "Cortado", "Cuban espresso", "Espresso", "Eiskaffee", 
                "The Flat White", "Frappuccino", "Galao", "Greek frappe coffee", "Iced Coffee", 
                "Indian filter coffee", "Instant coffee", "Irish coffee", "Liqueur coffee"]
        dictData = [{'coffeeName': coffee} for coffee in arrData]
        #print dictData

        jsonData = json.dumps(dictData)
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')
    else:
        # check this if ERROR
        raise Http404    
 


def json_get(request):
    if request.is_ajax():
        todo_items = ['Mow Lawn', 'Buy Groceries',]
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

#@csrf_exempt
def json_post(request):
    if request.is_ajax() and request.POST:
        data = {'message': "%s added" % request.POST.get('item')}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404


def more_todo(request):
    if request.is_ajax():
        todo_items = ['Mow Lawn', 'Buy Groceries',]
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404


def add_todo(request):
    if request.is_ajax() and request.POST:
        data = {'message': "%s added" % request.POST.get('item')}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404

''' Render a page with ajax call  '''
def json_page(request):
    msg = [1,2,3,4,5]
    html = render(request, 'json/index.html', {'msg': msg, 'variable': 'B', })
    return HttpResponse(html)


