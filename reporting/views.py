#!/usr/bin/python
# -*- coding: utf-8 -*-

from io import BytesIO
import datetime
from datetime import date, timedelta
import itertools, json
import time

from .excel_utils import WriteToExcel
from .pdf_utils import PdfPrint


from django import forms
from django.conf import settings
#from .settings import STATIC_ROOT
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.db.models import Avg, Count, Max, Min, Sum
from django.db.models import IntegerField, DurationField 
from django.db.models import ExpressionWrapper, Func, F
#from django.db.models.functions import Length, Upper


from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View


import StringIO
import xlsxwriter

from .docx_letters import *
from .excel_utils import *
from .pdf_utils import *

from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.linecharts import SampleHorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table,\
    TableStyle


from reportlab.lib.units import inch, cm, mm
from reportlab.lib.pagesizes import A4, letter
#from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, PageTemplate
from reportlab.platypus import Paragraph, PageBreak, Preformatted, Spacer
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode import code39, code128, code93, eanbc, qr, usps
from reportlab.graphics.barcode import getCodes, getCodeNames, createBarcodeDrawing


from .utils import get_temperatures, get_wind_speed, get_str_days,\
    get_random_colors, precip_prob_sum, get_percentage
legendcolors = get_random_colors(10)

from personel.models import *
from personel.models import Folder
from personel.helpScripts import countDays0

from django.db.models import ExpressionWrapper, Func, F
from django.db.models import IntegerField
#from django.settings import CONST_MAXACTIONDURATION

from pdf_letters import doPDFSchoolCoverLetter
from pdf_labels import doPDFSchoolLabels

#print settings.STATIC_ROOT
#pdfmetrics.registerFont(TTFont('FreeSans', settings.STATIC_ROOT + 'reporting/fonts/FreeSans.ttf'))
#pdfmetrics.registerFont(TTFont('FreeSansBold', settings.STATIC_ROOT + 'reporting/fonts/FreeSansBold.ttf'))

pdfmetrics.registerFont(TTFont('FreeSans', settings.STATIC_ROOT + '/static/reporting/fonts/FreeSans.ttf'))
pdfmetrics.registerFont(TTFont('FreeSansBold', settings.STATIC_ROOT + '/static/reporting/fonts/FreeSansBold.ttf'))

#VTZOUM HACK
#from django.templatetags.static import static
#pdfmetrics.registerFont(TTFont('FreeSans', static('fonts/FreeSans.ttf')))
#pdfmetrics.registerFont(TTFont('FreeSans', static('fonts/FreeSansBold.ttf')))


#########################################
# HTML Views
#########################################
def homeSecretariat(request):
    return render(request,"templates/home.html")

def homeHtml(request):
    return render(request,"home.html")

# Create your views here.
def home(request):
    #return render(request, 'personel/home.html', {'msg': 'Hello'})
    return HttpResponse('This Is Home')


#########################################
# DOCX VIEWS
#########################################
#url(r'^doc/test/$', staff_or_403(docTest), name='docTest'),
def docTest(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
    else:
        lesson = None
    
    #Data
    #data = AcceptanceJoinTablesX2(LessonID).order_by('LessonID__name','SchoolToGradeID__name')
    data = None
    #print data    


    """
    # Prepare document for download        
    # -----------------------------
    f = StringIO()
    document.save(f)
    length = f.tell()
    f.seek(0)
    response = HttpResponse(
        f.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=' + docx_title
    response['Content-Length'] = length
    return response
    """


    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename=docTest.docx'
    docx_data = doDocxTest(data, lesson)
    response.write(docx_data)
    return response



#############################################
# ΔΙΑΒΙΒΑΣΤΙΚΑ ΣΧΟΛΕΙΩΝ για ΑΠΟΣΤΟΛΗ
#############################################
def docSchoolCoverLetter(request):
    
    SchoolToGradeId = request.GET.get('SchoolToGradeID', None)
    print SchoolToGradeId
    
    if SchoolToGradeId: 
        #theSchoolToGrade = SchoolToGrade.objects.get(id=SchoolToGradeId)    
        data = SchoolToGrade.objects.filter(id=SchoolToGradeId)
        #data = data.filter(LessonID=LessonID)
    else:
        data = SchoolToGrade.objects.all()
 
    data = data.order_by('name')
    #print data
    
    #PDF part 
    #Buffer
    #buffer = BytesIO()
    #pdf = doPDFSchoolCoverLetter(buffer, data, LetterCode=1)

    #DOC part 
    docx_data = doDocSchoolCoverLetter(data)

    #Response part
    #filename = 'Letters' + today.strftime('%Y-%m-%d')    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    today = date.today()
    filename = 'SchoolCoverLetters'
    response['Content-Disposition'] = 'attachement; filename={0}.docx'.format(filename)
    
    response.write(docx_data)
    return response




#########################################
# PDF Views
#########################################
def homePdf(request):
    
    response = HttpResponse(content_type='application/pdf')
    today = date.today()
    filename = 'pdf_demo' + today.strftime('%Y-%m-%d')
    response['Content-Disposition'] =\
        'attachement; filename={0}.pdf'.format(filename)
    buffer = BytesIO()

    #report = PdfPrint(buffer, 'A4')
    
    #weather_period = Weather.objects.all()    
    #pdf = report.report(weather_period, 'Weather statistics data')

    data = Folder.objects.all()
    print data    
    pdf = report.report(data, 'Data')
    response.write(pdf)
    return response


#########################################
#PDF LABELS for SCHOOL 
#########################################
    # SCHOOLS
#url(r'^/reporting/pdf/school/labels/$', staff_or_403(pdfSchoolLabels), name='pdfschoollabels'),
#url(r'^/reporting/pdf/school/coverletter/$', staff_or_403(pdfSchoolCoverLetter), name='pdfschoolcoverletter'),
def pdfSchoolLabels(request):
    
    SchoolToGradeId = request.GET.get('SchoolToGradeID', None)
    print SchoolToGradeId
    
    if SchoolToGradeId: 
        #theSchoolToGrade = SchoolToGrade.objects.get(id=SchoolToGradeId)    
        data = SchoolToGrade.objects.filter(id=SchoolToGradeId)
        #data = data.filter(LessonID=LessonID)
    else:
        data = SchoolToGrade.objects.all()
 
    data = data.order_by('name')
    #print data
    
    #PDF part 
    #Buffer
    buffer = BytesIO()
    pdf = doPDFSchoolLabels(buffer, data)

    #Response part
    response = HttpResponse(content_type='application/pdf')
    today = date.today()
    #filename = 'Letters' + today.strftime('%Y-%m-%d')
    filename = 'SchoolLabels'
    response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format(filename)
    
    response.write(pdf)
    return response


#########################################
#PDF LETTERS for SCHOOL 
#########################################
def pdfSchoolCoverLetter(request):
    
    SchoolToGradeId = request.GET.get('SchoolToGradeID', None)
    print SchoolToGradeId
    
    if SchoolToGradeId: 
        #theSchoolToGrade = SchoolToGrade.objects.get(id=SchoolToGradeId)    
        data = SchoolToGrade.objects.filter(id=SchoolToGradeId)
        #data = data.filter(LessonID=LessonID)
    else:
        data = SchoolToGrade.objects.all()
 
    data = data.order_by('name')
    #print data
    
    #PDF part 
    #Buffer
    buffer = BytesIO()
    pdf = doPDFSchoolCoverLetter(buffer, data, LetterCode=1)

    #Response part
    response = HttpResponse(content_type='application/pdf')
    today = date.today()
    #filename = 'Letters' + today.strftime('%Y-%m-%d')
    filename = 'SchoolCoverLetters'
    response['Content-Disposition'] = 'attachement; filename={0}.pdf'.format(filename)
    
    response.write(pdf)
    return response

#########################################
# PDF Barcode
#########################################
def pdfBarcode(request):

    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    codeType = request.GET.get('codeType', None)
    fromNo = request.GET.get('fromNo', None)
    toNo = request.GET.get('toNo', None)
    
    print LessonID, codeType, fromNo, toNo 
    
    if (LessonID==None):
        #return render(request, "resp-nodata.html")
        html = "<html><body><h1>ΔΕΝ ΕΠιλέξατε Μάθημα!</h1></body></html>"
        return HttpResponse(html)        

    #Data
    #data = Folder.objects
    #data = Folder.objects.filter(LessonID=LessonID).all()

    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)    
        data = Folder.objects.filter(LessonID=LessonID)
    
    if codeType:
        data = data.filter(codeType=codeType)
    
    if fromNo:
        data = data.filter(no__gte = int(fromNo))
    
    if toNo:
        data = data.filter(no__lte= int(toNo))

    data = data.values().order_by('codeType', 'no')
    #data = data.values('id', 'no', 'codeBarcode').order_by('codeType', 'no')
    #data = Folder.objects.filter(LessonID=LessonID, codeType=codeType).values('id', 'no', 'codeBarcode').order_by('codeType', 'no')
    
    
    if len(data)==0:
        return render(request, "resp-nodata.html", {'msg':u'ΔΕΝ ΥΠΑΡΧΟΥΝ ΔΙΑΘΕΣΙΜOI ΦΑΚΕΛΟΙ!'})
        #html = "<html><body><h1>ΔΕΝ ΥΠΑΡΧΟΥΝ ΔΙΑΘΕΣΙΜΟΙ ΦΑΚΕΛΟΙ!</h1></body></html>"
        #return HttpResponse(html)        
    
    #print "view(2):LEN:",  len(data), " DATA:", data
    
    #PDF part-Buffer
    buffer = BytesIO()
    pdf = createBarCodesv2(buffer, data, lesson)

    #Response 
    response = HttpResponse(content_type='application/pdf')
    today = date.today()
    filename = 'barcodes-' + str(lesson.id) + '-' + today.strftime('%Y-%m-%d')
    response['Content-Disposition'] ='attachement; filename={0}.pdf'.format(filename)
    response.write(pdf)
    return response

#########################################
# PDF Letter
#########################################
def pdfLetter(request):

    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    GraderArrayID = json.loads(request.GET['jqxinputGraderArrayID']) 
    LetterCode = request.GET.get('LetterCode', None)
    #jqxinputLesson = request.POST.get('jqxinputGraderNewLesson', None)
    print LessonID, GraderArrayID, LetterCode
    
    #Data
    #data = Grader.objects
    #data = GraderJoinTables(LessonID=None, exclude=False)
    data = Grader.objects.select_related("LessonID", "TeacherID")
    
    #GraderArrayIDInt = [int(e) if e.isdigit() else e for e in GraderArrayID.split(',')]
    GraderArrayIDInt = [int(e) if e.isdigit() else e for e in GraderArrayID.split(',')]
    
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)    
        data = data.filter(LessonID=LessonID)
    
    if GraderArrayID:
        data = data.filter(pk__in = GraderArrayIDInt)
        #(no__gte = fromNo) (no__lte= toNo)
    
    #if not LetterCode:
    #    LetterCode =1
        #(no__gte = fromNo) (no__lte= toNo)
    
    """
    #print 'POST Received:', jqxinputLesson, jqxinputTeacherArray        
    #lessonIsNull = True  if jqxinputLesson == ''  else False 
    #teacherArrayIsNull = True  if jqxinputTeacherArray == ''  else False 

    #print "Found in DB (LESSON):", lesson.name
    for jqxinputTeacher in jqxinputTeacherArray:
        teacher = Teacher.objects.get(id = jqxinputTeacher )  # get Teacher Data 
        #print "Found in DB (TEACHER):", teacher.surname
        graderExists = False  if Grader.objects.filter(TeacherID = teacher, LessonID = lesson).count() == 0  else True 
        if not (graderExists):
            #print 'No GraderExists:', teacher,  lesson
            # INSERT to DB > MUST CHECK FOR FAIL CONDITIONS
            Grader(LessonID = lesson, TeacherID = teacher, ).save()
            #print 'INSERT Grader:', teacher,  lesson
        else: 
            print 'GraderExists:', teacher,  lesson
            status = 'Error'

    dictData = {'status': status, }
    """

    data = data.order_by('TeacherID__surname', 'TeacherID__name')
    print data
    
    #
    #PDF part 
    #
    #Buffer
    buffer = BytesIO()
    pdf = createPDFLetters(buffer, data, LetterCode)

    #
    #Response part
    #
    response = HttpResponse(content_type='application/pdf')
    today = date.today()
    #filename = 'Letters' + today.strftime('%Y-%m-%d')
    filename = 'Letters'
    response['Content-Disposition'] =\
        'attachement; filename={0}.pdf'.format(filename)
    
    response.write(pdf)
    return response
    """
    """

#########################################
# PDF Users
#########################################
def print_users(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="My Users.pdf"'

    buffer = BytesIO()

    report = MyPrint(buffer, 'Letter')
    pdf = report.print_users()

    response.write(pdf)
    return response




#########################################
# XLS ACCEPTANCE
#########################################
def xlsAcceptance(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
    else:
        lesson = None
    
    #Data
    data = AcceptanceJoinTablesX2(LessonID).order_by('LessonID__name','SchoolToGradeID__name')
    #print data    
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Acceptance.xlsx'
    xlsx_data = doXlsAcceptance(data, lesson)
    response.write(xlsx_data)
    return response

#########################################
# XLS ACCEPTANCE
def xlsAcceptanceSum(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
    else:
        lesson = None
    
    #Data
    data = AcceptanceJoinTablesX2(LessonID).values('LessonID', 'LessonID__name', 'LessonID__type').all()\
            .annotate(sumBooks=Sum('books'), sumBooksAbscent=Sum('booksAbscent'), sumBooksZero=Sum('booksZero'), )\
            .order_by('LessonID__type','LessonID__name')
            #.order_by('-sumBooks')
            
    #print data    
    #[{'LessonID': 4, 'sumBooks': 662}, {'LessonID': 5, 'sumBooks': 0}, 
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=AcceptanceSum.xlsx'
    xlsx_data = doXlsAcceptanceSum(data, lesson)
    response.write(xlsx_data)
    return response


#########################################
# XLS BOOKING
#########################################
def xlsBooking(request):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    #if LessonID is not None:
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        data = BookingJoinTables().filter(FolderID__LessonID=LessonID)
    else:
        lesson = None
        data = BookingJoinTables().all()
    
    #Grader as filter
    GraderID = request.GET.get('GraderID', None)
    #if GraderID is not None :
    if GraderID :
        grader = Grader.objects.get(id=GraderID)
        data = data.filter(GraderID=GraderID)
    else:
        grader = None
        data = data

    #Date as filter
    dateFrom = request.GET.get('dateFrom', None)
    #if GraderID is not None : FAILS 
    if dateFrom:
        day, month, year = dateFrom.split("/")
        data = data.filter( actionTime__year= year, actionTime__month=month, actionTime__day=day, )
    else:
        data = data

    print 'LessonID:', LessonID, 'GraderID:', GraderID, 'dateFrom:', dateFrom
    #Data
    #.filter(FolderID__LessonID__id=LessonID)\
    data = data.order_by('FolderID__LessonID__name')
    #.filter(GraderID=GraderID)\
    #.order_by('LessonID__name','SchoolToGradeID__name')
    #print data    
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Booking.xlsx'
    xlsx_data = doXlsBooking(data, lesson)
    response.write(xlsx_data)
    return response

def xlsBookingDays(request, LessonID=None, dateFrom=None, dateTo=None):
    pass
    """
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
    else:
        lesson = None
    
    #Date as filter
    #dateFrom = request.GET.get('dateFrom', None)    
    #dateTo = request.GET.get('dateTo', None)    
    
    #Data
    data = BookingJoinTables().order_by('FolderID__LessonID__name')
    #print data        
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=BookingDay.xlsx'
    xlsx_data = doXlsBookingDay(data, lesson)
    response.write(xlsx_data)
    return response
"""

#########################################
# XLS BOOKING WEEKDAYS
#########################################
"""
WEEKDAYS COUNT
Get WEEKDAYS for ALL GRADERS + ALL LESSONTS 
"""
def xlsBookingWeekdaysCount(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    #if LessonID is not None:
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        #data = BookingJoinTables().filter(FolderID__LessonID=LessonID)
    else:
        lesson = None
        #data = BookingJoinTables().all()
    
    # FILTER ON WEEKENDS #OK

    weekdays=[1,2,3,4,5,6,7]
    #WeekEnds=[1,7]

    #OK-HMERES ERGASIAS
    #data = data.extra(select={'day':'date( actionTime )'}).values('GraderID_id', 'day')
    """
    data = Booking.objects.filter(actionTime__week_day__in=weekdays).select_related("FolderID", "GraderID").all()
    data = data.extra(select={'day':'date( actionTime )', 'TotalWeekdays':'COUNT(DISTINCT(date(actionTime)))'}).values('GraderID_id','GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 'TotalWeekdays')
    print data
    """
    dbData = Booking.objects.filter(actionTime__week_day__in=weekdays).select_related("GraderID")\
            .extra(select={'date':'DATE(actionTime)','count':'COUNT(GraderID_id)'})\
            .values('date','GraderID_id',\
            'GraderID__TeacherID__id','GraderID__TeacherID__surname','GraderID__TeacherID__name','GraderID__TeacherID__codeAfm','GraderID__TeacherID__codeGrad',)\
            .order_by('GraderID__TeacherID__surname','GraderID__TeacherID__name', 'date')

    """ Custom fuct. to couint days in dbData dict for each Grader """
    data=countDays0(dbData)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=BookingWeekdaysCount.xlsx'
    xlsx_data = doXlsBookingWeekdaysCount(data, lesson)
    response.write(xlsx_data)
    return response


#########################################
# XLS BOOKING WEEKDAYS DETAILS
#########################################
def xlsBookingWeekdaysDetails(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    #if LessonID is not None:
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        #data = BookingJoinTables().filter(FolderID__LessonID=LessonID)
    else:
        lesson = None
        #data = BookingJoinTables().all()
    
    # FILTER ON WEEKENDS #OK
    # Saturday = 7 Sunday = 1 | 1: SUNDAY, 2: MONDAY etc.
    #data = data.order_by('FolderID__LessonID__name'
    weekdays=[1,2,3,4,5,6,7]
    #WeekEnds=[1,7]
    data = Booking.objects.filter(actionTime__week_day__in=weekdays).select_related("FolderID", "GraderID").all()
    data = data.extra(select={'day':'date( actionTime )'})\
            .values('GraderID_id', 'GraderID__LessonID__name', 'GraderID__LessonID__type',\
                    'GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 'day')\
            .annotate(available=Count('actionTime')).annotate(sumDuration=Sum('actionDuration'))\
            .order_by('day', 'GraderID__LessonID','GraderID',)\

    #print "days (%2.2f) hours (%0.2f) minutes (%0.2f)" %(td.days, td.seconds//3600, (td.seconds//60)%60)
    print data    
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=BookingWeekdays.xlsx'
    xlsx_data = doXlsBookingWeekdaysDetails(data, lesson)
    response.write(xlsx_data)
    return response




#########################################
# XLS BOOKING  WEEKENDS COUNT
#########################################
"""
Get Weekend DAYS for ALL GRADERS + ALL LESSONTS 
"""
def xlsBookingWeekendsCount(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    #if LessonID is not None:
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        #data = BookingJoinTables().filter(FolderID__LessonID=LessonID)
    else:
        lesson = None
        #data = BookingJoinTables().all()
    
    # FILTER ON WEEKENDS #OK
    #Lesson as filter
    weekends=[1,7]    
    # FILTER ON WEEKENDS #OK
    # Saturday = 7 Sunday = 1 | 1: SUNDAY, 2: MONDAY etc.
    #+ SK ERGASIAS
    #OK-HMERES ERGASIAS
    """
    data = Booking.objects.filter(actionTime__week_day__in=WeekEnds).select_related("FolderID", "GraderID").all()
    data = data.extra(select={'day':'date( actionTime )', 'TotalWeekends':'COUNT(DISTINCT(date(actionTime)))'})\
            .values('GraderID_id','GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 'TotalWeekdays')
    """

    dbData = Booking.objects.filter(actionTime__week_day__in=weekends).select_related("GraderID")\
            .extra(select={'date':'DATE(actionTime)','count':'COUNT(GraderID_id)'})\
            .values('date','GraderID_id',\
            'GraderID__TeacherID__id','GraderID__TeacherID__surname','GraderID__TeacherID__name','GraderID__TeacherID__codeAfm','GraderID__TeacherID__codeGrad',)\
            .order_by('GraderID__TeacherID__surname','GraderID__TeacherID__name', 'date')

    """ Custom fuct. to couint days in dbData dict for each Grader """
    data=countDays0(dbData)

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=BookingWeekendsCount.xlsx'
    xlsx_data = doXlsBookingWeekendsCount(data, lesson)
    response.write(xlsx_data)
    return response


#########################################
# XLS BOOKING  WEEKENDS COUNT
#########################################
"""
Gets Weekend workdsys for Grader 
"""
def xlsBookingWeekendsDetails(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    #if LessonID is not None:
    weekends=[1,7]
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        data = Booking.objects.filter(FolderID__LessonID=lesson,actionTime__week_day__in=weekends).select_related("FolderID", "GraderID").all()
    else:
        lesson = None
        data = Booking.objects.filter(actionTime__week_day__in=weekends).select_related("FolderID", "GraderID").all()
    
    # FILTER ON WEEKENDS #OK
    # Saturday = 7 Sunday = 1 | 1: SUNDAY, 2: MONDAY etc.
    #data = data.order_by('FolderID__LessonID__name'
    #weekdays=[1,2,3,4,5,6,7]
    """
    data = Booking.objects.filter(actionTime__week_day__in=weekdays).select_related("FolderID", "GraderID")\
         .values('GraderID__LessonID__name',
                            'GraderID_id', 'GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 
                            'actionTime'
                            )\
         .extra(select={'day':'date( actionTime )'})\
            .annotate(countTimes=Count('actionTime'))\
            .annotate(sumDuration=Sum('actionDuration'))\
            .order_by('GraderID__LessonID','GraderID','day',)\
            .values('GraderID__LessonID__name', 'GraderID__LessonID__type',
                    'GraderID_id', 'GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 
                    'sumDuration', 'countTimes',
                    )
            #.order_by('GraderID__LessonID', 'GraderID','actionTime',)
            #.values('GraderID__LessonID', 'GraderID','actionTime',)\
    """
    #data = Booking.objects.filter(actionTime__week_day__in=weekends).select_related("FolderID", "GraderID").all()
    
    data = data.filter(action=1).extra(select={'day':'date(actionTime)'})\
            .values('GraderID_id', 'GraderID__LessonID__name', 'GraderID__LessonID__type', 'GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 'day')\
            .annotate(available=Count('actionTime')).annotate(sumDuration=Sum('actionDuration'))\
            .order_by('day', 'GraderID__LessonID','GraderID',)
    """

    #SOLUTION 2 - VIA FIELD TRANSFORM 
    data = data.extra(select={'day':'date(actionTime)'})\
            .values('GraderID_id', 'GraderID__LessonID__name', 'GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 'day')\
            .annotate(actionDurationINT=ExpressionWrapper(F('actionDuration'), output_field=IntegerField()))

    data = data.filter(actionDurationINT__isnull=False)\
            .annotate(SumActionDurationINT=Sum('actionDurationINT'))\
            .annotate(available=Count('actionTime'))\
            .order_by('day', 'GraderID__LessonID','GraderID',)
    """


    #print "days (%2.2f) hours (%0.2f) minutes (%0.2f)" %(td.days, td.seconds//3600, (td.seconds//60)%60)
    print data    
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=BookingWeekendsSum.xlsx'
    xlsx_data = doXlsBookingWeekendsDetails(data, lesson)
    response.write(xlsx_data)
    return response



"""
Probably redundant
"""
def xlsBookingGrader(request, LessonID=None, GraderID=None):
    pass
    """   
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID is not None :
        lesson = Lesson.objects.get(id=LessonID)
    else:
        lesson = None
    
    #Grader as filter
    GraderID = request.GET.get('GraderID', None)
    if GraderID is not None :
        grader = Grader.objects.get(id=GraderID)
    else:
        grader = None

    #Date as filter
    #dateFrom = request.GET.get('dateFrom', None)    
    #dateTo = request.GET.get('dateTo', None)    

    #Data
    data = BookingJoinTables(LessonID).order_by('LessonID__name','SchoolToGradeID__name')
    #print data    
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=BookingGrader.xlsx'
    xlsx_data = doXlsBookingGrader(data, lesson)
    response.write(xlsx_data)
    return response
    """   



#########################################
# XLS FOLDER
#########################################
def xlsFolder(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        data = Folder.objects.filter(LessonID=LessonID)
    else:
        lesson = None
        data = Folder.objects.all()
    
    #Data
    #data = FolderJoinTables(LessonID, exclude=False).order_by('LessonID__name', 'codeType', 'no')
    data = data.select_related("LessonID").order_by('LessonID__name', 'codeType', 'no')
    #print data    
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Folder.xlsx'
    xlsx_data = doXlsFolder(data, lesson)
    response.write(xlsx_data)
    return response



#############################################
# Fakeloi pou kathysteroun na diorthwthoun peran enos xronikou oriou (eg 3 days)
def xlsFolderDelays(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        #data = Folder.objects.filter(LessonID = LessonID)
    else:
        lesson = None
        #data = Folder.objects.all()
    
    #Data    
    #data = Folder.objects).filter( codeLocation = 1 ).order_by('LessonID__name', 'codeType', 'no').values()
    #data= Booking.objects.select_related("FolderID", "GraderID").filter(FolderID__codeLocation=1).order_by('GraderID__LessonID', 'FolderID__codeType', 'actionTime')
    now = datetime.now()
    timeDelta = timedelta(days=settings.CONST_MAXACTIONDURATION)    #Help scripts
    checkDate = now - timeDelta
    data = Booking.objects.select_related("FolderID", "GraderID")\
            .filter(actionTime__lt=checkDate,action=0, station=0)\
            .exclude(FolderID__codeStatus=2)\
            .order_by('GraderID__LessonID', 'FolderID__codeType', 'FolderID__no', 'actionTime')     #ok   
            #.filter(FolderID__codeLocation=1, action=0, station=0)\

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=FolderDelays.xlsx'
    xlsx_data = doXlsFolderDelays(data, lesson)
    response.write(xlsx_data)
    return response


#############################################
# Istoriko Fakelwn
def xlsFolderHistory(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        data = Folder.objects.filter(LessonID = LessonID)
    else:
        lesson = None
        data = Folder.objects.all().order_by('LessonID')


    #FOLDER HISTORY OK
    dataObj = []
    #for f in Folder.objects.all().order_by('LessonID'):
    for f in data:
        graders=Folder.objects.get(id=f.id).bookings.all().distinct()
        dataObj.append({'f':f, 'g':graders,});        
        """
        #print "F=>", f.id,
        for g in graders:
            print g.TeacherID.surname,
        """
        #print "x"
    
    """
    #OK-FOLDERS WITH GRADERS-NOW 
    dataObj = []
    for f in Folder.objects.filter(codeLocation=1).order_by('LessonID'):
        bookings=f.booking_set.filter(action=0).order_by('-actionTime').distinct()
        dataObj.append({'f':f, 'b':bookings[0],});
    """
    #print data    

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=FolderHistory.xlsx'
    xlsx_data = doXlsFolderHistory(dataObj, lesson)
    response.write(xlsx_data)
    return response

#############################################
# Fakeloi pou diorthonontai twra!
def xlsFolderNow(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        data = Folder.objects.filter(LessonID=LessonID, codeLocation=1)
    else:
        lesson = None
        data = Folder.objects.filter(codeLocation=1).order_by('LessonID')

    #OK-FOLDERS WITH GRADERS-NOW 
    dataObj = []
    for f in data:
    #for f in Folder.objects.filter(codeLocation=1).order_by('LessonID'):
        bookings=f.booking_set.filter(action=0).order_by('-actionTime').distinct()
        dataObj.append({'f':f, 'b':bookings[0],});
    #print data    

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=FolderNow.xlsx'
    xlsx_data = doXlsFolderNow(dataObj, lesson)
    response.write(xlsx_data)
    return response

#############################################σ
# Katastasi Fakelvn (sxetikh me diorvsh) 
# ...Count (codeType, codeStatus, )  ... GroupBy (codeType, codeStatus) 
#{'codeType': 0, 'countCodeType': 21, 'LessonID': 4, 'codeStatus': 0}
def xlsFolderStatus0(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        data = Folder.objects.filter(LessonID=LessonID)
    else:
        lesson = None
        data = Folder.objects.all()

    dataDB = data.values('codeLocation', 'codeStatus', 'codeType', 'LessonID', 'LessonID__name')\
        .annotate(countCodeType=Count('codeStatus'),)\
        .order_by('LessonID','codeType','codeStatus')
        #{'codeType': 0, 'countCodeType': 21, 'LessonID': 4, 'codeStatus': 0}    
    #print dataDB

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=FolderStatus0.xlsx'      
    xlsx_data = doXlsFolderStatus0(dataDB, lesson)
    response.write(xlsx_data)
    return response


    ###############################################
    # INTO XLXS Sheet 
    #xlsx_data = doXlsFolderStatus0(data, lesson)
    #def doXlsFolderStatus0 (dataDB, lesson=None):
    """
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("FolderStatus0")

    title, header, cell, cell_center = formatAWorkbook(workbook)
    
    # write title
    lesson_text = xlsTitle(lesson)
    title_text = u"{0} {1}".format(ugettext(u"ΣΥΝΟΛΑ ΦΑΚΕΛΩΝ"), lesson_text)    
    worksheet_s.merge_range('A2:F2', title_text, title)

    # column widths
    lesson_col_width = 15
    stringColWidth = 20
    numberColWidth = 5     

    #print dataDB

    # 2nd hash no DB data
    hashDataDB = itertools.groupby(dataDB, lambda item: item["LessonID"])

    # SubGroups list of Folders #OK
    row = 5 
    for key, group in hashDataDB:
        #print key, ([item for item in group])

        # get Total Folders for Lesson 
        fABC = Folder.objects.filter(LessonID=key).values('LessonID', 'LessonID__name', 'codeType')\
                .annotate(countType=Count('codeType'),)

        # hack for lesson mame
        lname= fABC[0]['LessonID__name'] 

        #defaults for count(codeType)
        (fA, fB, fC) = (0, 0, 0)
        for x in fABC: 
            if x['codeType']==0 : 
                fA = x['countType']
            elif x['codeType']==1 : 
                fB = x['countType']
            elif x['codeType']==2 : 
                fC = x['countType']

        print key, (fA, fB, fC)        
        #(fA, fB, fC) = (100, 100, 100)

        #lesson = 'LessonID__name'
        # write totals > header 
        row = row + 1
        worksheet_s.write_string(row, 1, u'ΜΑΘΗΜΑ', cell_center)
        worksheet_s.write_string(row, 2, u'Συν Φ(Α)', cell_center)
        worksheet_s.write_string(row, 3, u'Συν Φ(B)', cell_center)
        worksheet_s.write_string(row, 4, u'Συν Φ(ANA)', cell_center)
        # write totals > data 
        row = row + 1
        worksheet_s.write_string(row, 1, lname, cell_center)
        worksheet_s.write_number(row, 2, fA, cell_center)
        worksheet_s.write_number(row, 3, fB, cell_center)
        worksheet_s.write_number(row, 4, fC, cell_center)
        # write counts > header 
        row = row + 1
        worksheet_s.write(row, 0, ugettext(u"AA"), header)
        worksheet_s.write(row, 1, ugettext(u"Μάθημα"), header)
        worksheet_s.write(row, 2, ugettext(u"Τύπος"), header)
        worksheet_s.write(row, 3, ugettext(u"Κατάσταση"), header)
        worksheet_s.write(row, 4, ugettext(u"Πλήθος"), header)
        worksheet_s.write(row, 5, ugettext(u"Ποσοστό"), header)

        # write counts > data 
        row = row + 1
        for idx, data in enumerate(group):

            #write cell data
            worksheet_s.write_number(row, 0, idx + 1, cell_center)

            val = data['LessonID__name']
            #val = 'LessonID__name'
            worksheet_s.write_string(row, 1, val, cell)        
            #if len(val) > lesson_col_width: lesson_col_width = len(val)

            val = (Folder.lexCodeType(Folder, data['codeType']))
            #val = data['codeType']
            worksheet_s.write_string(row, 2, val, cell)        
            
            val = (Folder.lexCodeStatus(Folder, data['codeStatus']))
            #val = data['codeStatus']
            worksheet_s.write_string(row, 3, val, cell)        
                    
            # Same value for countCodeType, countCodeStatus, countCodeLocation
            val = data['countCodeType']
            worksheet_s.write_number(row, 4, val, cell_center)

            # calc percntage %
            if data['codeType'] in [0,1]:    # is fAB
                val= float(100*data['countCodeType']) / (fA+fB)
            elif data['codeType']==2:         # is fC
                val= float(100*data['countCodeType']) / (fC)
            else: 
                val= 0
            #money = workbook.add_format({'num_format': '$#,##0'})
            percent_format = workbook.add_format({'num_format': '0.00"%"'})  
            worksheet_s.write_number(row, 5, val, percent_format)
            
            # next row
            row = row +1
        
        # skip 3 lines / new lesson 
        row = row +3
        # change column widths
        worksheet_s.set_column('B:E', stringColWidth) 

	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    
    #return xlsx_data
    ############################################### 
    response.write(xlsx_data)
    return response
    """



# Synola+Counts Fakelvn 
# ...Count (codeType, codeStatus, CodeLocation)  ... GroupBy (codeType, codeStatus) 
#[{'countCodeLocation': 4, 'countCodeType': 4, 'codeStatus': 0, 'codeType': 0, 'LessonID': 4, 'countCodeStatus': 4},
def xlsFolderStatus1(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
    else:
        lesson = None
    
    #Data
    data = Folder.objects.all().values('codeStatus', 'codeType', 'codeLocation', 'no', 'LessonID')\
        .annotate(countCodeType=Count('codeType'), countCodeStatus=Count('codeStatus'), countCodeLocation=Count('codeLocation'))\
        .order_by('LessonID','codeType')
    #[{'countCodeLocation': 4, 'countCodeType': 4, 'codeStatus': 0, 'codeType': 0, 'LessonID': 4, 'countCodeStatus': 4},

    #Folder.objects.all().values('codeStatus', 'codeType', 'LessonID').annotate(countStatus=Count('codeStatus')).order_by('LessonID','codeType')
    #print data    
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=FolderStatus.xlsx'
    xlsx_data = doXlsFolderStatus(data, lesson)
    response.write(xlsx_data)
    return response


#
def xlsFolderSum(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        data = Folder.objects.filter(LessonID=LessonID)
    else:
        lesson = None
        data = Folder.objects.all()
    
    #Data
    #data = FolderJoinTables(LessonID, exclude=False).order_by('LessonID__name', 'codeType', 'no')
    data = data.values('codeStatus', 'codeType', 'codeLocation', 'LessonID', 'LessonID__name', 'LessonID__type',)\
        .annotate(countCodeType=Count('codeType'), countCodeStatus=Count('codeStatus'), countCodeLocation=Count('codeLocation'))\
        .order_by('LessonID','codeType')
    #[{'countCodeLocation': 4, 'countCodeType': 4, 'codeStatus': 0, 'codeType': 0, 'LessonID': 4, 'countCodeStatus': 4},
    print data    
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=FolderSum.xlsx'
    xlsx_data = doXlsFolderSum(data, lesson)
    response.write(xlsx_data)
    return response



#########################################
# XLS GRADER
#########################################
def xlsGrader(request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
    else:
        lesson = None
    
    #Data
    data = GraderJoinTables(LessonID, exclude=False).order_by('LessonID__name', 'TeacherID__surname', )
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Grader.xlsx'
    xlsx_data = doXlsGrader(data, lesson)
    response.write(xlsx_data)
    return response


#########################################
#ΕΙΚΟΝΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΗ
def xlsGraderWorkv3(request, LessonID=None):
    
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        data = Grader.objects.filter(LessonID=LessonID)
    else:
        lesson = None
        data = Grader.objects.all()
    
    data = data.order_by('LessonID__name', 'TeacherID__surname')

    # Prepare data
    dataObj=[]
    for idx, g in enumerate(data):
        bSet = g.booking_set\
                .values('GraderID__id', 'FolderID__id', 'FolderID__no', 'wasTypeOf')\
                .annotate(sumAction=Sum('actionDuration'))
        # Append Data
        dataObj.append({'g':g,'bSums':bSet,})
        """
        print g.id, g.LessonID.name, g.TeacherID.surname#, bSet
        for b in bSet: 
            print "\t", b['FolderID__id'], b['sumAction'], b['wasTypeOf']
        """
    #print data    

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=GraderWorkv3.xlsx'
    xlsx_data = doXlsGraderWorkv3(dataObj)
    response.write(xlsx_data)
    return response

#########################################
#ΕΙΚΟΝΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΗ
def xlsGraderWorkv2(request, LessonID=None):
    
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        data = Grader.objects.filter(LessonID=LessonID)
    else:
        lesson = None
        data = Grader.objects.all()

    # we get each grader
    data = data.order_by('LessonID__name', 'TeacherID__surname')
    # we must access each grader on Booking Records now 
    #data = Grader.objects.filter(LessonID__id=9)[0].booking_set.filter(action=0, station=0).values()

    #Data
    #data = FolderJoinTables(LessonID, exclude=False).order_by('LessonID__name', 'codeType', 'no')
    """
    data = data.values('codeStatus', 'codeType', 'codeLocation', 'LessonID', 'LessonID__name')
        .annotate(countCodeType=Count('codeType'), countCodeStatus=Count('codeStatus'), countCodeLocation=Count('codeLocation'))\
        .order_by('LessonID','codeType')
    """
    #data = data.values()
    print data    

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=GraderWorkv2.xlsx'
    xlsx_data = doXlsGraderWorkv2(data)
    response.write(xlsx_data)
    return response


##########################################################33
#ΕΙΚΟΝΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΗ-OLD
def xlsGraderWork(request, LessonID=None):
    
    #Data
    #data = GraderJoinTables(LessonID, exclude=False).order_by('LessonID__name', 'TeacherID__surname', )

    data = BookingJoinTablesX3().filter(station=0, action=1,)\
            .values('GraderID', 'GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 
                    'FolderID__LessonID__name', 'FolderID__no', 'station', 'action')\
            .annotate(countaction=Count('action')).order_by('action')
    #data = Booking.objects.all().values('GraderID', 'station', 'action').annotate(countAction=Count('GraderID'))
    #[{'FolderID__no': 1, 'action': 1, 'station': 0, 'countaction': 1, 'GraderID': 46}]
    
    #print data 

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=GraderWork.xlsx'
    xlsx_data = doXlsGraderWork(data)
    response.write(xlsx_data)
    return response



"""

"""
def xlsGraderWorkDay(request, LessonID=None):
    

    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    #if LessonID is not None:
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
        data = BookingJoinTables().filter(FolderID__LessonID=LessonID)
    else:
        lesson = None
        data = BookingJoinTables().all()
    
    #Grader as filter
    GraderID = request.GET.get('GraderID', None)
    #if GraderID is not None :
    if GraderID :
        grader = Grader.objects.get(id=GraderID)
        data = data.filter(GraderID=GraderID)
    else:
        grader = None
        data = data

    #Date as filter
    dateFrom = request.GET.get('dateFrom', None)
    #if GraderID is not None : FAILS 
    if dateFrom:
        day, month, year = dateFrom.split("/")
        data = data.filter( actionTime__year= year, actionTime__month=month, actionTime__day=day, )
    else:
        data = data

    #print 'LessonID:', LessonID, 'GraderID:', GraderID, 'dateFrom:', dateFrom
    #Data
    #.filter(FolderID__LessonID__id=LessonID)\
    data = data.order_by('FolderID__LessonID__name')
    #.filter(GraderID=GraderID)\
    #.order_by('LessonID__name','SchoolToGradeID__name')
    #print data    


    #Data
    #.filter(FolderID__LessonID__id=LessonID)\
    #.filter(GraderID=GraderID)\
    #.order_by('LessonID__name','SchoolToGradeID__name')
    #print data    



    data = BookingJoinTablesX3().filter(station=0, action=1,)\
            .values('GraderID', 'GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 
                    'FolderID__LessonID__name', 'FolderID__no', 
                    'station', 'action', 'actionTime')\
            .annotate(countaction=Count('action')).order_by('action')\
            .order_by('actionTime')
            #'GraderID__TeacherID__surname', 'GraderID__TeacherID__name'

    #data = data.order_by('FolderID__LessonID__name')
    #print data 

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=GraderWorkDay.xlsx'
    xlsx_data = doXlsGraderWorkDay(data)
    response.write(xlsx_data)
    return response





#########################################
# XLS TOTAL
#########################################
def xlsTotal (request, LessonID=None):
    
    #Lesson as filter
    LessonID = request.GET.get('LessonID', None)
    if LessonID:
        lesson = Lesson.objects.get(id=LessonID)
    else:
        lesson = None    
    #print '\nLessonID:', LessonID,
    #Data
    data = BookingJoinTables()\
            .filter(FolderID__LessonID__id=LessonID)\
            .order_by('FolderID__LessonID__name')
            #.filter(GraderID=GraderID)\
            #.order_by('LessonID__name','SchoolToGradeID__name')
    #print data    
    
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Total.xlsx'
    xlsx_data = doXlsTotal(data, lesson)
    response.write(xlsx_data)
    return response


#########################################
# XLS VAR 
#########################################
def homeXls(request):
    
    data = Folder.objects.all()
    #print data
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
    
    # Write xls data 
    xlsx_data = WriteToExcel(data, None)
    
    response.write(xlsx_data)
    return response


def WriteToExcel(weather_data, town=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Summary")



"""
def weather_history(request):
    weather_period = Weather.objects.all()
    town = None
    if request.method == 'POST':
        form = WeatherForm(data=request.POST)
        if form.is_valid():
            town_id = form.data['town']
            #town = Town.objects.get(pk=town_id)
            #weather_period = Weather.objects.filter(town=town_id)
        if 'excel' in request.POST:
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
            xlsx_data = WriteToExcel(weather_period, town)
            response.write(xlsx_data)
            return response
        if 'pdf' in request.POST:
            response = HttpResponse(content_type='application/pdf')
            today = date.today()
            filename = 'pdf_demo' + today.strftime('%Y-%m-%d')
            response['Content-Disposition'] =\
                'attachement; filename={0}.pdf'.format(filename)
            buffer = BytesIO()
            report = PdfPrint(buffer, 'A4')
            pdf = report.report(weather_period, 'Weather statistics data')
            response.write(pdf)
            return response
    else:
        form = WeatherForm()

    template_name = "exportingfiles/weather_history.html"
    context = {
        'form': form,
        'town': town,
        'weather_period': weather_period,
    }
    return render(request, template_name, context)



def all_towns(request):
    towns = Town.objects.all()
    template_name = "exportingfiles/all_towns.html"
    context = {
        'towns': towns,
    }
    return render(request, template_name, context)


def today_weather(request):
    today = date.today()
    today_w = Weather.objects.filter(date=today)
    template_name = "exportingfiles/today_weather.html"
    context = {
        'today_weather': today_w
    }
    return render(request, template_name, context)


def details(request, weather_id):
    weather = Weather.objects.get(pk=weather_id)
    template_name = "exportingfiles/details.html"
    context = {
        'weather': weather,
    }
    return render(request, template_name, context)



"""

