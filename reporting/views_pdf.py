#!/usr/bin/python
# -*- coding: utf-8 -*-

from io import BytesIO
import StringIO
import datetime
from datetime import date, timedelta
import itertools, json
import time

from django import forms
from django.conf import settings
#from .settings import STATIC_ROOT
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Avg, Count, Max, Min, Sum
from django.db.models import IntegerField, DurationField 
from django.db.models import ExpressionWrapper, Func, F
from django.db.models import IntegerField
#from django.settings import CONST_MAXACTIONDURATION
#from django.db.models.functions import Length, Upper
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

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


from utils_pdf import *

from personel.models import *
from personel.helpScripts import countDays0

#from pdf_letters import doPDFSchoolCoverLetter
#from pdf_labels import doPDFSchoolLabels

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
#PDF Labels
#########################################
"""

"""
def doPDFSchoolLabels(buffer, dataDB, lesson=None): 
    
    elements = []
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=0, leftMargin=1*cm, topMargin=-2.0*cm, bottomMargin=-1.5*cm)
    #doc = SimpleDocTemplate("tables+barcodes.pdf", pagesize=A4, rightMargin=0, leftMargin=6*cm, topMargin=0*cm, bottomMargin=0)

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']
    
    # write title
    #lesson_text = xlsTitle(lesson)
    #title_text = u"{0}({1})-{2}".format(lesson_text, lesson.category[0:3], Lesson.lexLessonType(Lesson, lesson.type)[0:2])
    #title_text = u"{0} {1}".format(ugettext(u"ΜΑΘΗΜΑ"), lesson_text)
    #valLessonType = (Lesson.lexLessonType(Lesson, dataDB[count]['codeType']))
    lesson_text = "L"
    title_text = "T"

    #Values to generate data from 
    recs=[]
    [recs.append(r) for r in dataDB]
        
    #Table settings 
    size = len(recs)
    cols = 2
    # needs coreect when barcode =1 
    rows = (size/cols  if size%cols == 0 else size/cols +1)
    #print "DATA TABLE: size(%d) cols(%d) rows(%d)" %(size, cols, rows)

    #Make Table 
    dataArray = []
    count = 0

    while count < size:
    #for d in dataDB:
        dataRow = []
        for j in range(0,cols):
            parag = []
            pageTexStyleHead = ParagraphStyle(name="pageTexStyleLesson", alignment=TA_LEFT, fontSize=16, 
                    leftIndent=16, leading=6, spaceBefore=0, spaceAfter=8,)
            pageTexStyleTag = ParagraphStyle(name="pageTexStyleExplain", alignment=TA_LEFT, fontSize=14, 
                    leftIndent=16, spaceBefore=4, spaceAfter=0,)
            #parag.append(Paragraph('title_text', pageTexStyleHead))
            
            schoolName =  recs[count].name
            schoolCode=  recs[count].code
            schoolDDE=  recs[count].ddeName
            #tag1 = u"%s ΦΑΚΕΛΟΣ: %s"  %(valType, str(valNo))            
                        
            parag.append(Paragraph(schoolDDE, pageTexStyleTag))
            parag.append(Paragraph(schoolName, pageTexStyleTag))
            parag.append(Paragraph(recs[count].address, pageTexStyleTag))
            parag.append(Paragraph(recs[count].city+' ' +recs[count].tk, pageTexStyleTag))

            #tag1 = uvalType, str(valNo))            
            parag.append(Spacer(width=32, height=10))

            dataRow.append(parag)
            # 2xsame tags for 1-size list
            if size==1:
                parag=[]
                parag.append(Spacer(32, 16))
                dataRow.append(parag)

            #print count
            count += 1 
            if count == size: 
                break
        
        dataArray.append(dataRow)
        
    table = Table(dataArray, colWidths=11*cm, rowHeights=4.45*cm)    

    elements.append(table)
    doc.build(elements)

    # create document
    pdf = buffer.getvalue()
    buffer.close()
    return pdf



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


def doPDFSchoolCoverLetter(buffer, data, LetterCode=1): 
    
    constGCName=settings.CONST_REPORTS_GCENTER_NAME
    constGCPresdArticle=settings.CONST_REPORTS_GCENTER_PRESIDENT_ARTICLE
    constGCPresdName=settings.CONST_REPORTS_GCENTER_PRESIDENT_NAME
    constGCPresdSurname=settings.CONST_REPORTS_GCENTER_PRESIDENT_SURNAME

    Story = []
    styles=getSampleStyleSheet()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=0, leftMargin=1*cm, topMargin=0*cm, bottomMargin=0)
    #doc = SimpleDocTemplate("tables+barcodes.pdf", pagesize=A4, rightMargin=0, leftMargin=6*cm, topMargin=0*cm, bottomMargin=0)

    # Get StoryArrays 
    Story1=[]
    logo = settings.STATIC_ROOT + "/static/images/" + "python_logo.png"
    formatted_time = time.ctime()
    #IMAGE 
    im = Image(logo, 2*inch, 2*inch)
    Story1.append(im)
    
    # STYLES          
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='titleH', fontSize=24, leading=42, alignment=TA_CENTER, ))
    styles.add(ParagraphStyle(name='titleB',leading=42,alignment=TA_CENTER,\
            fontName='Helvetica-Bold', fontSize=24, )) 
    #parent=styles['default'],textColor=purple,

    #In Reportlab the linespacing is set using the leading style attribute according to the docs.    
    """
    styles = {}
    styles['title'] = ParagraphStyle( 'title',parent=styles['default'],leading=42,alignment=TA_CENTER,
        fontName='Helvetica-Bold', fontSize=24, textColor=purple,)
    """
    p1 = Paragraph("I'm a title!", styles['titleB']),
    ptext = '<font>%s</font>' % formatted_time     
    ptext = u'<font name="DejaVuSansMono"> ΠΡΩΤΟΚΟΛΛΟ ΠΑΡΑΔΟΣΗΣ ΚΑΙ ΠΑΡΑΛΑΒΗΣ</font>'
    Story1.append(Paragraph(ptext, styles["titleH"]))
    Story1.append(Spacer(1, 12))
    
    #Rec.-based data
    row = 0 
    for school in data:
        StoryDB = []
        
        name = school.name
        ddeName = school.ddeName
        #print "%s %s %s %s" %(s.code, s.name, s.ddeCode, s.ddeName)

        #ptext2 = u'<font name="DejaVuSansMono"> Σήμερα %s ημέρα  %s και ώρα %s</font>' %(datetime.now(), datetime.now(), datetime.now())
        ptext2 = u'<font name="DejaVuSansMono"> Σήμερα ......... ημέρα ......... και ώρα ......... </font>'
        ptext2 += u'<font name="DejaVuSansMono">o/η υπογραφόμενη/oς Πρόεδρος της Επιτροπής του %s</font>' %(constGCName)
        ptext2 += u'<font name="DejaVuSansMono"> παρέδωσα στη Δ/νση Δ.Ε. %s</font>' %(ddeName)
        ptext2 += u'<font name="DejaVuSansMono"> τα αποκόμματα, των γραπτών δοκιμίων και απουσιών, τις καταστάσεις βαθμολογίας '
        ptext2 += u'<font name="DejaVuSansMono"> των μαθητών της Γ΄Τάξης του %s που εξετάστηκαν στο %s.</font>' %(name, constGCName)
        StoryDB.append(Paragraph(ptext2, styles["Normal"]))
        ptext2 = u'<font name="DejaVuSansMono">Ο αριθμός τους κατά μάθημα και κατεύθυνση φαίνεται στον παρακάτω πίνακα.</font>'
        StoryDB.append(Paragraph(ptext2, styles["Normal"]))
        StoryDB.append(Spacer(1, 12))

        #Make TABLE 
        table_data = [(u'ΜΑΘΗΜΑ',u'ΤΕΤΡΑΔΙΑ',u'ΑΠΟΥΣΙΕΣ',u'ΜΗΔΕΝΙΣΜΕΝΑ', u'ΣΥΝΟΛΑ', )]
        #Loop RECORDs
        for rec in school.acceptance_set.all():
            # calc partial sum
            part_sum = (rec.books + rec.booksAbscent + rec.booksZero)
            table_data = table_data + [(rec.LessonID.name, rec.books, rec.booksAbscent, rec.booksZero, part_sum)]

        # Create the table
        #table = Table(table_data, colWidths=[doc.width/3.0]*3)
        #table = Table(table_data, colWidths=110, rowHeights=20)
        table = Table(table_data, rowHeights=20)
        
        """
        table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                        ('BOX', (0, 0), (-1, -1), 0.25, colors.black)]))
        """
        # TABLE 
        table.setStyle(TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))
        
        StoryDB.append(table)

        #TABLE-stories put together
        Story +=  Story1 + StoryDB #+ Story2 
        Story.append(PageBreak())
    
    # create document
    doc.build(Story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


"""
Returns 2 x Array Elements to be put Before and AFter Database Data
eg 
Story1 
>>StoryDB
Story2
etc
"""
def GetLetter(LetterCode): 
    pass

def GetLetterOld(LetterCode): 

    #if LetterCode == 'A1':
    if True:
        #doc = SimpleDocTemplate("form_letter.pdf",pagesize=letter, rightMargin=72,leftMargin=72,topMargin=72,bottomMargin=18)

        Story1=[]
        logo = settings.STATIC_ROOT + "/static/images/" + "python_logo.png"
        print logo

        magName = "Pythonista"
        issueNum = 12
        subPrice = "99.00"
        limitedDate = "03/05/2010"
        freeGift = "tin foil hat"

        formatted_time = time.ctime()
        full_name = "Mike Driscoll"
        address_parts = ["411 State St.", "Marshalltown, IA 50158"]
        
        #IMAGE 
        im = Image(logo, 2*inch, 2*inch)
        Story1.append(im)
        
        # STYLES          
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        styles.add(ParagraphStyle(name='titleH', fontSize=24, leading=42, alignment=TA_CENTER, ))
        #In Reportlab the linespacing is set using the leading style attribute according to the docs.
        """
        styles = {}
        styles['title'] = ParagraphStyle( 'title',
            parent=styles['default'],leading=42,alignment=TA_CENTER,
            fontName='Helvetica-Bold', fontSize=24, textColor=purple,
        )        
        p1 = Paragraph("I'm a title!", stylesheet['title']),
        """
        ptext = '<font size=12>%s</font>' % formatted_time
         
        Story1.append(Paragraph(ptext, styles["Normal"]))
        Story1.append(Spacer(1, 12))
        #return Story1
         
        # Create return address
        #if LetterCode == 'B1':
        Story2=[]
        ptext = '<font size=12>%s</font>' % full_name
        Story2.append(Paragraph(ptext, styles["Normal"]))       
        for part in address_parts:
            ptext = '<font size=12>%s</font>' % part.strip()
            Story2.append(Paragraph(ptext, styles["Normal"]))   
         
        Story2.append(Spacer(1, 12))
        ptext = '<font size=12>Dear %s:</font>' % full_name.split()[0].strip()
        Story2.append(Paragraph(ptext, styles["Normal"]))
        Story2.append(Spacer(1, 12))
         
        ptext = '<font size=12>We would like to welcome you to our subscriber base for %s Magazine! \
                You will receive %s issues at the excellent introductory price of $%s. Please respond by\
                %s to start receiving your subscription and get the following free gift: %s.</font>'\
                            % (magName,issueNum,subPrice,limitedDate,freeGift)

        Story2.append(Paragraph(ptext, styles["Justify"]))
        Story2.append(Spacer(1, 12))
                  
        ptext = '<font size=12>Thank you very much and we look forward to serving you.</font>'
        Story2.append(Paragraph(ptext, styles["Justify"]))
        Story2.append(Spacer(1, 12))
        ptext = '<font size=12>Sincerely,</font>'
        Story2.append(Paragraph(ptext, styles["Normal"]))
        Story2.append(Spacer(1, 48))
        ptext = '<font size=12>Ima Sucker</font>'
        Story2.append(Paragraph(ptext, styles["Normal"]))
        Story2.append(Spacer(1, 12))
        #doc.build(Story)
        return Story1, Story2



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


