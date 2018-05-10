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

from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from django.template import RequestContext


#########################################
# CUSTOM 404 | 500 HANDLERS
#########################################
def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response



#########################################
# TEST VIEWS
#########################################
@login_required(login_url="login/")
def myHome(request):
    return render(request,"home.html")

# Create your views here.
@login_required(login_url="login/")
def myHome2(request):
    return render(request, 'personel/home.html', {'msg': 'Hello'})


