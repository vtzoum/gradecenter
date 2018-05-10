#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.staticfiles.views import serve as serve_static
from django.views.decorators.cache import never_cache

from personel.views import *
#from session.views import *

from . import views

urlpatterns = patterns('',
    url(r'^/static/(?P<path>.*)$', never_cache(serve_static)), #disable caching
    #HOME
    #django jqxwidgets with ajax views with db records pages 


    #################################
    # user authen|author
    #################################
    #url(r'^login1/$', views.login, {'template_name': 'login.html'}), 
    #url(r'^logout1/$', views.logout, {'next_page': '/login'}),  
    
    #url(r'^admin/', include(admin.site.urls)),    
    url(r'^$', 'personel.views.home', name='home'),

    #url(r'^accounts/', include('django.contrib.auth.urls', namespace="auth")),
    #url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    #url('^accounts/', include('django.contrib.auth.urls')),

    #url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^logout/$', 'django.contrib.auth.views.logout'),
    #################################
    # sessions
    #################################

    url(r'^cookie/get/$', 'personel.views.viewGetCookie'), 
    url(r'^cookie/set/$', 'personel.views.viewSetCookie'),    
    
    #url(r'^/cookie/get/$', 'sessions.views.viewGetCookie'),    
    #url(r'^/cookie/set/$', 'sessions.views.viewSetCookie'),    

    #################################
    # ui > fitness
    #################################
    url(r'^ui/$', TemplateView.as_view(template_name='ui-final/ui.html')),    
    url(r'^ui/sb-admin/$', TemplateView.as_view(template_name='ui-final/ui+sb-admin.html')),    
    #################################
    # final > ui
    #################################
    #RELATIONSHIP(M:N)        
    url(r'^acceptance/$', TemplateView.as_view(template_name='ui-final/acceptance.html')),    
    url(r'^acceptance/crud/$', 'personel.views-er-rel-mn.jsonAcceptanceCrud'), #
    
    url(r'^assigngraderstolessons', TemplateView.as_view(template_name='ui-final/assign-graders-to-lessons.html')),
    
    #RELATIONSHIP(M:N)        
    url(r'^booking/$', TemplateView.as_view(template_name='ui-final/booking.html')),    
    url(r'^booking/crud/$', 'personel.views-er-rel-mn.jsonBookingCrud'), #
    
    url(r'^books/$', TemplateView.as_view(template_name='ui-final/books.html')),    

    #RELATIONSHIP(1:N)        
    #url(r'^folders/$', TemplateView.as_view(template_name='ui-final/folders.html')), 
    url(r'^folder/$', TemplateView.as_view(template_name='ui-final/folder.html')),    
    url(r'^folder/crud/$', 'personel.views-er-rel-1n.jsonFolderCrud'), #graders accessed by lessons 

    #RELATIONSHIP(M:N)        
    url(r'^grader/$', TemplateView.as_view(template_name='ui-final/grader.html')),
    #url(r'^grader/$', TemplateView.as_view(template_name='ui-final/grader.html')),
    #url(r'^grader/add/$', 'personel.views-ajax.formPostGraderAdd'),
    #url(r'^grader/lesson/$', TemplateView.as_view(template_name='ui-final/grader+lesson.html')),
    url(r'^grader/crud/$', 'personel.views-er-rel-mn.jsonGraderCrud'), #graders accessed by lessons 
        
    #ENTITY**KERNEL**
    url(r'^lesson/$', TemplateView.as_view(template_name='ui-final/lesson.html')),
    url(r'^lesson/crud/$', 'personel.views-crud.jsonLessonCrud'),
    url(r'^lesson/upload/$', TemplateView.as_view(template_name='ui-final/lesson+upload.html')),
    url(r'^lesson/upload/import/$', 'personel.views-fileupload.jsonFileCSVImportLesson'),

    #RELATIONSHIP(M:N)        
    url(r'^registry/$', TemplateView.as_view(template_name='ui-final/registry.html')),    

    url(r'^schooltograde/$', TemplateView.as_view(template_name='ui-final/schooltograde.html')),
    url(r'^schooltograde/crud/$', 'personel.views-crud.jsonSchoolToGradeCrud'),
    url(r'^schoolstograde/upload/$', TemplateView.as_view(template_name='ui-final/schoolstograde+upload.html')),    
    url(r'^schoolstograde/upload/import/$', 'personel.views-fileupload.jsonFileCSVImportSchoolToGrade'),
    
    url(r'^specialty/$', TemplateView.as_view(template_name='ui-final/specialty.html')),
    url(r'^specialty/crud/$', 'personel.views-crud.jsonSpecialtyCrud'),
    url(r'^specialty/upload/$', TemplateView.as_view(template_name='ui-final/specialty+upload.html')),
    url(r'^specialty/upload/import/$', 'personel.views-fileupload.jsonFileCSVImportSpecialty'),
    
    url(r'^teacher/$', TemplateView.as_view(template_name='ui-final/teacher.html')),
    url(r'^teacher/crud/$', 'personel.views-crud.jsonTeacherCrud'),
    url(r'^teacher/upload/$', TemplateView.as_view(template_name='ui-final/teacher+upload.html')),
    url(r'^teacher/upload/import/$', 'personel.views-fileupload.jsonFileCSVImportTeacher'),
    
    
        
    
    #################################
    # final > ajax
    #################################
    
    #url(r'^schooltograde/$', 'personel.views-ajax.ajaxSchoolToGrade'),
    #url(r'^schoolstograde/fileupload/csv/$', TemplateView.as_view(template_name='ui-final/schoolstograde+fileupload+csv.html')),
    
    #url(r'^specialty/$', TemplateView.as_view(template_name='ui-final/specialty.html')),
    #url(r'^specialty/fileupload/csv/$', TemplateView.as_view(template_name='ui-final/specialty+fileupload+csv.html')),
    
    #url(r'^teacher/$', TemplateView.as_view(template_name='ui-final/teacher.html')),
    #url(r'^teacher/fileupload/csv/$', TemplateView.as_view(template_name='ui-final/teacher+fileupload+csv.html')),


    #################################
    # final > json CRUD
    #################################
    url(r'^lesson/crud/$', 'personel.views-crud.jsonLessonCrud'),
    
    url(r'^schooltograde/crud/$', 'personel.views-crud.jsonSchoolToGradeCrud'),
    
    url(r'^teacher/crud/$', 'personel.views-crud.jsonTeacherCrud'),
    

    #################################
    #POST request + FORM + jqxWidgets
    #################################
    url(r'^formpost/$', TemplateView.as_view(template_name='ajax/form-post.html')),
    url(r'^ajaxformpost/$', 'personel.views-ajax.formPost'),

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
    url(r'^comboboxcheck/$', TemplateView.as_view(template_name='ui-jqwidgets/combobox+check.html')),
    url(r'^combogrid', TemplateView.as_view(template_name='ui-jqwidgets/combo+grid.html')),
    #datatble
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
    url(r'^grid/cell/command/menu/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+cell+command+menu.html')),
    url(r'^grid/cell/widget/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+cell+widget.html')),
    url(r'^grid/edit/popup/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+edit+popup.html')),
    url(r'^gridpopupeditdjango/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+popup+edit+django.html')),
    url(r'^grid/filter/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+filter.html')),    
    url(r'^grid/filter/row/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+filter+row.html')),    
    url(r'^grid/format/$', TemplateView.as_view(template_name='ui-jqwidgets/grid+format.html')),
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
    url(r'^tabs', TemplateView.as_view(template_name='ui-jqwidgets/tabs.html')),
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
    url(r'^ajax/add/$', 'personel.views-json.add_todo'),
    url(r'^ajax/more/$', 'personel.views-json.more_todo'),
    
    #AJAX
    url(r'^ajax_data/$', 'personel.views-ajax.ajax_data'),
    url(r'^ajax_page/$', 'personel.views-ajax.ajax_page'),
    
    url(r'^ajax_get/$', 'personel.views-ajax.ajax_get'),
    #url(r'^ajax_post/$', 'personel.views-ajax.ajax_post'),
    

    #################################
    #JSON
    #################################
    #//
    #JSON> DATA
    url(r'^jsonacceptance/$', 'personel.views-json.jsonAcceptance'),    
    url(r'^jsonbooking/$', 'personel.views-json.jsonBooking'),
    url(r'^jsondata/$', 'personel.views-json.jsonData'),
    url(r'^jsondatancb/$', 'personel.views-json.jsonDataNCB'),
    url(r'^jsondatanc/$', 'personel.views-json.jsonDataNC'),
    #url(r'^jsonfolder/', 'personel.views-json.jsonFolder'),
    url(r'^jsongrader/', 'personel.views-json.jsonGrader'),
    url(r'^jsongradermn/', 'personel.views-json.jsonGraderMN'),
    
    url(r'^jsonlesson/$', 'personel.views-json.jsonLesson'),
    url(r'^jsonlessonstatus/$', 'personel.views-json.jsonLessonStatus'),
    
    url(r'^jsonteacher/$', 'personel.views-json.jsonTeacher'),
    url(r'^jsonteachercrud/$', 'personel.views-json.jsonTeacherCrud'),
    #JSON > FILEUPLOADS
    url(r'^foo/$', 'personel.views-json.foo'),
    url(r'^jsonfileupload/$', 'personel.views-fileupload.jsonFileUpload'),
    url(r'^jsonfilecsvimportlesson/$', 'personel.views-fileupload.jsonFileCSVImportLesson'),
    url(r'^jsonfilecsvimportschooltograde/$', 'personel.views-fileupload.jsonFileCSVImportSchoolToGrade'),
    url(r'^jsonfilecsvimportteacher/$', 'personel.views-fileupload.jsonFileCSVImportTeacher'),
    #JSON PAGES
    url(r'^json/$', TemplateView.as_view(template_name='json/index.html')),
    url(r'^json/get/$', 'personel.views-json.json_get'),
    url(r'^json/post/$', 'personel.views-json.json_post'),
    url(r'^json/add/$', 'personel.views-json.json_post'),

    #SIMPLE
    url(r'^home/', 'personel.views-ajax.home'),


    #url(r'^$', 'personel.views.home', name='home'),
    url(r'^myview/$', MyView.as_view(), name='myview'),
    #form
    #url(r'^post/form_upload.html$', 'personel.views.post_form_upload', name='post_form_upload'),

    #url(r'^$', personel.views.ListContactView.as_view(),name='contacts-list',),

    #url(r'^new$', personel.views.CreateContactView.as_view(), name='contacts-new',),

    #url(r'^edit/(?P<pk>\d+)/$', personel.views.UpdateContactView.as_view(), name='contacts-edit',),

    #url(r'^delete/(?P<pk>\d+)/$', personel.views.DeleteContactView.as_view(), name='contacts-delete',),

    #url(r'^(?P<pk>\d+)/$', personel.views.ContactView.as_view(), name='contacts-view',),
    #2. 1:N
    #url(r'^edit/(?P<pk>\d+)/addresses$', personel.views.EditContactAddressView.as_view(), name='contacts-edit-addresses',),

    #url(r'^teachers/$', 'personel.views.home', name='teachers'),
    #url(r'^teacher/add/$', 'personel.views.teacher', name='teachers'),
    #url(r'^teacher/?P<id>\d+/$', 'personel.views.MyView.as_view()', name='myview'),
    #url(r'^myview/$', 'personel.views.MyView.as_view()', name='myview'),

    # url(r'^blog/', include('blog.urls')),
    #url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
