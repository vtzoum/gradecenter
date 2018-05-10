#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import time
from django.utils.translation import ugettext_lazy as _
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.charts.linecharts import SampleHorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table,\
    TableStyle


#Barcode
from reportlab.graphics.barcode import code39, code128, code93
from reportlab.graphics.barcode import eanbc, qr, usps
from reportlab.graphics.shapes import Drawing 
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.graphics import renderPDF


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


import time
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch


from django.conf import settings
#from .settings import STATIC_ROOT
from django.utils.translation import ugettext
from .utils import get_temperatures, get_wind_speed, get_str_days,\
    get_random_colors, precip_prob_sum, get_percentage
legendcolors = get_random_colors(10)


from django.conf import settings
from django.conf.urls.static import static

#print settings.STATIC_ROOT
#pdfmetrics.registerFont(TTFont('FreeSans', settings.STATIC_ROOT + 'reporting/fonts/FreeSans.ttf'))
#pdfmetrics.registerFont(TTFont('FreeSansBold', settings.STATIC_ROOT + 'reporting/fonts/FreeSansBold.ttf'))


from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from excel_utils import xlsTitle
from personel.models import *

################################################
# FONTS 
################################################
pdfmetrics.registerFont(TTFont('DejaVuSansMono', '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'))
pdfmetrics.registerFont(TTFont('FreeSans', settings.STATIC_ROOT + '/static/reporting/fonts/FreeSans.ttf'))
pdfmetrics.registerFont(TTFont('FreeSansBold', settings.STATIC_ROOT + '/static/reporting/fonts/FreeSansBold.ttf'))
#/usr/share/fonts/truetype/dejavu/
#/media/tzoumak/CRUZER32GB/CoDe - PYTHON/PYTHON-LIBRARIES/PDF/reportlab/fonts/dejavu-fonts-ttf-2.37/ttf/

#VTZOUM HACK
#from django.templatetags.static import static
#pdfmetrics.registerFont(TTFont('FreeSans', static('reporting/fonts/FreeSans.ttf')))
#pdfmetrics.registerFont(TTFont('FreeSans', static('fonts/FreeSansBold.ttf')))


#########################################
# PDF Letters
#########################################
"""
"""
def createPDFLetters(buffer, data, LetterCode=1): 
    pass

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




