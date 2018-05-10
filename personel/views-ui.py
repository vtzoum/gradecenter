#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views.generic import View
from django.views.generic import CreateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from django.core.urlresolvers import reverse

from django import forms

from django.views.generic.edit import FormView

from django.views.decorators.csrf import csrf_exempt



def comboGridPage(request):
    msg = [1,2,3,4,5]    
    html = render(request, 'ui-jqwidgets/combo+grid.html', {'msg': msg, 'variable': 'B', })
    return HttpResponse(html)

def gridPage(request):
    msg = [1,2,3,4,5]    
    html = render(request, 'ui-jqwidgets/grid.html', {'msg': msg, 'variable': 'B', })
    return HttpResponse(html)

def gridPopupEditPage(request):
    msg = [1,2,3,4,5]    
    html = render(request, 'ui-jqwidgets/grid+popup+edit.html', {'msg': msg, 'variable': 'B', })
    return HttpResponse(html)

def listboxPage(request):
    msg = [1,2,3,4,5]    
    html = render(request, 'ui-jqwidgets/listbox.html', {'msg': msg, 'variable': 'B', })
    return HttpResponse(html)

def menuPage(request):
    msg = [1,2,3,4,5]
    html = render(request, 'ui-jqwidgets/menu.html', {'msg': msg, 'variable': 'B', })
    return HttpResponse(html)


class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)


def home(request):
    return HttpResponse('Home!')


