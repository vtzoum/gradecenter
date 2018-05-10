#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import time

from django import forms
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.shortcuts import render
#from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View
#from modelsDemo import Contact

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User
from helpScripts import *


#########################################
# ER Page Views
#########################################
#@group_required('admins','editors')
#@login_required(login_url="login/")
#@group_required('Grammateia')
def pageSchoolToGrade(request):
    return render(request,"ui-final/schooltograde.html")
    #return render(request,"ui-final/schooltograde.html")


#########################################
# JINJA MESSAGES
#########################################                                       
def viewJinja2MessageAjax(request):
    #Handle Mesages
    messages.warning(request, 'WARNING!',fail_silently=True) #OK
    messages.error(request, 'ERROR!',fail_silently=True) #OK
    return render(request,"template+messages+ajax.html")

def viewJinja2Message(request):
    #Handle Mesages
    messages.warning(request, 'WARNING!',fail_silently=True) #OK
    messages.error(request, 'ERROR!',fail_silently=True) #OK
    return render(request,"template+messages.html")

#########################################
# COOKIES & SESSIONS
#########################################                                       
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
    response = HttpResponse()
    cookieValue = "Local current time :(%s)"  %(localtime)
    #set_cookie(response, key, value, expire=None)
    #response.set_cookie('user_id', user_id, max_age=30) 
    response.set_cookie('cookie_name', cookieValue)
    
    return response


"""
#response.set_cookie('read_count_%s' % content_type.id, value = read_count, expires = expires)
#hr = HttpResponse('ok')
#hr.set_cookie('user_id', user_id, max_age=30)

def set_cookie(response, key, value, expire=None):
    if expire is None:
        max_age = 365*24*60*60  #one year
    else:
        max_age = expire
    
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, 
        domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)
    
"""

#from personel.models import *

@login_required(login_url="login/")
def home2(request):
    return render(request,"home.html")

# Create your views here.
def home(request):
    #return render(request, 'personel/home.html', {'msg': 'Hello'})
    return HttpResponse('This Is Home')

# Create your views here.
def land(request):
    return render(request, 'personel/home.html', {'msg': 'Hello'})


class MyView(View):
    def get(self, request):
        # <view logic>
        return HttpResponse('result')


class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)



def detail(request, t_id):
    try:
        t = Teacher.objects.get(pk=t_id)
    except Teacher.DoesNotExist:
        raise Http404("Teacher does not exist")
    return render(request, 'teacher/detail.html', {'teacher': t})




#FORM-VIEW 
def post_form_upload(request):
    if request.method == 'GET':
        form = PostForm()
    else:
        # A POST request: Handle Form Upload
        form = PostForm(request.POST) # Bind data from request.POST into a PostForm
 
        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            content = form.cleaned_data['content']
            created_at = form.cleaned_data['created_at']
            #post = m.Post.objects.create(content=content, created_at=created_at)
            #return HttpResponseRedirect(reverse('post_detail', kwargs={'post_id': post.id}))
            return HttpResponseRedirect(reverse('myview',
                                                kwargs={'content': content, 'cleaned_data': form.cleaned_data, }))


    return render(request, 'post_form_upload.html', {
        'form': form,
    })



