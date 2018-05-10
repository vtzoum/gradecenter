#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import include, patterns, url
from django.contrib.staticfiles.views import serve as serve_static
from django.views.decorators.cache import never_cache

import views

urlpatterns = [
        
    #################################
    # disable caching
    #################################
    #url(r'^/static/(?P<path>.*)$', never_cache(serve_static)), 
    
    #################################
    # user profile
    #################################
    url(r'^(?P<pk>[0-9]+)/$', views.UserProfileDetail.as_view(), name='user_profile_detail'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.UserProfileUpdate.as_view(),name='user_profile_edit'),
    #url(r'^mousesmall/(?P<name>.*)/$', IDView.as_view(), name="rna_detailview"),

    #url(r'^(?P[0-9]+)/$', views.UserProfileDetail.as_view(), name='user_profile_detail'),
    #url(r'^(?P[0-9]+)/update/$', views.UserProfileUpdate.as_view(),name='user_profile_edit'),
    #url(r'^cookie/get/$', personel.views.viewGetCookie), 

]
