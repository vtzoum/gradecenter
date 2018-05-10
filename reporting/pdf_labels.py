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
            parag.append(Paragraph('title_text', pageTexStyleHead))
            
            schoolName =  recs[count].name
            schoolCode=  recs[count].code
            schoolDDE=  recs[count].ddeName
            #tag1 = u"%s ΦΑΚΕΛΟΣ: %s"  %(valType, str(valNo))            
                        
            parag.append(Paragraph(schoolName, pageTexStyleTag))
            parag.append(Paragraph(schoolCode, pageTexStyleTag))
            parag.append(Paragraph(schoolDDE, pageTexStyleTag))
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


