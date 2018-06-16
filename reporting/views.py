#!/usr/bin/python
# -*- coding: utf-8 -*-

#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from datetime import date, timedelta
import time
import StringIO
import xlsxwriter

from django.db.models import Avg, Sum, Max, Min, Count
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.shortcuts import render
from django.utils.translation import ugettext, ugettext_lazy as _


from docx import Document
from docx.shared import Inches, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH

from personel.models import *
from personel.helpScripts import td2DayHourMin

from .utils import *
#from .utils import get_temperatures, get_wind_speed, get_str_days, get_random_colors, precip_prob_sum, get_percentage, legendcolors = get_random_colors(10)


#############################################
# Fakeloi pou diorthonontai twra!
#############################################
def htmlFolderNow(request, LessonID=None):
    
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
        bookings=f.booking_set.filter(action=0).order_by('-actionTime').distinct()
        dataObj.append({'f':f, 'b':bookings[0],});
    #print data    

    #response = HttpResponse(content_type='application/vnd.ms-excel')
    #response['Content-Disposition'] = 'attachment; filename=FolderNow.xlsx'
    #xlsx_data = doXlsFolderNow(dataObj, lesson)
    #response.write(xlsx_data)
   
    html = render(request, 'reporting/html-folders-now.html', {'data': dataObj, 'lesson': lesson, "msg":"Hello"})
    #html = render(request, 'reporting/html-folders-now.html', {'data': 'Foo', "msg":"Hello"})
    return HttpResponse(html)
   

#########################################
#ΕΙΚΟΝΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΗ
#########################################
def htmlGraderWorkv3(request, LessonID=None):
    
    LessonID = request.GET.get('LessonID', None)
    #LessonID = 11
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
    print data


    #return render_template("clever_template", clever_function=lambda x: clever_function x)
    html = render(request, 'reporting/html-grader-work-v3.html', {'data': dataObj, 'lesson': lesson, "msg":"Hello"})

    #html = render(request, 'reporting/html-folders-now.html', {'data': 'Foo', "msg":"Hello"})
    return HttpResponse(html)


"""
Folders with Graders NOW
"""
def doXlsFolderNow (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("FolderNow")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΦΑΚΕΛΟΙ ΠΟΥ ΔΙΟΡΘΩΝΟΝΤΑΙ ΤΩΡΑ-"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4    
    worksheet_s.write(4, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(4, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(4, 2, ugettext(u"Τύπος"), header_STYLE)
    worksheet_s.write(4, 3, ugettext(u"Φάκελος "), header_STYLE)
    worksheet_s.write(4, 4, ugettext(u"Τετράδια"), header_STYLE)
    worksheet_s.write(4, 5, ugettext(u"Κατάσταση"), header_STYLE)
    worksheet_s.write(4, 6, ugettext(u"Θέση"), header_STYLE)
    worksheet_s.write(4, 7, ugettext(u"Βαθμολογητής"), header_STYLE)

    #print dataDB
    # add data to the sheet

    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row +1 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        #val = str(data['f'].codeType)
        #val = data.GraderID.LessonID.name
        val = data['b'].GraderID.LessonID.name
        worksheet_s.write_string(row, 1, val, cell_STYLE)        
        #if len(val) > lessonColWidth: lesson_col_width = len(val)

        val = (Folder.lexCodeType(Folder, data['f'].codeType))
        worksheet_s.write_string(row, 2, val, cell_STYLE)        
        
        val = data['f'].no
        worksheet_s.write_number(row, 3, val, cellC_STYLE)        

        val = data['f'].books
        worksheet_s.write_number(row, 4, val, cellC_STYLE)        
        
        val = (Folder.lexCodeStatus(Folder, data['f'].codeStatus))
        worksheet_s.write_string(row, 5, val, cell_STYLE)        
        
        val = (Folder.lexCodeLocation(Folder, data['f'].codeLocation))
        worksheet_s.write_string(row, 6, val, cell_STYLE)        

        #R.FolderID.codeStatus, R.GraderID.LessonID.id, R.GraderID.isgraderC, R.GraderID.LessonID.name, R.GraderID.LessonID.surname
        val = data['b'].GraderID.TeacherID.surname
        val = val + " " + data['b'].GraderID.TeacherID.name
        worksheet_s.write_string(row, 7, val, cellC_STYLE)        


    # change column widths
    worksheet_s.set_column('B:B', strColWidth) 
    worksheet_s.set_column('C:E', numColWidth) 
    worksheet_s.set_column('F:G', strColWidth) 
    worksheet_s.set_column('H:H', 40) 

    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data




