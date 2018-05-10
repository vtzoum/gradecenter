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
# PDF Barcodes
#########################################
"""
Create barcode examples and embed in a PDF
buffer, pageSize
"""
def createBarCodesv2(buffer, dataDB, lesson=None): 
    
    elements = []
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=0, leftMargin=1*cm, topMargin=-2.0*cm, bottomMargin=-1.5*cm)
    #doc = SimpleDocTemplate("tables+barcodes.pdf", pagesize=A4, rightMargin=0, leftMargin=6*cm, topMargin=0*cm, bottomMargin=0)

    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleH = styles['Heading1']
    #story = []
    
    # write title
    lesson_text = xlsTitle(lesson)
    title_text = u"{0}({1})-{2}".format(lesson_text, lesson.category[0:3], Lesson.lexLessonType(Lesson, lesson.type)[0:2])
    #title_text = u"{0} {1}".format(ugettext(u"ΜΑΘΗΜΑ"), lesson_text)
    #valLessonType = (Lesson.lexLessonType(Lesson, dataDB[count]['codeType']))
    
    #Values to generate barcodes from
    barcode_values = [r['codeBarcode'] for r in dataDB]
    #barcode_values = ['0004-0000000001', '0004-0000000002','0004-0000000003','0004-0000000004','0004-0000000005',]
    #print dataDB
    print barcode_values 


    #Table settings 
    size = len(barcode_values)
    cols = 2
    # needs coreect when barcode =1 
    rows = (size/cols  if size%cols == 0 else size/cols +1)
    #print "BARCODE TABLE: size(%d) cols(%d) rows(%d)" %(size, cols, rows)

    #Paragraph styles
    pageTexStyleHead = ParagraphStyle(name="pageTexStyleLesson", alignment=TA_LEFT, fontSize=16, 
            leftIndent=16, leading=12, spaceBefore=0, spaceAfter=4,)
    #pageTexStyleHead = ParagraphStyle(name="pageTexStyleLesson", alignment=TA_LEFT, fontSize=16, 
    #        leftIndent=16, leading=14, spaceBefore=0, spaceAfter=8,)
    pageTexStyleTag = ParagraphStyle(name="pageTexStyleExplain", alignment=TA_LEFT, fontSize=14, 
            leftIndent=16, spaceBefore=0, spaceAfter=0,)
    #[ Paragraph("Occupation", pageTextStyleCenter) , userData['studentDetails'].get('fOccupation', "-")]

    #Make Table 
    barcodeArray = []
    count = 0
    while count < size:
        barcodeRow = []
        for j in range(0,cols):
        
            parag = []            
            #header-A
            """
            parag.append(Paragraph(title_text, pageTexStyleHead))
            valType = (Folder.lexCodeType(Folder, dataDB[count]['codeType']))
            valNo = dataDB[count]['no']                #eg. ΦΑ#1
            valBooks= dataDB[count]['books']       #eg. ΦΑ#1
            tag1 = u"%s ΦΑΚΕΛΟΣ: %s"  %(valType, str(valNo))
            tag2 = u"ΤΕΤΡΑΔΙΑ: %s"  %(str(valBooks))
            parag.append(Paragraph(tag1, pageTexStyleTag))
            parag.append(Paragraph(tag2, pageTexStyleTag))            
            parag.append(Spacer(width=32, height=10))
            """
            
            #header-B 2016-07-20
            parag.append(Paragraph(title_text, pageTexStyleHead))


            valType = (Folder.lexCodeType(Folder, dataDB[count]['codeType']))
            valNo = dataDB[count]['no']                #eg. ΦΑ#1
            valBooks= dataDB[count]['books']       #eg. ΦΑ#1
            tag1 = u"Φ%s%s ΤΕΤΡΑΔΙΑ:%d"  %(str(valNo), valType[1:],valBooks)
            #tag2 = u"ΤΕΤΡΑΔΙΑ: %s"  %(str(valBooks))
            parag.append(Paragraph(tag1, pageTexStyleTag))
            
            #parag.append(Paragraph(tag2, pageTexStyleTag))
            parag.append(Spacer(width=32, height=10))
            #parag.append(Spacer(width=32, height=10))
            
            #parag.append(Extended39("A012345B}"))
            barcode_code128 = code128.Code128(dataDB[count]['codeBarcode'], barHeight=.3*inch, barWidth = 1.3, humanReadable=True)            
            parag.append(barcode_code128)

            barcodeRow.append(parag)

            # 2xsame tags for 1-size list
            if size==1:
                parag=[]
                parag.append(Spacer(32, 16))
                barcodeRow.append(parag)

            #print count
            count += 1 
            if count == size: 
                break


        barcodeArray.append(barcodeRow)

    #print barcodeArray
    #table = Table(barcodeArray, colWidths=doc.width/2, rowHeights=doc.height/8)
    
    table = Table(barcodeArray, colWidths=11*cm, rowHeights=4.45*cm)
    
    #parts.append(Spacer(1, 0.5 * inch))
    elements.append(table)
    doc.build(elements)

    # create document
    pdf = buffer.getvalue()
    buffer.close()
    return pdf



"""
Create barcode examples and embed in a PDF
buffer, pageSize
"""
"""
def createBarCodesv1(buffer, data): 

    # Create the pdf object
    c = canvas.Canvas(buffer, pagesize=A4) 
    #barcode_value = ['0004-0000000001', '0004-0000000002','0004-0000000003','0004-0000000004','0004-0000000005',]
    #barcode_value = "1234567890"
    #barcode_value = "0004-0000000001"
    #data = Folder.objects.filter(LessonID=LessonID, codeType=codeType).values('id', 'no', 'codeBarcode').order_by('codeType', 'no')
    barcode_value = [f['codeBarcode'] for f in data]
    print barcode_value 
    #barcode39 = code39.Extended39(barcode_value, humanReadable=True)
    #barcode39Std = code39.Standard39(barcode_value, barHeight=20, stop=1, humanReadable=True)
    # code93 also has an Extended and MultiWidth version
    #barcode93 = code93.Standard93(barcode_value, humanReadable=True)
    #barcode128 = code128.Code128(barcode_value, humanReadable=True)
    # the multiwidth barcode appears to be broken 
    #barcode128Multi = code128.MultiWidthBarcode(barcode_value)
    #barcode_usps = usps.POSTNET("50158-9999")
    #codes = [barcode39, barcode39Std, barcode93, barcode128, barcode_usps]    
    x = 1 * mm
    y = 285 * mm
    x1 = 6.4 * mm

    for value in barcode_value:
        barcode = code39.Extended39(value, humanReadable=True)
        barcode.drawOn(c, x, y)
        y = y - 15 * mm    
    
    c.save()

    # create document
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

"""


#########################################
# Helper PDF - CANVAS Numbered
#Use as doc.build(elements, onFirstPage=self._header_footer, 
# onLaterPages=self._header_footer, canvasmaker=NumberedCanvas)
#########################################
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(211 * mm, 15 * mm + (0.2 * inch),
                             "Page %d of %d" % (self._pageNumber, page_count))
        
#########################################
# PDF Demo 
#########################################
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet

class MyPrint:
    def __init__(self, buffer, pagesize):
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
        self.width, self.height = self.pagesize

    @staticmethod
    def _header_footer(canvas, doc):
        # Save the state of our canvas so we can draw on it
        canvas.saveState()
        styles = getSampleStyleSheet()

        # Header
        header = Paragraph('This is a multi-line header.  It goes on every page.   ' * 5, styles['Normal'])
        w, h = header.wrap(doc.width, doc.topMargin)
        header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

        # Footer
        footer = Paragraph('This is a multi-line footer.  It goes on every page.   ' * 5, styles['Normal'])
        w, h = footer.wrap(doc.width, doc.bottomMargin)
        footer.drawOn(canvas, doc.leftMargin, h)

        # Release the canvas
        canvas.restoreState()

    def print_users(self):
            buffer = self.buffer
            doc = SimpleDocTemplate(buffer,
                                    rightMargin=inch/4,
                                    leftMargin=inch/4,
                                    topMargin=inch/2,
                                    bottomMargin=inch/4,
                                    pagesize=self.pagesize)

            # Our container for 'Flowable' objects
            elements = []

            # A large collection of style sheets pre-made for us
            styles = getSampleStyleSheet()
            styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            users = User.objects.all()
            elements.append(Paragraph('My User Names', styles['Heading1']))
            for i, user in enumerate(users):
                elements.append(Paragraph(user.get_full_name(), styles['Normal']))

            #doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer, canvasmaker=NumberedCanvas)
            doc.build(elements, onFirstPage=self._header_footer, onLaterPages=self._header_footer)

            # Get the value of the BytesIO buffer and write it to the response.
            pdf = buffer.getvalue()
            buffer.close()
            return pdf
    

#########################################
# PDF Demo Class
#########################################
class PdfPrint:

    # initialize class
    def __init__(self, buffer, pageSize):
        self.buffer = buffer
        # default format is A4
        if pageSize == 'A4':
            self.pageSize = A4
        elif pageSize == 'Letter':
            self.pageSize = letter
        self.width, self.height = self.pageSize

    def pageNumber(self, canvas, doc):
        number = canvas.getPageNumber()
        canvas.drawCentredString(100*mm, 15*mm, str(number))

    def title_draw(self, x, y, text):
        chart_title = Label()
        chart_title.x = x
        chart_title.y = y
        chart_title.fontName = 'FreeSansBold'
        chart_title.fontSize = 16
        chart_title.textAnchor = 'middle'
        chart_title.setText(text)
        return chart_title

    def legend_draw(self, labels, chart, **kwargs):
        legend = Legend()
        chart_type = kwargs['type']
        legend.fontName = 'FreeSans'
        legend.fontSize = 13
        legend.strokeColor = None
        if 'x' in kwargs:
            legend.x = kwargs['x']
        if 'y' in kwargs:
            legend.y = kwargs['y']
        legend.alignment = 'right'
        if 'boxAnchor' in kwargs:
            legend.boxAnchor = kwargs['boxAnchor']
        if 'columnMaximum' in kwargs:
            legend.columnMaximum = kwargs['columnMaximum']
        # x-distance between neighbouring swatche\s
        legend.deltax = 0
        lcolors = legendcolors
        if chart_type == 'line':
            lcolors = [colors.red, colors.blue]
        legend.colorNamePairs = zip(lcolors, labels)

        for i, color in enumerate(lcolors):
            if chart_type == 'line':
                chart.lines[i].fillColor = color
            elif chart_type == 'pie':
                chart.slices[i].fillColor = color
            elif chart_type == 'bar':
                chart.bars[i].fillColor = color
        return legend

    def line_chart_draw(self, values, days):
        nr_days = len(days)
        min_temp = min(min(values[0]), min(values[1]))
        d = Drawing(0, 170)
        # draw line chart
        chart = SampleHorizontalLineChart()
        # set width and height
        chart.width = 350
        chart.height = 135
        # set data values
        chart.data = values
        # use(True) or not(False) line between points
        chart.joinedLines = True
        # set font desired
        chart.lineLabels.fontName = 'FreeSans'
        # set color for the plot area border and interior area
        chart.strokeColor = colors.white
        chart.fillColor = colors.lightblue
        # set lines color and width
        chart.lines[0].strokeColor = colors.red
        chart.lines[0].strokeWidth = 2
        chart.lines[1].strokeColor = colors.blue
        chart.lines[1].strokeWidth = 2
        # set symbol for points
        chart.lines.symbol = makeMarker('Square')
        # set format for points from chart
        chart.lineLabelFormat = '%2.0f'
        # for negative axes intersect should be under zero
        chart.categoryAxis.joinAxisMode = 'bottom'
        # set font used for axes
        chart.categoryAxis.labels.fontName = 'FreeSans'
        if nr_days > 7:
            chart.categoryAxis.labels.angle = 45
            chart.categoryAxis.labels.boxAnchor = 'e'
        chart.categoryAxis.categoryNames = days
        # change y axe format
        chart.valueAxis.labelTextFormat = '%2.0f °C'
        chart.valueAxis.valueStep = 10
        if min_temp > 0:
            chart.valueAxis.valueMin = 0
        llabels = ['Max temp', 'Min temp']
        d.add(self.title_draw(250, 180, _('Temperatures statistics')))
        d.add(chart)
        d.add(self.legend_draw(llabels, chart, x=400, y=150, type='line'))
        return d

    def pie_chart_draw(self, values, llabels):
        d = Drawing(10, 150)
        # chart
        pc = Pie()
        pc.x = 0
        pc.y = 50
        # set data
        pc.data = values
        # set labels
        pc.labels = get_percentage(values)
        # set the link line between slice and it's label
        pc.sideLabels = 1
        # set width and color for slices
        pc.slices.strokeWidth = 0
        pc.slices.strokeColor = None
        d.add(self.title_draw(250, 180,
                              _('Precipitation probability statistics')))
        d.add(pc)
        d.add(self.legend_draw(llabels, pc, x=300, y=150, boxAnchor='ne',
                               columnMaximum=12, type='pie'))
        return d

    def vertical_bar_chart_draw(self, values, days, llabels):
        d = Drawing(0, 170)
        #  chart
        bc = VerticalBarChart()
        # set width and height
        bc.height = 125
        bc.width = 470
        # set data
        bc.data = values
        # set distance between bars elements
        bc.barSpacing = 0.5

        # set labels position under the x axe
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        # set name displayed for x axe
        bc.categoryAxis.categoryNames = days

        # set label format for each bar
        bc.barLabelFormat = '%d'
        # set distance between top of bar and it's label
        bc.barLabels.nudge = 7

        # set some charactestics for the Y axe
        bc.valueAxis.labelTextFormat = '%d km/h'
        bc.valueAxis.valueMin = 0

        d.add(self.title_draw(250, 190, _('Wind speed statistics')))
        d.add(bc)
        d.add(self.legend_draw(llabels, bc, x=480, y=165, boxAnchor='ne',
                               columnMaximum=1, type='bar'))
        # d.add(bcl)
        return d

    def report(self, weather_history, title):
        # set some characteristics for pdf document
        doc = SimpleDocTemplate(
            self.buffer,
            rightMargin=72,
            leftMargin=72,
            topMargin=30,
            bottomMargin=72,
            pagesize=self.pageSize)

        # a collection of styles offer by the library
        styles = getSampleStyleSheet()
        # add custom paragraph style
        styles.add(ParagraphStyle(
            name="TableHeader", fontSize=11, alignment=TA_CENTER,
            fontName="FreeSansBold"))
        styles.add(ParagraphStyle(
            name="ParagraphTitle", fontSize=11, alignment=TA_JUSTIFY,
            fontName="FreeSansBold"))
        styles.add(ParagraphStyle(
            name="Justify", alignment=TA_JUSTIFY, fontName="FreeSans"))
        # list used for elements added into document
        data = []
        data.append(Paragraph(title, styles['Title']))
        # insert a blank space
        data.append(Spacer(1, 12))
        table_data = []
        # table header
        table_data.append([
            Paragraph('Date', styles['TableHeader']),
            Paragraph('Town', styles['TableHeader']),
            Paragraph('Max temp', styles['TableHeader']),
            Paragraph('Min temp', styles['TableHeader']),
            Paragraph('Wind speed', styles['TableHeader']),
            Paragraph('Precip', styles['TableHeader']),
            Paragraph('Precip probab', styles['TableHeader'])])
        for wh in weather_history:
            data.append(Paragraph(u'{0}'.format(wh), styles['ParagraphTitle']))
            data.append(Spacer(1, 12))
            data.append(Paragraph(wh.observations, styles['Justify']))
            data.append(Spacer(1, 24))
            # add a row to table
            table_data.append(
                [wh.date,
                 Paragraph(wh.town.name, styles['Justify']),
                 u"{0} °C".format(wh.max_temperature),
                 u"{0} °C".format(wh.min_temperature),
                 u"{0} km/h".format(wh.wind_speed),
                 u"{0} mm".format(wh.precipitation),
                 u"{0} %".format(wh.precipitation_probability)])
        # create table
        wh_table = Table(table_data, colWidths=[doc.width/7.0]*7)
        wh_table.hAlign = 'LEFT'
        wh_table.setStyle(TableStyle(
            [('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
             ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
             ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
             ('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))
        data.append(wh_table)
        data.append(Spacer(1, 48))
        # add line chart
        temperatures, days = get_temperatures(weather_history)
        line_chart = self.line_chart_draw(temperatures, days)
        data.append(line_chart)
        data.append(Spacer(1, 48))
        data.append(Spacer(1, 48))
        # add bar chart
        wind_speed, towns = get_wind_speed(weather_history)
        days = get_str_days()
        bar_chart = self.vertical_bar_chart_draw(wind_speed, days, towns)
        data.append(bar_chart)
        data.append(Spacer(1, 48))
        data.append(Spacer(1, 48))
        # add pie chart
        prec_percentage = precip_prob_sum(weather_history)
        llabels = ['0-20 %', '21-40 %', '41-60 %', '61-80 %', '81-100 %']
        pie_chart = self.pie_chart_draw(prec_percentage, llabels)
        data.append(pie_chart)
        # create document
        doc.build(data, onFirstPage=self.pageNumber,
                  onLaterPages=self.pageNumber)
        pdf = self.buffer.getvalue()
        self.buffer.close()
        return pdf
