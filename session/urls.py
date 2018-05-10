#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

import personel.views 
from personel.views import MyView, GreetingView

from django.conf.urls.static import static

from django.views.generic import TemplateView

from django.contrib.staticfiles.views import serve as serve_static
from django.views.decorators.cache import never_cache

urlpatterns = patterns('',
    url(r'^/static/(?P<path>.*)$', never_cache(serve_static)), #disable caching
    #################################
    # ui > fitness
    #################################
    url(r'^/cookie/get/$', 'sessions.views.viewGetCookie'),    
    url(r'^/cookie/set/$', 'sessions.views.viewSetCookie'),    
    #url(r'^ui/$', TemplateView.as_view(template_name='ui-final/ui.html')),    
    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

