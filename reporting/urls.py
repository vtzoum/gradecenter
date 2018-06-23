"""ExportingFiles URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from personel.decorators import *

from .views import *
from .views_docx import *
from .views_pdf import *
from .views_xlsx import *

urlpatterns = [

    #SIMPLE
    #url(r'^home/$', home, name='home'),
    #url(r'^home/html/$', staff_or_403(homeHtml), name='homehtml'),
    url(r'^home/pdf/$', staff_or_403(homePdf), name='homepdf'),
    url(r'^home/xls/$', staff_or_403(homeXls), name='homexls'),

    #GENERAL
    url(r'^general/$', staff_or_403(TemplateView.as_view(template_name='reporting/general.html')), name='reportgeneral'),

    #Barcode+SECRETARIAT
    url(r'^accepting/$', staff_or_403(TemplateView.as_view(template_name='reporting/accepting.html')), name='reportaccepting'),
    url(r'^grading/$', staff_or_403(TemplateView.as_view(template_name='reporting/grading.html')), name='reportgrading'),
    url(r'^barcodes/$', staff_or_403(TemplateView.as_view(template_name='reporting/barcodes.html')), name='reportbarcodes'),
    url(r'^schools/$', staff_or_403(TemplateView.as_view(template_name='reporting/schools.html')), name='reportschools'),
    url(r'^graders/$', staff_or_403(TemplateView.as_view(template_name='reporting/graders.html')), name='reportgraders'),
    url(r'^work/$', staff_or_403(TemplateView.as_view(template_name='reporting/work.html')), name='reportwork'),
    url(r'^secretariat/$', staff_or_403(TemplateView.as_view(template_name='reporting/secretariat.html')), name='reportsecretariat'),
    #Closing reports
    url(r'^closing/$', staff_or_403(TemplateView.as_view(template_name='reporting/closing.html')), name='reportclosing'),

    ###########################################
    #DOCX
    ###########################################
    url(r'^doc/test/$', staff_or_403(docTest), name='docTest'),
    url(r'^doc/school/coverletter/$', staff_or_403(docSchoolCoverLetter), name='docschoolcoverletter'),

    ###########################################
    #XLS
    ###########################################
    #XLS ACCEPTANCE
    url(r'^xls/acceptance/sum/$', staff_or_403(xlsAcceptanceSum), name='xlsacceptancesum'),
    url(r'^xls/acceptance/$', staff_or_403(xlsAcceptance), name='xlsacceptance'),

    #XLS BOOKING
    url(r'^xls/booking/$', staff_or_403(xlsBooking), name='xlsbooking'),
    #url(r'^xls/booking/days/$', staff_or_403(xlsBookingDays), name='xlsbookingdays'),
    #url(r'^xls/booking/weekends/$', staff_or_403(xlsBookingWeekends), name='xlsbookingweekends'),
    url(r'^xls/booking/weekdays/count/$', staff_or_403(xlsBookingWeekdaysCount), name='xlsbookingweekdayscount'),
    url(r'^xls/booking/weekdays/details/$', staff_or_403(xlsBookingWeekdaysDetails), name='xlsbookingweekdaysdetails'),
    url(r'^xls/booking/weekends/count/$', staff_or_403(xlsBookingWeekendsCount), name='xlsbookingweekendscount'),
    url(r'^xls/booking/weekends/details/$', staff_or_403(xlsBookingWeekendsDetails), name='xlsbookingweekendsdetails'),
    url(r'^xls/booking/grader/$', staff_or_403(xlsBookingGrader), name='xlsbookinggrader'),

    #XLS FOLDER
    url(r'^xls/folder/$', staff_or_403(xlsFolder), name='xlsfolder'),
    url(r'^xls/folder/delays/$', staff_or_403(xlsFolderDelays), name='xlsfolderdelays'),
    url(r'^xls/folder/history/$', staff_or_403(xlsFolderHistory), name='xlsfolderhistory'),
    url(r'^xls/folder/now/$', staff_or_403(xlsFolderNow), name='xlsfoldernow'),
    url(r'^xls/folder/status0/$', staff_or_403(xlsFolderStatus0), name='xlsfolderstatus0'),
    url(r'^xls/folder/status1/$', staff_or_403(xlsFolderStatus1), name='xlsfolderstatus1'),
    url(r'^xls/folder/sum/$', staff_or_403(xlsFolderSum), name='xlsfoldersum'),

    # HTML
    url(r'^html/folder/now/$', htmlFolderNow, name='htmlfoldernow'),
    url(r'^html/folder/sum/$', htmlFolderSum, name='htmlfoldersum'),
    url(r'^html/grader/workv3/$', htmlGraderWorkv3, name='htmlgraderworkv3'),
    #url(r'^booking03/$', group_required_or_403('Grammateia', 'Filaxi', 'Apothiki')(TemplateView.as_view(template_name='ui-final.jinja/booking+v0.3.html'))),
    

    #CHARTS
    url(r'^chart/folder/sum$', chartFolderSum, name='chartfoldersum'),
    url(r'^chart/folder/sum/pie$', chartFolderSumPie, name='chartfoldersumpie'),
    url(r'^chart/folder/sum/stackcol$', chartFolderSumStackCol, name='chartfoldersumstackcol'),


    #XLS GRADER
    url(r'^xls/grader/$', staff_or_403(xlsGrader), name='xlsgrader'),
    url(r'^xls/grader/workv3/$', staff_or_403(xlsGraderWorkv3), name='xlsgraderworkv3'),
    url(r'^xls/grader/workv2/$', staff_or_403(xlsGraderWorkv2), name='xlsgraderworkv2'),
    url(r'^xls/grader/work/$', staff_or_403(xlsGraderWork), name='xlsgraderwork'),
    url(r'^xls/grader/work/day/$', staff_or_403(xlsGraderWorkDay), name='xlsgraderworkday'),

    #XLS TOTALS
    url(r'^xls/total/$', staff_or_403(xlsTotal), name='xlsgraderwork'),

    ###########################################
    #PDF
    ###########################################
    url(r'^pdf/barcode/$', staff_or_403(pdfBarcode), name='pdfbarcode'),
    url(r'^pdf/letter/$', staff_or_403(pdfLetter), name='pdfletter'),

    # SCHOOLS
    url(r'^pdf/school/labels/$', staff_or_403(pdfSchoolLabels), name='pdfschoollabels'),
    url(r'^pdf/school/coverletter/$', staff_or_403(pdfSchoolCoverLetter), name='pdfschoolcoverletter'),




    #COORDINATORS
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$', today_weather, name='today_weather'),
    #url(r'^weather/history/$', weather_history, name='weather_history'),
    #url(r'^weather/details/(?P<weather_id>\w+)', details, name='details'),
    #url(r'^towns/$', all_towns, name='towns'),

]



