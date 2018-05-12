#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast, json
from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.generic import CreateView, View
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.decorators.csrf import csrf_exempt

from personel.models import * 



""" ajaxForm POST | returns JSON response """
def formPost(request):

    #print "POST:", request.POST
    if request.is_ajax() and request.method == 'POST':
        jqxinputFileName = request.POST.get("jqxinputFileName", "error")
        jqxinputIdxName = request.POST.get("jqxinputIdxName", "")
        jqxinputFirstRow = request.POST.get("jqxinputFirstRow", "")
        if True:
            pass
            #codeAfm = request.GET.get('codeAfm', None)
            #return HttpResponse(result, content_type='application/json')
        
        # return JSON         
        #<!-- User Inputs -->
        dictData = {'jqxinputFileName':jqxinputFileName, 'jqxinputIdxName': jqxinputIdxName, 'jqxinputFirstRow':jqxinputFirstRow, }
        #dictData = {'jqxinputFileName':'myName.txt', 'jqxinputIdxName': 1, 'jqxinputFirstRow':2, }
        jsonData = json.dumps(dictData)
        #print jsonData
        return HttpResponse(jsonData, content_type='application/json')
        #html = render(request, 'ajax/h1.html', {'data': data, 'postData': [g, lg,],})
        #return HttpResponse(html)         
    else:
        #html = '<p>This is not ajax or POST request </p>'      
        raise Http404    
        #return HttpResponse(html)


''' NO: SEND HTML Template data via ajax to the ajax page'''
def ajax_get(request):
    
    if request.is_ajax():

        if request.method == 'GET':        
            g = request.GET.get('postData', 'You submitted nothing!')
            lg = request.GET.getlist('postData')
                
        html = render(request, 'ajax/h1.html', 
                {'data': data, 'postData': [g, lg, p, lp],})
        #html = render(request, 'ajax/h1.html', {'data': data,})
        return HttpResponse(html)         
    else:
        html = '<p>This is not ajax</p>'      
        return HttpResponse(html)

@csrf_exempt
def ajax_data(request):
    
    data = [1,2,3,4,5]

    if request.is_ajax():
        
        if request.method == 'GET':
            x = request.GET.get('postData', 'You submitted nothing!')
            lx = request.GET.getlist('postData')

        if request.method == 'POST':
            x = request.POST.get('postData', 'You submitted nothing!')
            lx = request.POST.getlist('postData')
        
        '''
        if request.method == 'GET':
            data = 'You submitted: %r' % request.GET['postData']
        #ajax POST
        elif request.method == 'POST':
            #assume [postData]
            data = 'You submitted: %r' % request.GET.getlist('postData')
        #no ajax
        else:
            data = 'You submitted nothing!'    
        '''
        
        html = render(request, 'ajax/h1.html', 
                {'data': data, 'postData': [x, lx],})
        #html = render(request, 'ajax/h1.html', {'data': data,})
        return HttpResponse(html)         
    else:
        html = '<p>This is not ajax</p>'      
        return HttpResponse(html)



''' Render a page with ajax call  '''
def ajax_page(request):
    msg = [1,2,3,4,5]
    html = render(request, 'ajax.html', {'msg': msg, 'variable': 'B', })
    return HttpResponse(html)



class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)


def home(request):
    return HttpResponse('Home!')


