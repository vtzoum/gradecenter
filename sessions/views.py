#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.generic import CreateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.core.urlresolvers import reverse


""" 
Retrieving a cookie:
""" 
""" 
Retrieving a cookie:
""" 
def viewGetCookie(request):
    
    if 'cookie_name' in request.COOKIES:
        value = request.COOKIES['cookie_name']
        print request.COOKIES['cookie_name']    
    return HttpResponse(value)
    #return render( request, 'personel/home.html', {'cookie': value} )


""" 
Setting a cookie:
""" 
def viewSetCookie(request):
    greeting = "Cooking set!"

    #start = time.time()
    localtime = time.asctime( time.localtime(time.time()) )
    print "Local current time :", localtime
    #end = time.time()    
    cookieValue = "Local current time :(%s)", %(localtime)
    response = HttpResponse()
    response.set_cookie('cookie_name', cookieValue)
    return response



"""
class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)

# Create your views here.
def home(request):
    return render(request, 'personel/home.html', {'msg': 'Hello'})

"""

