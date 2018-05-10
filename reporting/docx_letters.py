#!/usr/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from datetime import date, timedelta
import time
import StringIO
import xlsxwriter
from django.utils.translation import ugettext
from django.db.models import Avg, Sum, Max, Min, Count

from .models import Town, Weather

from personel.models import *
from personel.helpScripts import td2DayHourMin

from django.utils.translation import ugettext_lazy as _



from django.conf import settings
from django.utils.translation import ugettext
from .utils import get_temperatures, get_wind_speed, get_str_days,\
    get_random_colors, precip_prob_sum, get_percentage
legendcolors = get_random_colors(10)


from django.conf import settings
from django.conf.urls.static import static

from personel.models import *



from docx import Document
from docx.shared import Inches

################################################
# HEADER
################################################
"""
def doXlsHeader(workbook, worksheet, lesson=None):
"""
    
#########################################
# DOCX Letters
#########################################
def doDocxTest(dataDB, lesson=None):
    
    #global lesson_col_width    
    #output = StringIO.StringIO()    
    #document = Document(output)
    doc = Document()
    docx_title="TEST_DOCUMENT.docx"
            
    # ---- Cover Letter ----
    #document.add_picture((r'%s/static/images/my-header.png' % (settings.PROJECT_PATH)), width=Inches(4))
    doc.add_paragraph()
    doc.add_paragraph("%s" % date.today().strftime('%B %d, %Y'))
    doc.add_paragraph('Dear Sir or Madam:')
    doc.add_paragraph('We are pleased to help you with your widgets.')
    doc.add_paragraph('Please feel free to contact me for any additional information.')
    doc.add_paragraph('I look forward to assisting you in this project.')
    doc.add_page_break()

    # Prepare document for download        
    # -----------------------------
    output = StringIO.StringIO()
    #output = StringIO()
    doc.save(output)
    length = output.tell()
    output.seek(0)
    
    """
    #Response
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=' + docx_title
    response['Content-Length'] = length
    return response

    """

    # close workbook
    #workbook.close()
    docx_data = output.getvalue()
    return docx_data

#########################################
# DOCX Letters
#########################################
def doDocSchoolCoverLetter(dataDB, lesson=None):
    
    #global lesson_col_width    
    #output = StringIO.StringIO()    
    #document = Document(output)
    doc = Document()

    constGCName=settings.CONST_REPORTS_GCENTER_NAME
    constGCPresdArticle=settings.CONST_REPORTS_GCENTER_PRESIDENT_ARTICLE
    constGCPresdName=settings.CONST_REPORTS_GCENTER_PRESIDENT_NAME
    constGCPresdSurname=settings.CONST_REPORTS_GCENTER_PRESIDENT_SURNAME
    
    #docx_title=u'ΔΙΑΒΙΒΑΣΤΙΚΟ ΣΧΟΛΕΙΩΝ.docx'    
    
    # ---- Cover Letter ----
    #document.add_picture((r'%s/static/images/my-header.png' % (settings.PROJECT_PATH)), width=Inches(4))
    doc.add_paragraph()
    doc.add_paragraph("%s" % date.today().strftime('%B %d, %Y'))

    #logo = settings.STATIC_ROOT + "/static/images/" + "python_logo.png"    
    formatted_time = time.ctime()
    
    #Titles etc
    document.add_heading(u'ΠΡΩΤΟΚΟΛΛΟ ΠΑΡΑΔΟΣΗΣ ΚΑΙ ΠΑΡΑΛΑΒΗΣ', 0)    
    #document.add_heading('Heading, level 1', level=1)    
    #document.add_paragraph('Intense quote', style='IntenseQuote')
    
    #List & Bullet paragaphs
    #document.add_paragraph('first item in unordered list', style='ListBullet')
    #document.add_paragraph('first item in ordered list', style='ListNumber')
    
    #Image
    #document.add_picture('python.jpeg', width=Inches(1.25))


    #Rec.-based data
    row = 0 
    for school in data:
        #StoryDB = []        
        name = school.name
        ddeName = school.ddeName
        #print "%s %s %s %s" %(s.code, s.name, s.ddeCode, s.ddeName)
        #ptext2 = u'<font name="DejaVuSansMono"> Σήμερα %s ημέρα  %s και ώρα %s</font>' %(datetime.now(), datetime.now(), datetime.now())
        text = u'Σήμερα ......... ημέρα ......... και ώρα .........'
        text += u'o/η υπογραφόμενη/oς Πρόεδρος της Επιτροπής του %s' %(constGCName)
        text += u'παρέδωσα στη Δ/νση Δ.Ε. %s' %(ddeName)
        text += u'τα αποκόμματα, των γραπτών δοκιμίων και απουσιών, τις καταστάσεις βαθμολογίας '
        text += u'των μαθητών της Γ΄Τάξης του %s που εξετάστηκαν στο %s.' %(name, constGCName)
        doc.add_paragraph(text)
        
        text = u'Ο αριθμός τους κατά μάθημα και κατεύθυνση φαίνεται στον παρακάτω πίνακα.'
        doc.add_paragraph(text)

        #Make TABLE 
        #table_data = [(u'ΜΑΘΗΜΑ',u'ΤΕΤΡΑΔΙΑ',u'ΑΠΟΥΣΙΕΣ',u'ΜΗΔΕΝΙΣΜΕΝΑ', u'ΣΥΝΟΛΑ', )]

        # Create the table
        #-----------------
        #table = Table(table_data, rowHeights=20)
        table = doc.add_table(rows=1, cols=5)

        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = u'ΜΑΘΗΜΑ'
        hdr_cells[1].text = u'ΤΕΤΡΑΔΙΑ'
        hdr_cells[2].text = u'ΑΠΟΥΣΙΕΣ'
        hdr_cells[3].text = u'ΜΗΔΕΝΙΣΜΕΝΑ'
        hdr_cells[4].text = u'ΣΥΝΟΛΑ'
        
        #Loop RECORDs
        for rec in school.acceptance_set.all():
            # calc partial sum
            #table_data = table_data + [(rec.LessonID.name, rec.books, rec.booksAbscent, rec.booksZero, part_sum)]
            row_cells = table.add_row().cells
            row_cells[0].text = rec.LessonID.name
            row_cells[1].text = str(rec.books)
            row_cells[2].text = str(rec.booksAbscent)
            row_cells[3].text = str(rec.booksZero)            
            part_sum = (rec.books + rec.booksAbscent + rec.booksZero)
            row_cells[4].text = str(part_sum)
                        

        #StoryDB.append(table)

        #TABLE-stories put together
        #Story +=  Story1 + StoryDB #+ Story2 
        doc.add_page_break()
    
    # create document
    #doc.build(Story)
    #pdf = buffer.getvalue()
    #buffer.close()
    #return pdf


    # Prepare document for download        
    # -----------------------------
    output = StringIO.StringIO()
    #output = StringIO()
    doc.save(output)
    length = output.tell()
    output.seek(0)
    
    """
    #Response
    response = HttpResponse(
        output.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = 'attachment; filename=' + docx_title
    response['Content-Length'] = length
    return response

    """


    # close workbook
    #workbook.close()
    docx_data = output.getvalue()
    return docx_data


