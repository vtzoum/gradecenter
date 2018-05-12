#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import include, patterns, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.views import serve as serve_static
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView

#from session.views import *
import views
import personel 
from personel import views, views_ajax, views_json, viewsErCrud, viewsErRelMn, viewsErRel1N, viewsFileUpload

from registration.backends.simple.views import RegistrationView

from personel.decorators import *
from personel.helpScripts import *

from django.shortcuts import render_to_response
from django.template import RequestContext


def get_success_url(self,request, user):
    return '/teacher/'

# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    #def get_success_url(self,request, user):
    def get_success_url(self,user):
        return '/teacher/'


#################################
#CUSTOM ERROR PAGES
#(set DEBUG=False to activate)
#################################
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

# HTTP Error 401
def error400(request):
    response = render_to_response('400.html', context_instance=RequestContext(request))
    response.status_code = 400
    return response

def error401(request):
    response = render_to_response('401.html', context_instance=RequestContext(request))
    response.status_code = 401
    return response

def error403(request):
    response = render_to_response('403.html', context_instance=RequestContext(request))
    response.status_code = 403
    return response

# HTTP Error 400
def error404(request):
    response = render_to_response('404.html', context_instance=RequestContext(request))
    response.status_code = 404
    return response

def error500(request):
    response = render_to_response('500.html', context_instance=RequestContext(request))
    response.status_code = 500
    return response


class HttpResponseNotAuthorized(HttpResponse):
    status_code = 401

    def __init__(self, redirect_to):
        HttpResponse.__init__(self)
        self['WWW-Authenticate'] = 'Basic realm="%s"' % Site.objects.get_current().name


from django.conf.urls import handler400, handler403, handler404, handler500 

#handler400 = 'my_app.views.bad_request'
#handler403 = 'my_app.views.permission_denied'
#handler404 = 'my_app.views.page_not_found'
#handler500 = 'my_app.views.server_error'
handler400 = error400
handler401 = error401
handler403 = error403
handler404 = error404
handler500 = error500


urlpatterns = [    
    
    #################################
    # disable caching
    #################################
    url(r'^/static/(?P<path>.*)$', never_cache(serve_static)), #disable caching

    
    #################################
    # user profile
    #################################
    url(r'^user_profile/', include('user_profile.urls')),

    #################################
    # INCLUDE > reporting
    #################################
    url(r'^reporting/', include('reporting.urls')),

    #################################
    #DBTableData
    #################################
    url(r'^dde/data/$', personel.views_json.jsonDBTableDataDDE), 
    url(r'^specialty/data/$', personel.views_json.jsonDBTableDataSpecialty),

    #################################
    #ROOTHome
    #################################
    url(r'^$', TemplateView.as_view(template_name='ui-final.jinja/home.html'), name='base'),    
    url(r'^home/$', TemplateView.as_view(template_name='ui-final.jinja/home.html'), name='home'),
    url(r'^land/$', TemplateView.as_view(template_name='ui-final.jinja/home-land.html'), name='homeland'),

    #################################
    # REDUX Accounts 
    #################################
    url(r'^accounts/', include('registration.backends.default.urls')),
    #url(r'^accounts/', include('registration.backends.simple.urls')),    
    #url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('django.contrib.auth.urls', namespace="auth")),

    #################################
    # USER AUTH
    #################################
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    #url(r'^login/$', auth_views.login, {'template_name': 'core/login.html'}, name='login'),
    #url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),    
    #url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    #url(r'^register/$', auth_views.register, name='register'),            
    #url(r'^login1/$', views.login, {'template_name': 'login.html'}),     
    #url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^logout/$', 'django.contrib.auth.views.logout'),
    #url(r'^accounts/register/$', get_success_url, name='registration_register'),
    url(r'login/success/$', views_json.loginSuccess, name='login_success'),     #UNTESTED
    
    #################################
    # DJANGO ADMIN 
    #################################
    url(r'^admin/', include(admin.site.urls)),    
    
    #################################
    # final > ui
    #################################
    #url(r'^gcparam/$', TemplateView.as_view(template_name='ui-final.jinja/gcparam.html')),    
    url(r'^gcparam/$', personel.views.gcparam),

    
    url(r'^about/$', TemplateView.as_view(template_name='ui-final.jinja/about.html')),    
    #RELATIONSHIP(M:N)        
    url(r'^acceptance/$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/acceptance.html'))),    
    url(r'^acceptance/crud/$', personel.viewsErRelMn.jsonAcceptanceCrud), 
    
    url(r'^assigngraderstolessons', TemplateView.as_view(template_name='ui-final.jinja/assign-graders-to-lessons.html')),
    
    #RELATIONSHIP(M:N)        
    #url(r'^schooltograde/$', staff_or_403(personel.views.pageSchoolToGrade)),
    url(r'^booking/manage/$', group_required_or_403('Admin')(TemplateView.as_view(template_name='ui-final.jinja/booking+manage.html'))),
    url(r'^booking/$', group_required_or_403('Grammateia', 'Filaxi', 'Apothiki')(TemplateView.as_view(template_name='ui-final.jinja/booking.html'))),
    url(r'^booking01/$', group_required_or_403('Grammateia', 'Filaxi', 'Apothiki')(TemplateView.as_view(template_name='ui-final.jinja/booking+v0.1.html'))),
    url(r'^booking02/$', group_required_or_403('Grammateia', 'Filaxi', 'Apothiki')(TemplateView.as_view(template_name='ui-final.jinja/booking+v0.2.html'))),
    url(r'^booking03/$', group_required_or_403('Grammateia', 'Filaxi', 'Apothiki')(TemplateView.as_view(template_name='ui-final.jinja/booking+v0.3.html'))),
    url(r'^booking04/$', group_required_or_403('Grammateia', 'Filaxi', 'Apothiki')(TemplateView.as_view(template_name='ui-final.jinja/booking+v0.4.html'))),
    url(r'^booking/crud/$', personel.viewsErRelMn.jsonBookingCrud),
    url(r'^booking/post/$', personel.viewsErRelMn.jsonBookingPost),
    
    url(r'^books/$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/books.html'))),

    #RELATIONSHIP(1:N)        
    #url(r'^folders/$', TemplateView.as_view(template_name='ui-final.jinja.jinja/folders.html')), 
    url(r'^folder/$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/folder.html'))),
    url(r'^folder/crud/$', personel.viewsErRel1N.jsonFolderCrud), #graders accessed by lessons 

    #RELATIONSHIP(M:N)        
    url(r'^grader/$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/grader.html'))),
    url(r'^grader/crud/$', personel.viewsErRelMn.jsonGraderCrud), #graders accessed by lessons 
    #url(r'^grader/add/$', personel.views_ajax.formPostGraderAdd'),
    #url(r'^grader/lesson/$', TemplateView.as_view(template_name='ui-final.jinja/grader+lesson.html')),
        
    #ENTITY**KERNEL**
    url(r'^lesson/$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/lesson.html'))),
    url(r'^lesson/crud/$', personel.viewsErCrud.jsonLessonCrud),
    url(r'^lesson/manage$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/lesson+manage.html'))),
    url(r'^lesson/status/$', personel.viewsErCrud.jsonLessonStatus),
    url(r'^lesson/upload/$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/lesson+upload.html'))),
    url(r'^lesson/upload/import/$', staff_or_403(personel.viewsFileUpload.jsonFileCSVImportLesson)),

    #RELATIONSHIP(M:N)        
    url(r'^registry/$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/registry.html'))),

    #ENTITY
    #@login_required(login_url="login/")
    #@group_required('Grammateia')
    #url(r'^schooltograde/$', personel.views.pageSchoolToGrade),
    
    #url(r'^schooltograde/$', login_required(staff_or_401(personel.views.pageSchoolToGrade))),
    
    #url(r'^schooltograde/$', staff_or_403(personel.views.pageSchoolToGrade)),   #OK
    url(r'^schooltograde/$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/schooltograde.html'))),   # NOT OK
    
    #url(r'^schooltograde/$', group_required_or_401('Grammateia')(personel.views.pageSchoolToGrade)),
    
    #url(r'^schooltograde/$', TemplateView.as_view(template_name='ui-final.jinja/schooltograde.html')),
    url(r'^schooltograde/crud/$', personel.viewsErCrud.jsonSchoolToGradeCrud),
    url(r'^schoolstograde/upload/$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/schoolstograde+upload.html'))),
    url(r'^schoolstograde/upload/import/$', staff_or_403(personel.viewsFileUpload.jsonFileCSVImportSchoolToGrade)),
    
    #ENTITY
    url(r'^specialty/$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/specialty.html'))),
    url(r'^specialty/crud/$', staff_or_403(personel.viewsErCrud.jsonSpecialtyCrud)),
    url(r'^specialty/upload/$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/specialty+upload.html'))),
    url(r'^specialty/upload/import/$', staff_or_403(personel.viewsFileUpload.jsonFileCSVImportSpecialty)),
    
    #ENTITY
    url(r'^teacher/$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/teacher.html'))),
    url(r'^teacher/crud/$', personel.viewsErCrud.jsonTeacherCrud),
    url(r'^teacher/upload/$', staff_or_403(TemplateView.as_view(template_name='ui-final.jinja/teacher+upload.html'))),
    url(r'^teacher/upload/import/$', staff_or_403(personel.viewsFileUpload.jsonFileCSVImportTeacher)),
    
   
        
    #################################
    # cookies-sessions
    #################################
    url(r'^cookie/get/$', personel.views.viewGetCookie), 
    url(r'^cookie/set/$', personel.views.viewSetCookie),    
    #url(r'^/cookie/get/$', 'sessions.views.viewGetCookie'),    
    #url(r'^/cookie/set/$', 'sessions.views.viewSetCookie'),    
    
    #################################
    # Templates
    #################################
    url(r'^template/tags/$', TemplateView.as_view(template_name='template+tags.html')),    
    url(r'^template/cookies/$', TemplateView.as_view(template_name='template+cookies.html')),    


    #################################
    # Templates-JINJA
    #################################
    #url(r'^template-jinja/messages/$', TemplateView.as_view(template_name='template+messages.html')),
    url(r'^template-jinja/messages/$', personel.views.viewJinja2Message), 
    url(r'^template-jinja/messages-ajax/$', personel.views.viewJinja2MessageAjax), 

    #################################
    # ui > fitness
    #################################
    url(r'^ui/$', TemplateView.as_view(template_name='ui-final.jinja/ui.html')),    
    url(r'^ui/flat-admin/$', TemplateView.as_view(template_name='ui/ui+flat-admin.html')),    
    url(r'^ui/sb-admin/$', TemplateView.as_view(template_name='ui-final.jinja/ui+sb-admin.html')),    
    
    #################################
    # final > ajax
    #################################
    
    #url(r'^schooltograde/$', personel.views_ajax.ajaxSchoolToGrade'),
    #url(r'^schoolstograde/fileupload/csv/$', TemplateView.as_view(template_name='ui-final.jinja/schoolstograde+fileupload+csv.html')),
    
    #url(r'^specialty/$', TemplateView.as_view(template_name='ui-final.jinja/specialty.html')),
    #url(r'^specialty/fileupload/csv/$', TemplateView.as_view(template_name='ui-final.jinja/specialty+fileupload+csv.html')),
    
    #url(r'^teacher/$', TemplateView.as_view(template_name='ui-final.jinja/teacher.html')),
    #url(r'^teacher/fileupload/csv/$', TemplateView.as_view(template_name='ui-final.jinja/teacher+fileupload+csv.html')),



    #################################
    #POST request + FORM + jqxWidgets
    #################################
    url(r'^formpost/$', TemplateView.as_view(template_name='ajax/form-post.html')),
    url(r'^ajaxformpost/$', personel.views_ajax.formPost),

    #################################
    # plugin > JS-Isotope 
    #################################
    url(r'^isotope/search/$', TemplateView.as_view(template_name='ui-plugins-isotope/filtering+searchfield.html')),

    #################################
    #jqxWidgets with ajax views pages 
    #################################
    # Buttons
    url(r'^buttons', TemplateView.as_view(template_name='ui-jqwidgets/buttons.html')),
    # Combobox
    url(r'^combobox/$', TemplateView.as_view(template_name='ui-jqwidgets/combobox.html')),
    url(r'^combobox/check/$', TemplateView.as_view(template_name='ui-jqwidgets/combobox+check.html')),
    url(r'^combobox/check/all/$', TemplateView.as_view(template_name='ui-jqwidgets/combobox+check+all-none.html')),
    url(r'^combogrid', TemplateView.as_view(template_name='ui-jqwidgets/combo+grid.html')),
    #dataadapter
    url(r'^dataadapter/$', TemplateView.as_view(template_name='ui-jqwidgets/dataadapter.html')),
    url(r'^dataadapter/aggregate/$', TemplateView.as_view(template_name='ui-jqwidgets/dataadapter+aggregate.html')),
    url(r'^dataadapter/grouprecord/$', TemplateView.as_view(template_name='ui-jqwidgets/dataadapter+grouprecord.html')),
    #datatable
    url(r'^datatable/column/command/$', TemplateView.as_view(template_name='ui-jqwidgets/datatable+column+command.html')),
    url(r'^datatable/row/format/$', TemplateView.as_view(template_name='ui-jqwidgets/datatable+row+format.html')),
    #datetime
    url(r'^datetime/datetime/$', TemplateView.as_view(template_name='ui-jqwidgets/datetime+datetime.html')),
    #draggable
    url(r'^draggable/$', TemplateView.as_view(template_name='ui-jqwidgets/draggable.html')),    
    url(r'^draggabletarget/$', TemplateView.as_view(template_name='ui-jqwidgets/draggable+target.html')),    
    url(r'^draggabletargetform/$', TemplateView.as_view(template_name='ui-jqwidgets/draggable+target+form.html')),        
    #grid 
    url(r'^dropdownlist/$', TemplateView.as_view(template_name='ui-jqwidgets/dropdownlist.html')),
    url(r'^dropdownlistsearch/$', TemplateView.as_view(template_name='ui-jqwidgets/dropdownlist+search.html')),
    #grid 
    url(r'^grid/$', TemplateView.as_view(template_name='ui-jqwidgets/grid.html')),
    url(r'^grid/aggregates/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+aggregates.html')),
    url(r'^grid/aggregates/column/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+aggregates+column.html')),
    url(r'^grid/aggregates/custom/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+aggregates+custom.html')),
    url(r'^grid/aggregates/renderer/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+aggregates+render.html')),
    url(r'^grid/crud/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+crud.html')),
    url(r'^grid/crud/e/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+crud+e.html')),
    url(r'^grid/crud/inline/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+crud+inline.html')),
    url(r'^grid/cell/command/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+cell+command.html')),
    url(r'^grid/cell/commandv1/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+cell+command-v1.html')),
    url(r'^grid/cell/commandv2/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+cell+command-v2.html')),
    url(r'^grid/cell/commandv3/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+cell+command-v3.html')),
    url(r'^grid/cell/command/menu/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+cell+command+menu.html')),
    url(r'^grid/cell/widget/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+cell+widget.html')),
    url(r'^grid/dataadapter$', TemplateView.as_view(template_name='ui-jqwidgets/grid+dataadapter.html')),
    url(r'^grid/edit/popup/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+edit+popup.html')),
    url(r'^gridpopupeditdjango/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+popup+edit+django.html')),
    url(r'^grid/filter/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+filter.html')),    
    url(r'^grid/filter/row/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+filter+row.html')),    
    url(r'^grid/format/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+format.html')),
    url(r'^grid/keyboard/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+keyboard.html')),
    url(r'^grid/msg/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+msg.html')),
    url(r'^gridgraders/$', TemplateView.as_view(template_name='ui-jqwidgets/grid-graders-mn.html')),
    url(r'^grid/row/disable/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+row+disable.html')),
    url(r'^grid/statusbar/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+statusbar.html')),
    url(r'^grid/toolbar/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+toolbar.html')),
    
    #dashboard
    url(r'^dashboard/$', TemplateView.as_view(template_name='ui-jqwidgets/dashboard.html')),
    url(r'^dashboardexperiment/$', TemplateView.as_view(template_name='ui-jqwidgets/dashboard-experiment.html')),    
    #listox
    url(r'^listbox/$', TemplateView.as_view(template_name='ui-jqwidgets/listbox.html')),
    url(r'^listboxdraggable/$', TemplateView.as_view(template_name='ui-jqwidgets/listbox+draggable.html')),    
    #menu
    url(r'^menu/$', TemplateView.as_view(template_name='ui-jqwidgets/menu.html')),    
    #progressbar
    url(r'^progressbar/', TemplateView.as_view(template_name='ui-jqwidgets/progressbar.html')),
    url(r'^progressbarranges/', TemplateView.as_view(template_name='ui-jqwidgets/progressbar+ranges.html')),
    #slider
    url(r'^slider/$', TemplateView.as_view(template_name='ui-jqwidgets/slider.html')),    
    #sortable
    url(r'^sortable/$', TemplateView.as_view(template_name='ui-jqwidgets/sortable.html')),    
    url(r'^sortablesearch/$', TemplateView.as_view(template_name='ui-jqwidgets/sortable+search.html')),    
    url(r'^sortableselectable/$', TemplateView.as_view(template_name='ui-jqwidgets/sortable+selectable.html')),        
    #Tabs
    url(r'^tabs/$', TemplateView.as_view(template_name='ui-jqwidgets/tabs.html')),
    url(r'^tabs2/$', TemplateView.as_view(template_name='ui-jqwidgets/tabs2.html')),
    #validator
    url(r'^validator/$', TemplateView.as_view(template_name='ui-jqwidgets/validator.html')),    
    #window
    url(r'^window/$', TemplateView.as_view(template_name='ui-jqwidgets/window.html')),    
    url(r'^windowextra/$', TemplateView.as_view(template_name='ui-jqwidgets/window+extra.html')),    
    #################################
    #jqxWidgets > FileUploads + CSV + DBimport 
    #################################
    #fileuploads
    url(r'^fileupload/$', TemplateView.as_view(template_name='ui-jqwidgets/file-upload.html')),
    url(r'^fileupload/csv/lesson/$', TemplateView.as_view(template_name='ui-jqwidgets/fileupload+csv+lesson.html')),
    url(r'^fileupload/csv/teacher/$', TemplateView.as_view(template_name='ui-jqwidgets/fileupload+csv+teacher.html')),
    
    #################################
    #jqxWidgets > CHARTS
    #################################
    url(r'^chart/bar/$', TemplateView.as_view(template_name='ui-jqwidgets-charts/bar.html')),
    url(r'^chart/bargauge/$', TemplateView.as_view(template_name='ui-jqwidgets-charts/bargauge.html')),
    
    url(r'^chart/column/$', TemplateView.as_view(template_name='ui-jqwidgets-charts/column.html')),
    url(r'^chart/column/local/$', TemplateView.as_view(template_name='ui-jqwidgets-charts/column+local.html')),
    
    url(r'^chart/pie/$', TemplateView.as_view(template_name='ui-jqwidgets-charts/pie.html')),

    #################################
    # basic-ui
    #################################
    url(r'^divselectable/$', TemplateView.as_view(template_name='ui-basic/div+selectable.html')),    
    url(r'^ui-basic/form/$', TemplateView.as_view(template_name='ui-basic/form.html')),    
    url(r'^ui-basic/form/bootstrap/$', TemplateView.as_view(template_name='ui-basic/form+bootstrap.html')),    


    #################################
    #AJAX
    #################################
    #url(r'', TemplateView.as_view(template_name='index.html')),
    url(r'^ajax/add/$', personel.views_json.add_todo),
    url(r'^ajax/more/$', personel.views_json.more_todo),
    
    #AJAX
    url(r'^ajax_data/$', personel.views_ajax.ajax_data),
    url(r'^ajax_page/$', personel.views_ajax.ajax_page),
    
    url(r'^ajax_get/$', personel.views_ajax.ajax_get),
    #url(r'^ajax_post/$', personel.views_ajax.ajax_post'),
    

    #################################
    #JSON
    #################################
    #//
    url(r'^jsongriddataadapter/$', personel.views_json.jsonGridDataadapter),    
    #JSON> DATA
    url(r'^jsonacceptance/$', personel.views_json.jsonAcceptance),    
    #url(r'^jsonbooking/$', personel.views_json.jsonBooking),
    url(r'^jsondata/$', personel.views_json.jsonData),
    url(r'^jsondatancb/$', personel.views_json.jsonDataNCB),
    url(r'^jsondatanc/$', personel.views_json.jsonDataNC),
    #url(r'^jsonfolder/', personel.views_json.jsonFolder),
    url(r'^jsongrader/', personel.views_json.jsonGrader),
    url(r'^jsongradermn/', personel.views_json.jsonGraderMNV0),
    
    url(r'^jsonlesson/$', personel.views_json.jsonLesson),
    url(r'^jsonlessonstatus/$', personel.views_json.jsonLessonStatus),
    
    url(r'^jsonteacher/$', personel.views_json.jsonTeacher),
    #url(r'^jsonteachercrud/$', personel.views_json.jsonTeacherCrud),
    #JSON > FILEUPLOADS
    #url(r'^foo/$', personel.views_json.foo),
    url(r'^jsonfileupload/$', personel.viewsFileUpload.jsonFileUpload),
    url(r'^jsonfilecsvimportlesson/$', personel.viewsFileUpload.jsonFileCSVImportLesson),
    url(r'^jsonfilecsvimportschooltograde/$', personel.viewsFileUpload.jsonFileCSVImportSchoolToGrade),
    url(r'^jsonfilecsvimportteacher/$', personel.viewsFileUpload.jsonFileCSVImportTeacher),
    #JSON PAGES
    url(r'^json/$', TemplateView.as_view(template_name='json/index.html')),
    url(r'^json/get/$', personel.views_json.json_get),
    url(r'^json/post/$', personel.views_json.json_post),
    url(r'^json/add/$', personel.views_json.json_post),

    #SIMPLE
    #url(r'^home/', personel.views_ajax.home),


    #url(r'^$', personel.views.home', name='home'),
    #url(r'^myview/$', MyView.as_view(), name='myview'),
    #form
    #url(r'^post/form_upload.html$', personel.views.post_form_upload', name='post_form_upload'),

    #url(r'^$', personel.views.ListContactView.as_view(),name='contacts-list',),

    #url(r'^new$', personel.views.CreateContactView.as_view(), name='contacts-new',),

    #url(r'^edit/(?P<pk>\d+)/$', personel.views.UpdateContactView.as_view(), name='contacts-edit',),

    #url(r'^delete/(?P<pk>\d+)/$', personel.views.DeleteContactView.as_view(), name='contacts-delete',),

    #url(r'^(?P<pk>\d+)/$', personel.views.ContactView.as_view(), name='contacts-view',),
    #2. 1:N
    #url(r'^edit/(?P<pk>\d+)/addresses$', personel.views.EditContactAddressView.as_view(), name='contacts-edit-addresses',),

    #url(r'^teachers/$', personel.views.home', name='teachers'),
    #url(r'^teacher/add/$', personel.views.teacher', name='teachers'),
    #url(r'^teacher/?P<id>\d+/$', personel.views.MyView.as_view()', name='myview'),
    #url(r'^myview/$', personel.views.MyView.as_view()', name='myview'),

    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
] 
#] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
