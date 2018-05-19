#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from datetime import date, timedelta
import StringIO
import xlsxwriter

from django.conf import settings
#from .settings import STATIC_ROOT
from django.db.models import Avg, Sum, Max, Min, Count
from django.utils.translation import ugettext

from personel.models import *
from personel.helpScripts import td2DayHourMin

from .models import Town, Weather
from .utils import *

#Global report params
title_cellspan='A1:C1'
date_cellspan='G1:I1'
report_title_cellspan='A2:I2'
lesson_title_cellspan='A3:I3'

# Row to start printing data
start_row=4

# column widths
#lessonColWidth = 15
#codeColWidth = 15
observations_col_width = 25
# column widths
afm_col_width = 15
codeColWidth = 15
dateColWidth = 20
lessonColWidth = 25
nameColWidth = 30
numColWidth = 10
strColWidth = 20
snameColWidth = 30
# column widths


def setWorkbookStyles ( workbook ):
    # GLOBAL excel styles
    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })
    cell = workbook.add_format({
        'align': 'left',
        'valign': 'top',
        'text_wrap': True,
        'border': 1
    })
    cell_center = workbook.add_format({
        'align': 'center',
        'valign': 'top',
        'border': 1
    })


# GLOBAL excel styles
def getWorkbookStyles(workbook):
    title_STYLE = workbook.add_format({ 'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})
    header_STYLE = workbook.add_format({'bg_color': '#F7F7F7','color': 'black','align': 'left','valign': 'top','border': 1})
    cell_STYLE = workbook.add_format({'align': 'right','valign': 'top','text_wrap': True,'border': 1})
    cellC_STYLE = workbook.add_format({'align': 'center','valign': 'top','border': 1})
    cellL_STYLE = workbook.add_format({'align': 'left','valign': 'top','text_wrap': True,'border': 1})
    return title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE

"""
Prepares header for workbook 
@The workbook @The Lesson-or all
"""
def doXlsHeader(workbook, worksheet, lesson=None):
    
    #title_cellspan='A1:C1' date_cellspan='G1:I1' report_title_cellspan='A2:I2' lesson_title_cellspan='A3:I3'

    # Get formatters
    topTitle_STYLE = workbook.add_format({ 'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})
    lesson_STYLE = workbook.add_format({ 'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})
    date_STYLE = workbook.add_format({ 'bold': True, 'align': 'left', 'valign': 'vcenter'})
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)


    # Get GC info record
    gcinfo = GradeCenterInfo.getGCInfo(GradeCenterInfo)
    #record.update( name, article,  presidentName, presidentSurname, phone, folderBooks, minFolderBooks, 
    title_text=gcinfo.name
    #constGCPresdArticle=gcinfo.article
    #constGCPresdName=gcinfo.presidentName
    #constGCPresdSurname=gcinfo.presidentSurname
    #date_text =  datetime.now().strftime('%d/%m/%Y %H:%M')
    # Header
    date_text =  datetime.now().strftime('%d/%m/%Y %H:%M')
    #worksheet.merge_range('A1:C1', title_text, cell_STYLE)
    worksheet.write('D1', title_text, topTitle_STYLE)
    #worksheet.merge_range('G1:I1', date_text, cell_STYLE)
    worksheet.write('A1', date_text, date_STYLE)
    
    #Lesson
    lesson_text = ugettext(u"ΟΛΑ ΤΑ ΜΑΘΗΜΑΤΑ")
    if lesson:
        lessonType = Lesson.lexLessonType(lesson, lesson.type)
        #lesson_text = u"ΜΑΘΗΜΑ:" + lesson.name + '(' + lessonType + ')' 
        lesson_text = u"ΜΑΘΗΜΑ:" + lesson.name + '(' + lessonType + ')' if lesson else ugettext(u"ΟΛΑ ΤΑ ΜΑΘΗΜΑΤΑ")
    """
    Ta dw Imerisia-ESPERINA
    #val = data.codeStatus
    val = (Folder.lexCodeStatus(Folder, data.codeStatus))
    worksheet_s.write_string(row, 4, val, cellC_STYLE)
    """
    #title_text = u"{0} {1}".format(ugettext(u"ΧΡΕΩΣΕΙΣ"), lesson_text)    
    #worksheet.merge_range('A3:I3', lesson_text, title_STYLE)
    worksheet.write('D3', lesson_text, lesson_STYLE)
    
    # write header
    return worksheet

#########################################
# XLS ACCEPTANCE
#########################################
def doXlsAcceptance (dataDB, lesson=None):
    
    global lessonColWidth
    
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Acceptance")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    """
    title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE = formatAWorkbook(workbook)
    
    # write title
    lesson_text = reportTitle(lesson)
    title_text = u"{0} {1}".format(ugettext(u"ΠΑΡΑΛΑΒΕΣ"), lesson_text)
    
    # merge cells
    worksheet_s.merge_range('B2:I2', title_text, title)

    #[{'FolderID__no': 1, 'action': 1, 'station': 0, 'countaction': 1, 'GraderID': 46}]
    """
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    #report_title = u"{0} {1}".format(ugettext(u"ΧΡΕΩΣΕΙΣ"), lesson_text)    
    report_title = u"ΠΑΡΑΛΑΒΕΣ ΓΡΑΠΤΩΝ"
    #worksheet_s.merge_range('A2:G2', report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4
    worksheet_s.write(start_row, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Κωδ.Σχολείου"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Επωνυμία"), header_STYLE)
    worksheet_s.write(start_row, 4, ugettext(u"Τύπος"), header_STYLE)
    #worksheet_s.write(4, 4, ugettext(u"Πλήθος Φακέλων"), header_STYLE)
    worksheet_s.write(start_row, 5, ugettext(u"Τετράδια"), header_STYLE)
    worksheet_s.write(start_row, 6, ugettext(u"Απουσίες"), header_STYLE)
    worksheet_s.write(start_row, 7, ugettext(u"Μηδενισμένα"), header_STYLE)
    worksheet_s.write(start_row, 8, ugettext(u"Κατάσταση"), header_STYLE)

    #print dataDB
     
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row + 1 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        val = data.LessonID.name
        worksheet_s.write_string(row, 1, val, cellL_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)

        val = data.SchoolToGradeID.code
        worksheet_s.write_string(row, 2, val, cell_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)

        val = data.SchoolToGradeID.name
        worksheet_s.write_string(row, 3, val, cellL_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)

        val = data.SchoolToGradeID.type
        worksheet_s.write_number(row, 4, val, cell_STYLE)        

        val = data.books
        worksheet_s.write_number(row, 5, val, cell_STYLE)        

        val = data.booksAbscent
        worksheet_s.write_number(row, 6, val, cell_STYLE)        

        val = data.booksZero
        worksheet_s.write_number(row, 7, val, cell_STYLE)        

        val = u'OK' if data.status else u'-'
        worksheet_s.write_string(row, 8, val, cell_STYLE)


    # change column widths
    worksheet_s.set_column('B:B', nameColWidth )  # Lesson column
    worksheet_s.set_column('C:C', codeColWidth )  # Lesson column
    worksheet_s.set_column('D:D', nameColWidth )  # Lesson column
    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data

"""
"""
def doXlsAcceptanceSum (dataDB, lesson=None):
    
    global lessonColWidth
    
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("AcceptanceSum")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    report_title = u"ΠΑΡΑΛΑΒΕΣ (ΣΥΝΟΛΑ)"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4
    worksheet_s.write(start_row, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Τύπος"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Τετράδια"), header_STYLE)
    worksheet_s.write(start_row, 4, ugettext(u"Απουσίες"), header_STYLE)
    worksheet_s.write(start_row, 5, ugettext(u"Μηδεν/να"), header_STYLE)
    #worksheet_s.write(4, 6, ugettext(u"Σύνολο Παραλαβών (OK)"), header_STYLE)
    
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row + 1 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)

        #{'LessonID': 4, 'sumBooks': 662, 'sumBooksAbscent': 1, 'sumBooksZero': 1},

        val = data['LessonID__name']
        worksheet_s.write_string(row, 1, val, cellL_STYLE)        

        val = (Lesson.lexLessonType(Lesson, data['LessonID__type']))
        worksheet_s.write_string(row, 2, val[0:2], cellC_STYLE)        

        val = data['sumBooks']
        worksheet_s.write_number(row, 3, val, cellC_STYLE)        

        val = data['sumBooksAbscent']
        worksheet_s.write_number(row, 4, val, cellC_STYLE)        

        val = data['sumBooksZero']
        worksheet_s.write_number(row, 5, val, cell_STYLE)        


    # change column widths
    worksheet_s.set_column('B:B', lessonColWidth)  # Lesson column
    worksheet_s.set_column('F:F', 10)  # Lesson column

    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


#########################################
# XLS BOOKING
#########################################
def doXlsBooking (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Booking")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΧΡΕΩΣΕΙΣ"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4
    worksheet_s.write(start_row, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Τύπος"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Ημ-νία Ώρα"), header_STYLE)    
    worksheet_s.write(start_row, 4, ugettext(u"Σταθμός"), header_STYLE)
    worksheet_s.write(start_row, 5, ugettext(u"Πράξη"), header_STYLE)
    worksheet_s.write(start_row, 6, ugettext(u"Φάκελος"), header_STYLE)
    worksheet_s.write(start_row, 7, ugettext(u"Βαθμολογήτής"), header_STYLE)
    #worksheet_s.write(4, 3, ugettext(u"Επωνυμία"), header_STYLE)

    # column widths

    #print dataDB     
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row + 1 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        #[{'action': 0, 'station': 0, 'GraderID': 46, 'actionTime': datetime.datetime(2016, 9, 23, 14, 51, 7)},
        val = data.FolderID.LessonID.name
        worksheet_s.write_string(row, 1, val, cellL_STYLE)        
        #if len(val) > lessonColWidth:lesson_col_width = len(val)

        val = (data.FolderID.LessonID.lexLessonType(Lesson,data.FolderID.LessonID.type))[0:4]
        worksheet_s.write_string(row, 2, val, cellL_STYLE)

        val = data.actionTime
        worksheet_s.write(row, 3, val.strftime('%d/%m/%Y %H:%M'), cell_STYLE)

        val = (Booking.lexStationType(Booking, data.station))[0:4]
        worksheet_s.write_string(row, 4, val, cellC_STYLE)

        val = (Booking.lexActionType(Booking, data.action))[0:4]
        worksheet_s.write_string(row, 5, val, cellC_STYLE)        
        
        val = u"Φ(%d)%s" %(data.FolderID.no,\
                Folder.lexCodeType(Folder, data.FolderID.codeType)[1:])
        worksheet_s.write_string(row, 6, val, cellL_STYLE)

        #val = data.GraderID.id
        #orksheet_s.write_number(row, 6, val, cellC_STYLE)                
        #R.FolderID.codeStatus, R.GraderID.LessonID.id, R.GraderID.isgraderC, R.GraderID.LessonID.name, R.GraderID.LessonID.surname
        val = u"%s %s" %(data.GraderID.TeacherID.surname, data.GraderID.TeacherID.name)
        worksheet_s.write_string(row, 7, val, cellL_STYLE)        


        #val = u'OK' if data.status else u'-'
        #worksheet_s.write_string(row, 8, val, cellC_STYLE)

    # change column widths
    worksheet_s.set_column('A:A', numColWidth)  
    worksheet_s.set_column('B:B', 30)  
    worksheet_s.set_column('C:C', numColWidth)  
    worksheet_s.set_column('D:D', dateColWidth)  
    worksheet_s.set_column('E:G', numColWidth)  
    worksheet_s.set_column('H:H', 30) 
    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


#########################################
# XLS GRADER Weekdays COUNT
#########################################
# dataDB is 
def doXlsBookingWeekdaysCount (dataDB, lesson=None):
       
    global lessonColWidth   # used when we use if .. for cell wodth

    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("GraderWeekdaysCount")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    #worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΗΜΕΡΕΣ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΩΝ"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4    
    worksheet_s.write(start_row, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"ΑΦΜ"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Κωδικός"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Επώνυμο"), header_STYLE)
    worksheet_s.write(start_row, 4, ugettext(u"Όνομα"), header_STYLE)
    worksheet_s.write(start_row, 5, ugettext(u"Ημέρες"), header_STYLE)    
    worksheet_s.write(start_row, 6, ugettext(u"TeacherID"), header_STYLE)
    worksheet_s.write(start_row, 7, ugettext(u"GraderID"), header_STYLE)
    """   
    countDict = countDays0(data) 
    for g in countDays0(data).keys().sort(): 
        print countDict[g]['surname'], len(countDict[g]['dates'])
    """   
   
    # add data to the table
    row = 0 
    for idx, tid in enumerate(dataDB.keys()):
        row = start_row + 1 + idx        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        data = dataDB[tid]

        val = data['afm']
        worksheet_s.write_string(row, 1, val, cell_STYLE)                

        val = data['code']
        worksheet_s.write_string(row, 2, val, cell_STYLE)                

        val = data['surname']
        worksheet_s.write_string(row, 3, val, cellL_STYLE)        

        val = data['name']
        worksheet_s.write_string(row, 4, val, cellL_STYLE)                
        
        if data['dates']:
            val =  len(data['dates'])
        else: 
            val =  0

        worksheet_s.write(row, 5, val, cellC_STYLE)   

        val = tid
        worksheet_s.write_string(row, 6, str(val), cell_STYLE)
    
        val = data['GraderID_id']
        worksheet_s.write_string(row, 7, str(val), cell_STYLE)                
        
        #val = data['TotalWeekdays']        
        #worksheet_s.write(row, 5, val, cellC_STYLE)        

    # change column widths
    worksheet_s.set_column('A:A', num_col_width)
    worksheet_s.set_column('B:C', afm_col_width)
    worksheet_s.set_column('D:E', nameColWidth)
    worksheet_s.set_column('F:F', 8)
    #worksheet_s.set_column('F:G', None, None, {'hidden': True})
    worksheet_s.set_column('G:H', None, None, {'hidden': True})

    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


#########################################
# XLS Grader Work GroupBy Weekdays
#########################################
# dataDB is 
def doXlsBookingWeekdaysDetails (dataDB, lesson=None):
    
    global lessonColWidth   # used when we use if .. for cell wodth
    
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("GraderWeekdays")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    #worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΗΜΕΡΕΣ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΩΝ (ΑΝΑΛΥΤΙΚΑ)"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4    
    worksheet_s.write(start_row, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Τύπος"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Ημ-νία"), header_STYLE)    
    worksheet_s.write(start_row, 4, ugettext(u"Επώνυμο"), header_STYLE)
    worksheet_s.write(start_row, 5, ugettext(u"Όνομα"), header_STYLE)
    worksheet_s.write(start_row, 6, ugettext(u"Πράξεις"), header_STYLE)    
    worksheet_s.write(start_row, 7, ugettext(u"Συνολική Διάρκεια"), header_STYLE)   
    #worksheet_s.write(4, 4, ugettext(u"Πλήθος Φακέλων"), header_STYLE)
    #worksheet_s.write(4, 3, ugettext(u"Ειδικ"), header_STYLE)
    #worksheet_s.write(4, 4, ugettext(u"ΑΦΜ"), header_STYLE)
    #worksheet_s.write(4, 5, ugettext(u"Κ.Βαθμ"), header_STYLE)
    #print dataDB
   
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row + 1 + idx        
        #data
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)

        #val = data.LessonID.name
        #val = data['GraderID__LessonID__name']
        val = data['GraderID__LessonID__name']        
        #val = data.GraderID.LessonID.name
        worksheet_s.write_string(row, 1, val, cellL_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cellC_STYLE)        
        
        val = data['GraderID__LessonID__type']
        val = (Lesson.lexLessonType(Lesson,val))[0:4]
        worksheet_s.write_string(row, 2, val, cellC_STYLE)

        val = data['day']
        #val = data.actionTime
        #worksheet_s.write(row, 4, val.strftime('%d/%m/%Y'), cellC_STYLE)        
        worksheet_s.write(row, 3, val, cellC_STYLE)        

        val = data['GraderID__TeacherID__surname']
        #val = data.GraderID.TeacherID.surname
        worksheet_s.write_string(row, 4, val, cellL_STYLE)        

        val = data['GraderID__TeacherID__name']
        #val = data.GraderID.TeacherID.name
        worksheet_s.write_string(row, 5, val, cellL_STYLE)        

        #available=Count('actionTime')).annotate(sumDuration=Sum('actionDuration'))
        #val = data['actionTime']
        val = data['available']
        #val = data.actionTime
        #worksheet_s.write(row, 4, val.strftime('%d/%m/%Y'), cellC_STYLE)        
        worksheet_s.write(row, 6, val, cellC_STYLE)        

        val = data['sumDuration']
        #val = data.sumActionDuration
        if val is None:
            val= u"0Ω-0Λ"
        else:
            #td = datetime.timedelta(0,77) #td.total_seconds()
            #val= u"%00.2fΩ%00.2fΛ" %(val.seconds//3600, (val.seconds//60)%60)
            val= u"%00.fΩ-%00.fΛ" %(val.seconds//3600, (val.seconds//60)%60)
            #val= "Days(%2.2f) hours (%0.2f) minutes (%0.2f)" %(td.days, td.seconds//3600, (td.seconds//60)%60)
        worksheet_s.write_string(row, 7, val, cellC_STYLE)  
        """
        """

    # change column widths
    worksheet_s.set_column('A:A', numColWidth)  
    worksheet_s.set_column('B:B', 30)  
    worksheet_s.set_column('C:C', numColWidth)  
    worksheet_s.set_column('D:D', dateColWidth)  # Lesson column
    worksheet_s.set_column('E:F', nameColWidth)  
    worksheet_s.set_column('G:G', num_col_width)  
    worksheet_s.set_column('H:H', dateColWidth)  


    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data





#########################################
# XLS GRADER Weekdays COUNT
#########################################
# dataDB is 
def doXlsBookingWeekendsCount (dataDB, lesson=None):
    
    global lessonColWidth   # used when we use if .. for cell wodth
    
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("GraderWeekdaysCount")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    #worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΣΑΒΑΤΟΚΥΡΙΑΚΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΩΝ"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4    
    worksheet_s.write(start_row, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"ΑΦΜ"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Κωδικός"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Επώνυμο"), header_STYLE)
    worksheet_s.write(start_row, 4, ugettext(u"Όνομα"), header_STYLE)
    worksheet_s.write(start_row, 5, ugettext(u"Ημέρες"), header_STYLE)    
    worksheet_s.write(start_row, 6, ugettext(u"TeacherID"), header_STYLE)
    worksheet_s.write(start_row, 7, ugettext(u"GraderID"), header_STYLE)
    """   
    countDict = countDays0(data) 
    for g in countDays0(data).keys().sort(): 
        print countDict[g]['surname'], len(countDict[g]['dates'])
    """   
   
    # add data to the table
    row = 0 
    for idx, tid in enumerate(dataDB.keys()):
        row = start_row + 1 + idx        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        data = dataDB[tid]

        val = data['afm']
        worksheet_s.write_string(row, 1, val, cell_STYLE)                

        val = data['code']
        worksheet_s.write_string(row, 2, val, cell_STYLE)                

        val = data['surname']
        worksheet_s.write_string(row, 3, val, cellL_STYLE)        

        val = data['name']
        worksheet_s.write_string(row, 4, val, cellL_STYLE)                
        
        if data['dates']:
            val =  len(data['dates'])
        else: 
            val =  0

        worksheet_s.write(row, 5, val, cellC_STYLE)   

        val = tid
        worksheet_s.write_string(row, 6, str(val), cell_STYLE)
    
        val = data['GraderID_id']
        worksheet_s.write_string(row, 7, str(val), cell_STYLE)                
        
        #val = data['TotalWeekdays']        
        #worksheet_s.write(row, 5, val, cellC_STYLE)        


    # change column widths
    worksheet_s.set_column('A:A', num_col_width)
    worksheet_s.set_column('B:C', afm_col_width)
    worksheet_s.set_column('D:E', nameColWidth)
    worksheet_s.set_column('F:F', 8)
    #worksheet_s.set_column('F:G', None, None, {'hidden': True})
    worksheet_s.set_column('G:H', None, None, {'hidden': True})

    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


#########################################
# XLS Grader Work
#########################################
# dataDB is list of dict values due to annotation of Sum
# Not a list of Objects
def doXlsBookingWeekendsDetails (dataDB, lesson=None):
    
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("GraderWeekendsSum")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΣΑΒΒΑΤΟΚΥΡΙΑΚΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΩΝ (ΑΝΑΛΥΤΙΚΑ)"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)


    # write header
    #start_row=4    
    worksheet_s.write(start_row, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Τύπος"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Ημ-νία"), header_STYLE)    
    worksheet_s.write(start_row, 4, ugettext(u"Επώνυμο"), header_STYLE)
    worksheet_s.write(start_row, 5, ugettext(u"Όνομα"), header_STYLE)
    worksheet_s.write(start_row, 6, ugettext(u"Πράξεις"), header_STYLE)    
    worksheet_s.write(start_row, 7, ugettext(u"Συνολική Διάρκεια"), header_STYLE)   
    #worksheet_s.write(4, 4, ugettext(u"Πλήθος Φακέλων"), header_STYLE)
    #worksheet_s.write(4, 3, ugettext(u"Ειδικ"), header_STYLE)
    #worksheet_s.write(4, 4, ugettext(u"ΑΦΜ"), header_STYLE)
    #worksheet_s.write(4, 5, ugettext(u"Κ.Βαθμ"), header_STYLE)
    #print dataDB

    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row + 1 + idx        
        data
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)


        val = data['GraderID__LessonID__name']        
        worksheet_s.write_string(row, 1, val, cellL_STYLE)        
        
        val = data['GraderID__LessonID__type']
        val = (Lesson.lexLessonType(Lesson,val))[0:4]
        worksheet_s.write_string(row, 2, val, cellC_STYLE)

        val = data['day']
        #val = data.actionTime
        #worksheet_s.write(row, 4, val.strftime('%d/%m/%Y'), cellC_STYLE)        
        worksheet_s.write(row, 3, val, cellC_STYLE)        

        val = data['GraderID__TeacherID__surname']
        #val = data.GraderID.TeacherID.surname
        worksheet_s.write_string(row, 4, val, cellL_STYLE)        

        val = data['GraderID__TeacherID__name']
        #val = data.GraderID.TeacherID.name
        worksheet_s.write_string(row, 5, val, cellL_STYLE)        


        #available=Count('actionTime')).annotate(sumDuration=Sum('actionDuration'))
        #val = data['actionTime']
        val = data['available']
        #val = data.actionTime
        #worksheet_s.write(row, 4, val.strftime('%d/%m/%Y'), cellC_STYLE)        
        worksheet_s.write(row, 6, val, cellC_STYLE)        

        val = data['sumDuration']
        #val = data.sumActionDuration
        if val is None:
            val= u"0Ω-0Λ"
        else:
            #td = datetime.timedelta(0,77) #td.total_seconds()
            #val= u"%00.2fΩ%00.2fΛ" %(val.seconds//3600, (val.seconds//60)%60)
            val= u"%00.fΩ-%00.fΛ" %(val.seconds//3600, (val.seconds//60)%60)
            #val= "Days(%2.2f) hours (%0.2f) minutes (%0.2f)" %(td.days, td.seconds//3600, (td.seconds//60)%60)
        worksheet_s.write_string(row, 7, val, cellC_STYLE)  

        """
        #SOLUTION 2 - VIA FIELD TRANSFORM 
        #val0 = data['sumDuration']
        val = data['SumActionDurationINT']        
        if val is None:
            val= u"(00)ΩΩ (00)ΛΛ"
        else:
            val=str(timedelta(microseconds=val))#[:-7]
            #t0= str(timedelta(microseconds=data['actionDurationINTEGER']))
        """        
        #SOLUTION 1 - VIA DURATION FIELD AS-IS


    # change column widths
    worksheet_s.set_column('A:A', numColWidth)  
    worksheet_s.set_column('B:B', 30)  
    worksheet_s.set_column('C:C', numColWidth)  
    worksheet_s.set_column('D:D', dateColWidth)  # Lesson column
    worksheet_s.set_column('E:F', nameColWidth)  
    worksheet_s.set_column('G:G', num_col_width)  
    worksheet_s.set_column('H:H', dateColWidth)  

    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


#########################################
# XLS Folder
# Fakeloi / Mathima 
#########################################
def doXlsFolder (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Folder")
    
    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΦΑΚΕΛΟΙ"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4    
    worksheet_s.write(start_row, 0, "AA", header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Τύπος"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Φάκελος"), header_STYLE)
    worksheet_s.write(start_row, 4, ugettext(u"Γραπτά"), header_STYLE)
    worksheet_s.write(start_row, 5, ugettext(u"Θέση"), header_STYLE)
    worksheet_s.write(start_row, 6, ugettext(u"Κατάσταση"), header_STYLE)


    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row +1 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)

        val = data.LessonID.name
        worksheet_s.write_string(row, 1, val, cellL_STYLE)        

        val = (Lesson.lexLessonType(Lesson,data.LessonID.type))[0:4]
        worksheet_s.write_string(row, 2, val, cellL_STYLE)

        val = u"Φ(%d)%s" %(data.no,\
                Folder.lexCodeType(Folder, data.codeType)[1:])
        worksheet_s.write_string(row, 3, val, cellL_STYLE)
        
        val = data.books
        worksheet_s.write_number(row, 4, val, cellC_STYLE)

        #val = data.codeLocation
        val = (Folder.lexCodeLocation(Folder, data.codeLocation))[0:4]
        worksheet_s.write_string(row, 5, val, cellC_STYLE)
        
        #val = data.codeStatus
        val = (Folder.lexCodeStatus(Folder, data.codeStatus))[0:4]
        worksheet_s.write_string(row, 6, val, cellC_STYLE)



        #val = u'ΝΑΙ' if data.isgraderC else u'ΟΧΙ'
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cellC_STYLE)        

    # change column widths
    worksheet_s.set_column('A:A', numColWidth)  
    worksheet_s.set_column('B:B', 30)  
    worksheet_s.set_column('C:C', numColWidth)  
    worksheet_s.set_column('D:E', numColWidth)  
    worksheet_s.set_column('F:G', numColWidth)  

    row = row + 1	
    """
    if lesson:
        lessons = [lesson]
    else:
        lessons = Lesson.objects.all()

    dates = Weather.objects.order_by('date').filter(
        lesson=Lesson.objects.first()).values_list('date', flat=True)
    str_dates = []
    """

    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


"""
Folders with DELAYS
"""
def doXlsFolderDelays (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("FolderDelays")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΦΑΚΕΛΟΙ ΠΟΥ ΚΑΘΥΣΤΕΡΟΥΝ-"
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

    # column widths
    lessonColWidth = 15
    strColWidth = 20
    numColWidth = 10
     
    #print dataDB
    # add data to the sheet
    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row +1 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        #val = data['LessonID__name']
        val = data.GraderID.LessonID.name
        worksheet_s.write_string(row, 1, val, cell_STYLE)        
        #if len(val) > lessonColWidth: lesson_col_width = len(val)

        #val = (Folder.lexCodeType(Folder, data['codeType']))
        val = (Folder.lexCodeType(Folder, data.FolderID.codeType))
        worksheet_s.write_string(row, 2, val, cell_STYLE)        

        val = data.FolderID.no
        worksheet_s.write_number(row, 3, val, cellC_STYLE)        

        val = data.FolderID.books
        worksheet_s.write_number(row, 4, val, cellC_STYLE)        
        
        val = (Folder.lexCodeStatus(Folder, data.FolderID.codeStatus))
        worksheet_s.write_string(row, 5, val, cell_STYLE)        
        
        val = (Folder.lexCodeLocation(Folder, data.FolderID.codeLocation))
        worksheet_s.write_string(row, 6, val, cell_STYLE)        

        #R.FolderID.codeStatus, R.GraderID.LessonID.id, R.GraderID.isgraderC, R.GraderID.LessonID.name, R.GraderID.LessonID.surname
        val = data.GraderID.TeacherID.surname
        val = val + " " + data.GraderID.TeacherID.name
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


"""
Folders with Graders NOW
"""
def doXlsFolderHistory (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("FolderHistory")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΙΣΤΟΡΙΚΟ ΦΑΚΕΛΩΝ-"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4    
    worksheet_s.write(start_row, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Τύπος"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Φάκελος "), header_STYLE)
    worksheet_s.write(start_row, 4, ugettext(u"Τετράδια"), header_STYLE)
    worksheet_s.write(start_row, 5, ugettext(u"Κατάσταση"), header_STYLE)
    worksheet_s.write(start_row, 6, ugettext(u"Θέση"), header_STYLE)
    worksheet_s.write(start_row, 7, ugettext(u"Βαθμολογητής-Φ(Α)"), header_STYLE)
    worksheet_s.write(start_row, 8, ugettext(u"Βαθμολογητής-Φ(Β)"), header_STYLE)

    #print dataDB
    # add data to the sheet

    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row +1 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        #val = data.GraderID.LessonID.name
        val = data['f'].LessonID.name
        worksheet_s.write_string(row, 1, val, cellL_STYLE)        
        #if len(val) > lessonColWidth: lesson_col_width = len(val)

        val = (Lesson.lexLessonType(Lesson,data['f'].LessonID.type))[0:4]
        worksheet_s.write_string(row, 2, val, cellL_STYLE)
        #if len(val) > lessonColWidth: lesson_col_width = len(val)

        val = u"Φ(%d)%s" %(data['f'].no,\
                (Folder.lexCodeType(Folder, data['f'].codeType))[1:])
        worksheet_s.write_string(row, 3, val, cellC_STYLE)        

        val = data['f'].books
        worksheet_s.write_number(row, 4, val, cellC_STYLE)        


        val = (Folder.lexCodeStatus(Folder, data['f'].codeStatus))[0:4]
        worksheet_s.write_string(row, 5, val, cellL_STYLE)        
        
        val = (Folder.lexCodeLocation(Folder, data['f'].codeLocation))[0:4]
        worksheet_s.write_string(row, 6, val, cellL_STYLE)        

        #print "F=>", f.id,
        for c_idx, g in enumerate(data['g']):
            val = g.TeacherID.surname+ " " + g.TeacherID.name
            worksheet_s.write_string(row, 7+c_idx, val, cellL_STYLE)        

    # change column widths
    worksheet_s.set_column('B:B', strColWidth) 
    worksheet_s.set_column('C:E', numColWidth) 
    worksheet_s.set_column('F:G', strColWidth) 
    worksheet_s.set_column('H:I', 40) 

    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


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



"""
def doXlsFolderStatus (dataDB, lesson=None):
    pass
"""

def doXlsFolderStatus0 (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("FolderStatus0")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΣΥΝΟΛΑ ΦΑΚΕΛΩΝ"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)
    # write header
    #start_row=4       
    worksheet_s.write(start_row, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Τύπος"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Κατάσταση"), header_STYLE)
    worksheet_s.write(start_row, 4, ugettext(u"Πλήθος"), header_STYLE)
    #worksheet_s.write(start_row, 5, ugettext(u"Θέση"), header_STYLE)

    # column widths
    lessonColWidth = 15
    strColWidth = 20
    numColWidth = 5

    """     
    dataDB = [{'codeType': 0, 'countCodeType': 21, 'LessonID': 4, 'codeStatus': 0}, 
        {'codeType': 0, 'countCodeType': 2, 'LessonID': 4, 'codeStatus': 1}, 
        {'codeType': 1, 'countCodeType': 1, 'LessonID': 4, 'codeStatus': 0}, 
        {'codeType': 1, 'countCodeType': 2, 'LessonID': 4, 'codeStatus': 2}, 
        {'codeType': 2, 'countCodeType': 1, 'LessonID': 4, 'codeStatus': 1}, 
    ]
    """     

    print dataDB

    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row +1 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)

        #[{'countCodeLocation': 4, 'countCodeType': 4, 'codeStatus': 0, 'codeType': 0, 'LessonID': 4, 'countCodeStatus': 4},
        val = data['LessonID__name']
        worksheet_s.write_string(row, 1, val, cell_STYLE)        
        #if len(val) > lessonColWidth: lesson_col_width = len(val)

        val = (Folder.lexCodeType(Folder, data['codeType']))
        #val = data['codeType']
        worksheet_s.write_string(row, 2, val, cell_STYLE)        
        
        val = (Folder.lexCodeStatus(Folder, data['codeStatus']))
        #val = data['codeStatus']
        worksheet_s.write_string(row, 3, val, cell_STYLE)        
        
        # Same value for countCodeType, countCodeStatus, countCodeLocation
        val = data['countCodeType']
        worksheet_s.write_number(row, 4, val, cellC_STYLE)        
        
        #val = data['codeLocation']
        #worksheet_s.write_string(row, 4, val, cell_STYLE)        
        
    # change column widths
    worksheet_s.set_column('B:E', strColWidth) 

    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


"""
"""
def doXlsFolderSum (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("FolderStatus")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΣΥΝΟΛΑ ΦΑΚΕΛΩΝ"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4    
    
    worksheet_s.write(start_row, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Τύπος"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Κατηγορία"), header_STYLE)
    worksheet_s.write(start_row, 4, ugettext(u"Πλήθος"), header_STYLE)
    worksheet_s.write(start_row, 5, ugettext(u"Θέση"), header_STYLE)
    worksheet_s.write(start_row, 6, ugettext(u"Κατάσταση"), header_STYLE)

    #print dataDB
     
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = 5 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)

        #[{'countCodeLocation': 4, 'countCodeType': 4, 'codeStatus': 0, 'codeType': 0, 'LessonID': 4, 'countCodeStatus': 4},
        #val = data.LessonID.name
        val = data['LessonID__name']
        worksheet_s.write_string(row, 1, val, cellL_STYLE)        
        #if len(val) > lessonColWidth: lesson_col_width = len(val)

        val = (Lesson.lexLessonType(Lesson,data['LessonID__type']))[0:4]
        worksheet_s.write_string(row, 2, val, cellL_STYLE)

        val = (Folder.lexCodeType(Folder, data['codeType']))[1:]
        worksheet_s.write_string(row, 3, val, cellC_STYLE)        

        # Same value for countCodeType, countCodeStatus, countCodeLocation
        val = data['countCodeType']
        worksheet_s.write_number(row, 4, val, cellC_STYLE)        
        
        val = (Folder.lexCodeLocation(Folder, data['codeLocation']))[0:4]
        #val = data['codeLocation']
        worksheet_s.write_string(row, 5, val, cellL_STYLE)        
        
        val = (Folder.lexCodeStatus(Folder, data['codeStatus']))[0:4]
        #val = data['codeStatus']
        worksheet_s.write_string(row, 6, val, cellL_STYLE)        
        
        

    # change column widths
    # change column widths
    worksheet_s.set_column('A:A', numColWidth) 
    worksheet_s.set_column('B:B', 30)  
    worksheet_s.set_column('C:C', numColWidth)  
    worksheet_s.set_column('D:E', numColWidth)  
    worksheet_s.set_column('F:G', numColWidth)  

    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data



#########################################
# XLS Grader
#########################################
def doXlsGrader (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Grader")
    
    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΒΑΘΜΟΛΟΓΗΤΕΣ"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4    
    worksheet_s.write(start_row, 0, "AA", header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"Επώνυμο"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Όνομα"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Ειδικ"), header_STYLE)
    worksheet_s.write(start_row, 4, ugettext(u"ΑΦΜ"), header_STYLE)
    worksheet_s.write(start_row, 5, ugettext(u"Κ.Βαθμ"), header_STYLE)
    worksheet_s.write(start_row, 6, ugettext(u"Συντ"), header_STYLE)
    worksheet_s.write(start_row, 7, ugettext(u"ΑναΒαθ"), header_STYLE)
    worksheet_s.write(start_row, 8, ugettext(u"Μάθημα"), header_STYLE)

    # column widths
    lessonColWidth = 15
    codeColWidth = 15
    observations_col_width = 25

    #print dataDB

    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row +1 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        val = data.TeacherID.surname
        worksheet_s.write_string(row, 1, val, cellL_STYLE)
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)
        
        val = data.TeacherID.name
        worksheet_s.write_string(row, 2, val, cellL_STYLE)

        val = data.TeacherID.codeSpec
        worksheet_s.write_string(row, 3, val, cell_STYLE)
        
        val = data.TeacherID.codeGrad
        worksheet_s.write_string(row, 4, val, cellC_STYLE)
        
        val = data.TeacherID.codeAfm
        worksheet_s.write_string(row, 5, val, cellC_STYLE)        
        
        val = u'ΝΑΙ' if data.isCoordinator else u'ΟΧΙ'
        worksheet_s.write_string(row, 6, val, cellC_STYLE)
        
        val = u'ΝΑΙ' if data.isgraderC else u'ΟΧΙ'
        worksheet_s.write_string(row, 7, val, cellC_STYLE)

        val = data.LessonID.name
        valType = Lesson.lexLessonType(data.LessonID, data.LessonID.type)
        val = val + '('+valType+')'
        worksheet_s.write_string(row, 8, val, cell_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cellC_STYLE)        


    # change column widths
    worksheet_s.set_column('B:C', nameColWidth)      # 
    worksheet_s.set_column('D:H', codeColWidth)     # Lesson column
    worksheet_s.set_column('I:I', 20)     # Lesson column
    #worksheet_s.set_column('G:G', 20)  # Lesson column

    row = row + 1
	
    """
    if lesson:
        lessons = [lesson]
    else:
        lessons = Lesson.objects.all()

    dates = Weather.objects.order_by('date').filter(
        lesson=Lesson.objects.first()).values_list('date', flat=True)
    str_dates = []
    """

    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data



#########################################
# XLS Grader Work
#########################################
def doXlsGraderWorkv3 (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("GraderWorkv3")
    
    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΕΙΚΟΝΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΗ"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4    
    worksheet_s.write(start_row, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Επώνυμο"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Όνομα"), header_STYLE)
    worksheet_s.write(start_row, 4, ugettext(u"Φάκελος"), header_STYLE)
    #print dataDB
    
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        #row = start_row + row + 1
        row = start_row +1 + idx
        
        #print g.id, g.LessonID.name, g.TeacherID.surname        
        #countCodeType = if len(b) > 0: b[0].countCodeType else: 0        
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        #val = data.LessonID.name
        val = data['g'].LessonID.name
        worksheet_s.write_string(row, 1, val, cellL_STYLE)        

        val = data['g'].TeacherID.surname
        worksheet_s.write_string(row, 2, val, cellL_STYLE)        

        val = data['g'].TeacherID.name
        worksheet_s.write_string(row, 3, val, cellL_STYLE)        

        for c_idx, b in enumerate(data['bSums']):      #bSums=Action duration sums
            #row = row + 1
            #print "\t", b['FolderID__id'], b['sumAction'], b['wasTypeOf']
            
            #row = row + 1
            #val = u"{0} {1} {2}".format( str(b['FolderID__no']), str(Folder.lexCodeType(Folder, b['wasTypeOf'])), str(b['sumAction']) ) #ugettext(), lesson_text)
            val = u"Φ"+str(b['FolderID__no'])
            #val = val + (Folder.lexCodeType(Folder, b['wasTypeOf']))[1:]            
            totalTime = td2DayHourMin(b['sumAction']) if b['sumAction'] else ""
            val = val + u"("+totalTime+")"
                
            #val = u"{0}-{1} {2}".format( (Folder.lexCodeType(Folder, b['wasTypeOf'])), str(b['FolderID__no']), totalTime ) #ugettext(), lesson_text)
            cellFormat = workbook.add_format()
            if b['wasTypeOf']==0: 
                color='#FF3333'   #red
            elif b['wasTypeOf']==1: 
                color='green' #green
            elif b['wasTypeOf']==2: 
                color='blue'  #blue
            elif b['wasTypeOf']==-1:    #Completed 
                color='brown' 
            else: 
                color='white' 
            #cellFormat.set_font_color(color)
            #cellFormat.set_bold(True)  # Also turns bold on.
            #cellFormat.set_bg_color(color)
            #cellFormat = workbook.add_format({'bold': False, 'font_size': 11, 'bg_color': color,'color': 'black','align': 'left','valign': 'top','text_wrap': True,'border': 1})
            cellFormat = workbook.add_format({'bold': False, 'font_size': 9, 'font_color': color,'color': 'black','align': 'left','valign': 'top','text_wrap': True,'border': 1})
            #worksheet_s.write_string(row, 4+c_idx, val, cellL_STYLE)
            worksheet_s.write_string(row, 4+c_idx, val, cellFormat)
            worksheet_s.set_column(4+c_idx,4+c_idx, 20)  # Lesson column
            
            worksheet_s.write(start_row, 4+c_idx, ugettext(u"Φάκελος")+str(c_idx+1), header_STYLE)

            """
            #val = u"{0}-{1} {2}".format( (Folder.lexCodeType(Folder, b['wasTypeOf'])), str(b['FolderID__no']), totalTime ) #ugettext(), lesson_text)
            val = u"Φ-"+str(b['FolderID__no'])
            worksheet_s.write_string(row, 4+ c_idx*3, val, cellC_STYLE)        

            val = (Folder.lexCodeType(Folder, b['wasTypeOf']))[1:]
            worksheet_s.write_string(row, 5+c_idx*3, val, cellL_STYLE)        

            val= b['sumAction']
            if val:
                worksheet_s.write(row, 6+c_idx*3, td2DayHourMin(val), cellC_STYLE)        
            """
        

        """        
        #print "days (%f:2) hours (%f) minutes (%f)" %(td.days, td.seconds//3600, (td.seconds//60)%60)
        #print "days (%2.2f) hours (%0.2f) minutes (%0.2f)" %(td.days, td.seconds//3600, (td.seconds//60)%60)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cellC_STYLE)        
        """
    # change column widths
    worksheet_s.set_column('B:B', lessonColWidth)  # Lesson column
    worksheet_s.set_column('C:C', snameColWidth)  # Lesson column
    worksheet_s.set_column('D:D', nameColWidth)  # Lesson column
    worksheet_s.set_column('E:E', 15)  # Lesson column

    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data

#########################################
# XLS Grader Work
#########################################
def doXlsGraderWork (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("GraderWorkv2")
    
    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΕΙΚΟΝΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΗ"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4    
    worksheet_s.write(start_row, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Επώνυμο"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Όνομα"), header_STYLE)
    worksheet_s.write(start_row, 4, ugettext(u"Πλήθος Φακέλων"), header_STYLE)
    #worksheet_s.write(4, 3, ugettext(u"Ειδικ"), header_STYLE)
    #worksheet_s.write(4, 4, ugettext(u"ΑΦΜ"), header_STYLE)
    #worksheet_s.write(4, 1, ugettext(u"Σταθμός"), header_STYLE)
    #worksheet_s.write(4, 1, ugettext(u"Πράξη"), header_STYLE)
    #worksheet_s.write(4, 5, ugettext(u"Κ.Βαθμ"), header_STYLE)
    #$worksheet_s.write(4, 6, ugettext(u"Συντ"), header_STYLE)

    # column widths
    #lessonColWidth = 15
    #codeColWidth = 15
    #observations_col_width = 25

    #print dataDB
    
    #[{'FolderID__no': 1, 'action': 1, 'station': 0, 'countaction': 1, 'GraderID': 46}]
    
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row +1 + idx        

        # we get each grader
        #data = Grader.objects..filter(LessonID=LessonID)
        # we must access each grader on Booking Records now 
        g = data
        b = data.booking_set.filter(action=0, station=0)\
                .annotate(countCodeType=Count('id'))
        
        print g.id, g.LessonID.name, g.TeacherID.surname
        
        #countCodeType = if len(b) > 0: b[0].countCodeType else: 0
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        #val = data.LessonID.name
        val = g.LessonID.name
        worksheet_s.write_string(row, 1, val, cellL_STYLE)        

        val = g.TeacherID.surname
        worksheet_s.write_string(row, 2, val, cellL_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cellC_STYLE)        

        val = g.TeacherID.name
        #val = data['GraderID__TeacherID__surname']
        worksheet_s.write_string(row, 3, val, cellL_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cellC_STYLE)        

        #val =  b[0].countCodeType if (len(b)>0) else 0
        val =  len(b) if (len(b)>0) else 0
        #val = data['GraderID__TeacherID__name']
        worksheet_s.write_number(row, 4, val, cellC_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cellC_STYLE)        

        """        
        val = data['countCodeType']
        worksheet_s.write_number(row, 4, val, cellC_STYLE)        
        """


    # change column widths
    worksheet_s.set_column('B:B', lessonColWidth)  # Lesson column
    worksheet_s.set_column('C:C', snameColWidth)  # Lesson column
    worksheet_s.set_column('D:D', nameColWidth)  # Lesson column
    worksheet_s.set_column('E:E', 15)  # Lesson column

    row = row + 1
	
    """
    if lesson:
        lessons = [lesson]
    else:
        lessons = Lesson.objects.all()

    dates = Weather.objects.order_by('date').filter(
        lesson=Lesson.objects.first()).values_list('date', flat=True)
    str_dates = []
    """

    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data



#########################################
# XLS Grader WorkOLD
#########################################
def doXlsGraderWorkOld (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("GraderWork")
    
    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΕΙΚΟΝΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΗ"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4    
    worksheet_s.write(start_row, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(start_row, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(start_row, 2, ugettext(u"Επώνυμο"), header_STYLE)
    worksheet_s.write(start_row, 3, ugettext(u"Όνομα"), header_STYLE)
    worksheet_s.write(start_row, 4, ugettext(u"Πλήθος Φακέλων"), header_STYLE)
    #worksheet_s.write(4, 3, ugettext(u"Ειδικ"), header_STYLE)
    #worksheet_s.write(4, 4, ugettext(u"ΑΦΜ"), header_STYLE)
    #worksheet_s.write(4, 1, ugettext(u"Σταθμός"), header_STYLE)
    #worksheet_s.write(4, 1, ugettext(u"Πράξη"), header_STYLE)
    #worksheet_s.write(4, 5, ugettext(u"Κ.Βαθμ"), header_STYLE)
    #$worksheet_s.write(4, 6, ugettext(u"Συντ"), header_STYLE)

    # column widths
    lessonColWidth = 15
    codeColWidth = 15
    observations_col_width = 25

    #print dataDB
    
    #[{'FolderID__no': 1, 'action': 1, 'station': 0, 'countaction': 1, 'GraderID': 46}]
    
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row +1 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        #val = data.LessonID.name
        #[{'GraderID__TeacherID__surname': u'\u0391\u0398\u0391\u039d\u0391\u03a3\u039f\u03a0\u039f\u03a5\u039b\u039f\u03a5', 'countaction': 1, 'GraderID': 46, 'GraderID__TeacherID__name': u'\u0395\u039b\u0395\u039d\u0397', 'action': 1, 'station': 0, 'FolderID__no': 1}]

        val = data['FolderID__LessonID__name']
        worksheet_s.write_string(row, 1, val, cell_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cellC_STYLE)        

        val = data['GraderID__TeacherID__surname']
        worksheet_s.write_string(row, 2, val, cell_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cellC_STYLE)        

        val = data['GraderID__TeacherID__name']
        worksheet_s.write_string(row, 3, val, cell_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cellC_STYLE)        

        
        val = data['FolderID__no']
        worksheet_s.write_number(row, 4, val, cellC_STYLE)        


    # change column widths
    worksheet_s.set_column('B:B', lessonColWidth)  # Lesson column

    row = row + 1
	
    """
    if lesson:
        lessons = [lesson]
    else:
        lessons = Lesson.objects.all()

    dates = Weather.objects.order_by('date').filter(
        lesson=Lesson.objects.first()).values_list('date', flat=True)
    str_dates = []
    """

    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


#########################################
# XLS Grader WorkDay
#########################################
def doXlsGraderWorkDay (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("GraderWorkDay")
 
    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΕΙΚΟΝΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΗ"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4    
    
    worksheet_s.write(4, 0, ugettext(u"AA"), header_STYLE)
    worksheet_s.write(4, 1, ugettext(u"Μάθημα"), header_STYLE)
    worksheet_s.write(4, 2, ugettext(u"Επώνυμο"), header_STYLE)
    worksheet_s.write(4, 3, ugettext(u"Όνομα"), header_STYLE)
    worksheet_s.write(4, 4, ugettext(u"Σταθμός"), header_STYLE)
    worksheet_s.write(4, 5, ugettext(u"Πράξη"), header_STYLE)
    worksheet_s.write(4, 6, ugettext(u"Ημ-νία"), header_STYLE)

    #print dataDB
        
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row +1 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        val = data['FolderID__LessonID__name']
        worksheet_s.write_string(row, 1, val, cell_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)

        val = data['GraderID__TeacherID__surname']
        worksheet_s.write_string(row, 2, val, cell_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cellC_STYLE)        

        val = data['GraderID__TeacherID__name']
        worksheet_s.write_string(row, 3, val, cell_STYLE)        
        #if len(val) > lessonColWidth:
        #    lessonColWidth = len(val)

        
        val = data['station']
        worksheet_s.write_number(row, 4, val, cellC_STYLE)        

        val = data['action']
        worksheet_s.write_number(row, 5, val, cellC_STYLE)        

        val = data['actionTime']
        worksheet_s.write(row, 6, val.strftime('%d/%m/%Y'), cellC_STYLE)        


    # change column widths
    worksheet_s.set_column('B:D', lessonColWidth)  # Lesson column
    worksheet_s.set_column('G:G', dateColWidth)  # Lesson column

    row = row + 1
	
    """
    if lesson:
        lessons = [lesson]
    else:
        lessons = Lesson.objects.all()

    dates = Weather.objects.order_by('date').filter(
        lesson=Lesson.objects.first()).values_list('date', flat=True)
    str_dates = []
    """

    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data



#########################################
# XLS TOTAL
#########################################
def doXlsTotal (dataDB, lesson=None):
    
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Total")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    # Report title
    report_title = u"ΣΥΝΟΛΑ"
    #worksheet_s.merge_range(report_title_cellspan, report_title, title_STYLE)
    worksheet_s.write('D2', report_title, title_STYLE)

    # write header
    #start_row=4    

    #print dataDB
     
    # add data to the table
    row = 0 
    """
    #val = u'OK' if data.status else u'-'
    #worksheet_s.write_string(row, 8, val, cellC_STYLE)
    """
    # change column widths
    worksheet_s.set_column('B:B', lessonColWidth)

    # Creating the pie chart
    pie_chart = workbook.add_chart({'type': 'pie'})

    # add more Sheets
    worksheet_c = workbook.add_worksheet("Charts")
    worksheet_d = workbook.add_worksheet("Chart Data")

    # creating data for pie chart
    pie_values = []
    """
    pie_values.append(Weather.objects.filter(max_temperature__lte=20,
                                             max_temperature__gte=10).count())
    """
    #valuesCodeLocation = Folder.objects.filter(LessonID=4).values('codeType', 'LessonID', 'codeStatus').annotate(countStatus=Count('codeStatus')).order_by('codeType')    
    #valuesCodeStatus = Folder.objects.filter(LessonID=4).values('codeType', 'LessonID', 'codeStatus').annotate(countStatus=Count('codeStatus')).order_by('codeType') 
    valuesCodeStatus = Folder.objects.filter(LessonID=4).values('codeStatus').annotate(countStatus=Count('codeStatus'))\
            #.order_by('codeType') 
    print valuesCodeStatus 
    val = valuesCodeStatus.values()
    
    pie_values.append(Folder.objects.filter(codeLocation=0).count())
    pie_values.append(Folder.objects.filter(codeLocation=1).count())
    pie_values.append(Folder.objects.filter(codeLocation=2).count())
    
    #pie_values.append(Weather.objects.filter(max_temperature__lte=20,
    """
    pie_values2 = [{'countCodeLocation': 4, 'countCodeType': 4, 'codeLocation': 0, 'codeStatus': 0, 'codeType': 0, 'LessonID': 4, 'countCodeStatus': 4},
        {'countCodeLocation': 1, 'countCodeType': 1, 'codeLocation': 0, 'codeStatus': 1, 'codeType': 0, 'LessonID': 4, 'countCodeStatus': 1},
        {'countCodeLocation': 5, 'countCodeType': 5, 'codeLocation': 0, 'codeStatus': 0, 'codeType': 1, 'LessonID': 4, 'countCodeStatus': 5},
        {'countCodeLocation': 5, 'countCodeType': 5, 'codeLocation': 0, 'codeStatus': 0, 'codeType': 0, 'LessonID': 5, 'countCodeStatus': 5},
        {'countCodeLocation': 1, 'countCodeType': 1, 'codeLocation': 0, 'codeStatus': 0, 'codeType': 1, 'LessonID': 5, 'countCodeStatus': 1},
    ]
    
    pie_categories = ["T >18", "10 < T < 18", "T < 10"]
    """
    pie_categories = [u"ΑΠΟΘΗΚΗ", u"ΒΑΘΜΟΛΟΓΗΤΕΣ", u"ΦΥΛΑΞΗ", ]
    print pie_categories 
    
    #pie_values = [16, 2, 3]
    print pie_values
    
    """
    Folder.objects.all().values('codeStatus', 'codeType', 'LessonID')\
            .annotate(countCodeType=Count('codeType'), countCodeStatus=Count('codeStatus'), countCodeLocation=Count('codeLocation'))\
            .order_by('LessonID','codeType')

    #[{'countCodeLocation': 4, 'countCodeStatus': 4, 'countCodeType': 4, 'codeStatus': 0, 'codeType': 0, 'LessonID': 4 },


    # KATASTASH ΦΑΚΕΛΩΝ GIA TO ΜΑΘΗΜΑ (aka POREIA DIORTHOSIS)
    records = Folder.objects.filter(LessonID=4).values('codeType', 'LessonID', 'codeStatus').annotate(countStatus=Count('codeStatus')).order_by('codeType')
    [R for R in records]
        
    {'codeStatus': 0, 'countStatus': 4, 'LessonID': 4, 'codeType': 0}
    {'codeStatus': 1, 'countStatus': 1, 'LessonID': 4, 'codeType': 0}
    {'codeStatus': 0, 'countStatus': 5, 'LessonID': 4, 'codeType': 1}

    """

    # adding the data to "Chart Data" Sheet
    cell_index = 0
    cell_index = cell_index + 4
    
    worksheet_d.write_column("{0}1".format(chr(ord('A') + cell_index)),
                             pie_values)
    worksheet_d.write_column("{0}1".format(chr(ord('A') + cell_index + 1)),
                             pie_categories)

    worksheet_s.write_column("{0}1".format(chr(ord('A') + cell_index)),
                             pie_values)
    worksheet_s.write_column("{0}1".format(chr(ord('A') + cell_index + 1)),
                             pie_categories)


    # adding the data to the chart
    pie_chart.add_series({
        #'name': ugettext(u'ΘΕΣΗ ΦΑΚΕΛΩΝ (Στατιστικά)'),
        'name': ugettext(u'ΘΕΣΗ ΦΑΚΕΛΩΝ'),
        'values': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index), 1, 3),
        'categories': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index + 1), 1, 3),
        'data_labels': {'percentage': True}
    })
    """
    """
    # insert the chart on "Charts" Sheet
    #worksheet_c.insert_chart('A1', pie_chart)
    
    # >>>>>>>>> worksheet_s
    worksheet_s.insert_chart('A1', pie_chart)


    # STATUS pie chart 
    pie_chart_status = workbook.add_chart({'type': 'pie'})
    
    pie_values_Status = []
    pie_values_Status_Labels = []
    #for loc in [0,1,2,3,4,5,8]: 
    for st in range (0,7):
        pie_values_Status.append(Folder.objects.filter(codeStatus=st).count())    
        pie_values_Status_Labels.append(Folder.STATUS_TYPE[st][1])
        print st, Folder.STATUS_TYPE[st][1]

    # adding the data to "Chart Data" Sheet
    cell_index = 10
    cell_index = cell_index + 4
    
    worksheet_s.write_column("{0}1".format(chr(ord('A') + cell_index)),
                             pie_values_Status)
    worksheet_s.write_column("{0}1".format(chr(ord('A') + cell_index + 1)),
                             pie_values_Status_Labels)

    worksheet_d.write_column("{0}1".format(chr(ord('A') + cell_index)),
                             pie_values_Status)
    worksheet_d.write_column("{0}1".format(chr(ord('A') + cell_index + 1)),
                             pie_values_Status_Labels)

    # adding the data to the chart
    pie_chart_status.add_series({
        #'name': ugettext(u'ΚΑΤΑΣΤΑΣΗ ΦΑΚΕΛΩΝ (Στατιστικά)'),
        'name': ugettext(u'ΚΑΤΑΣΤΑΣΗ ΦΑΚΕΛΩΝ'),
        'values': '=Chart Data!${0}${1}:${0}${2}'.format(chr(ord('A') + cell_index), 1, 8),
        'categories': '=Chart Data!${0}${1}:${0}${2}'.format(chr(ord('A') + cell_index + 1), 1, 8),
        'data_labels': {'percentage': True}
    })    
    # >>>>>>>>> worksheet_s
    worksheet_s.insert_chart('G1', pie_chart_status)


    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


#########################################
# XLS VAR
#########################################
def WriteToExcel(weather_data, town=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("Summary")

    # write title
    if town:
        town_text = town.name
    else:
        town_text = ugettext("all recorded towns")
    title_text = u"{0} {1}".format(ugettext("Weather History for"), town_text)
    # merge cells
    worksheet_s.merge_range('B2:I2', title_text, title)

    # write header
    worksheet_s.write(4, 0, ugettext("No"), header_STYLE)
    worksheet_s.write(4, 1, ugettext("Town"), header_STYLE)
    worksheet_s.write(4, 2, ugettext("Date"), header_STYLE)
    worksheet_s.write(4, 3, ugettext("Description"), header_STYLE)
    worksheet_s.write(4, 4, ugettext(u"Max T. (℃)"), header_STYLE)
    worksheet_s.write(4, 5, ugettext(u"Min T. (℃)"), header_STYLE)
    worksheet_s.write(4, 6, ugettext("Wind (km/h)"), header_STYLE)
    worksheet_s.write(4, 7, ugettext("Precip. (mm)"), header_STYLE)
    worksheet_s.write(4, 8, ugettext("Precip. (%)"), header_STYLE)
    worksheet_s.write(4, 9, ugettext("Observations"), header_STYLE)

    # column widths
    town_col_width = 10
    description_col_width = 10
    observations_col_width = 25

    # add data to the table
    for idx, data in enumerate(weather_data):
        row = 5 + idx
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)

        worksheet_s.write_string(row, 1, data.town.name, cell_STYLE)
        if len(data.town.name) > town_col_width:
            town_col_width = len(data.town.name)

        worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cellC_STYLE)
        worksheet_s.write_string(row, 3, data.description, cell_STYLE)
        if len(data.description) > description_col_width:
            description_col_width = len(data.description)

        worksheet_s.write_number(row, 4, data.max_temperature, cellC_STYLE)
        worksheet_s.write_number(row, 5, data.min_temperature, cellC_STYLE)
        worksheet_s.write_number(row, 6, data.wind_speed, cellC_STYLE)
        worksheet_s.write_number(row, 7, data.precipitation, cellC_STYLE)
        worksheet_s.write_number(row, 8, data.precipitation_probability, cellC_STYLE)

        observations = data.observations.replace('\r', '')
        worksheet_s.write_string(row, 9, observations, cell_STYLE)
        observations_rows = compute_rows(observations, observations_col_width)
        worksheet_s.set_row(row, 15 * observations_rows)

    # change column widths
    worksheet_s.set_column('B:B', town_col_width)  # Town column
    worksheet_s.set_column('C:C', 11)  # Date column
    worksheet_s.set_column('D:D', description_col_width)  # Description column
    worksheet_s.set_column('E:E', 10)  # Max Temp column
    worksheet_s.set_column('F:F', 10)  # Min Temp column
    worksheet_s.set_column('G:G', 10)  # Wind Speed column
    worksheet_s.set_column('H:H', 11)  # Precipitation column
    worksheet_s.set_column('I:I', 11)  # Precipitation % column
    worksheet_s.set_column('J:J', observations_col_width)  # Observations column

    row = row + 1
    # Adding some functions for the data
    max_temp_avg = Weather.objects.all().aggregate(Avg('max_temperature'))
    worksheet_s.write_formula(row, 4,
                              '=average({0}{1}:{0}{2})'.format('E', 6, row),
                              cell_center,
                              max_temp_avg['max_temperature__avg'])
    min_temp_avg = Weather.objects.all().aggregate(Avg('min_temperature'))
    worksheet_s.write_formula(row, 5,
                              '=average({0}{1}:{0}{2})'.format('F', 6, row),
                              cell_center,
                              min_temp_avg['min_temperature__avg'])
    wind_avg = Weather.objects.all().aggregate(Avg('wind_speed'))
    worksheet_s.write_formula(row, 6,
                              '=average({0}{1}:{0}{2})'.format('G', 6, row),
                              cell_center,
                              wind_avg['wind_speed__avg'])
    precip_sum = Weather.objects.all().aggregate(Sum('precipitation'))
    worksheet_s.write_formula(row, 7,
                              '=sum({0}{1}:{0}{2})'.format('H', 6, row),
                              cell_center,
                              precip_sum['precipitation__sum'])
    precip_prob_avg = Weather.objects.all() \
        .aggregate(Avg('precipitation_probability'))
    worksheet_s.write_formula(row, 8,
                              '=average({0}{1}:{0}{2})'.format('I', 6, row),
                              cell_center,
                              precip_prob_avg['precipitation_probability__avg'])

    # add more Sheets
    worksheet_c = workbook.add_worksheet("Charts")
    worksheet_d = workbook.add_worksheet("Chart Data")

    if town:
        towns = [town]
    else:
        towns = Town.objects.all()

    # Creating the Line Chart
    line_chart = workbook.add_chart({'type': 'line'})
    # adding dates for the values
    dates = Weather.objects.order_by('date').filter(
        town=Town.objects.first()).values_list('date', flat=True)
    str_dates = []
    for d in dates:
        str_dates.append(d.strftime('%d/%m/%Y'))
    worksheet_d.write_column('A1', str_dates)
    worksheet_d.set_column('A:A', 10)

    # add data for the line chart
    for idx, t in enumerate(towns):
        data = Weather.objects.order_by('date').filter(town=t)
        letter_max_t = chr(ord('B') + idx)
        letter_min_t = chr(ord('B') + idx + len(towns))
        worksheet_d.write_column(
            "{0}1".format(letter_max_t),
            data.values_list('max_temperature', flat=True))
        worksheet_d.write_column(
            "{0}1".format(letter_min_t),
            data.values_list('min_temperature', flat=True))

        # add data to line chart series
        line_chart.add_series({
            'categories': '=Chart Data!$A1:$A${0}'.format(len(dates)),
            'values': '=Chart Data!${0}${1}:${0}${2}'
            .format(letter_max_t, 1, len(data)),
            'marker': {'type': 'square'},
            'name': u"{0} {1}".format(ugettext("Max T."), t.name)
        })
        line_chart.add_series({
            'categories': '=Chart Data!$A1:$A${0}'.format(len(dates)),
            'values': '=Chart Data!${0}${1}:${0}${2}'
            .format(letter_min_t, 1, len(data)),
            'marker': {'type': 'circle'},
            'name': u"{0} {1}".format(ugettext("Min T."), t.name)
        })
    # adding other options
    line_chart.set_title({'name': ugettext("Maximum and Minimum Temperatures")})
    line_chart.set_x_axis({
        'text_axis': True,
        'date_axis': False
    })
    line_chart.set_y_axis({
        'num_format': u'## ℃'
    })
    # Insert Chart to "Charts" Sheet
    worksheet_c.insert_chart('B2', line_chart, {'x_scale': 2, 'y_scale': 1})

    # Creating the column chart
    bar_chart = workbook.add_chart({'type': 'column'})

    # creating data for column chart
    cell_index = len(towns) * 2 + 2
    for idx, t in enumerate(towns):
        max_wind = Weather.objects.filter(town=t).aggregate(Max('wind_speed'))
        min_wind = Weather.objects.filter(town=t).aggregate(Min('wind_speed'))
        worksheet_d.write_string(idx, cell_index, t.name)
        worksheet_d.write_number(
            idx, cell_index + 1, max_wind['wind_speed__max'])
        worksheet_d.write_number(
            idx, cell_index + 2, min_wind['wind_speed__min'])

    # add series
    bar_chart.add_series({
        'name': 'Max Speed',
        'values': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index + 1), 1, len(towns)),
        'categories': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index), 1, len(towns)),
        'data_labels': {'value': True, 'num_format': u'#0 "km/h"'}
    })
    bar_chart.add_series({
        'name': 'Min Speed',
        'values': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index + 2), 1, len(towns)),
        'categories': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index), 1, len(towns)),
        'data_labels': {'value': True, 'num_format': u'#0 "km/h"'}
    })
    # adding other options
    bar_chart.set_title({'name': ugettext("Maximum and minimum wind speeds")})

    worksheet_c.insert_chart('B20', bar_chart, {'x_scale': 1, 'y_scale': 1})

    # Creating the pie chart
    pie_chart = workbook.add_chart({'type': 'pie'})

    # creating data for pie chart
    pie_values = []
    pie_values.append(Weather.objects.filter(max_temperature__gt=20).count())
    pie_values.append(Weather.objects.filter(max_temperature__lte=20,
                                             max_temperature__gte=10).count())
    pie_values.append(Weather.objects.filter(max_temperature__lt=10).count())
    pie_categories = ["T >18", "10 < T < 18", "T < 10"]

    # adding the data to "Chart Data" Sheet
    cell_index = cell_index + 4
    worksheet_d.write_column("{0}1".format(chr(ord('A') + cell_index)),
                             pie_values)
    worksheet_d.write_column("{0}1".format(chr(ord('A') + cell_index + 1)),
                             pie_categories)

    # adding the data to the chart
    pie_chart.add_series({
        'name': ugettext('Temperature statistics'),
        'values': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index), 1, 3),
        'categories': '=Chart Data!${0}${1}:${0}${2}'
        .format(chr(ord('A') + cell_index + 1), 1, 3),
        'data_labels': {'percentage': True}
    })

    # insert the chart on "Charts" Sheet
    worksheet_c.insert_chart('J20', pie_chart)

    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


def compute_rows(text, width):
    if len(text) < width:
        return 1
    phrases = text.replace('\r', '').split('\n')

    rows = 0
    for phrase in phrases:
        if len(phrase) < width:
            rows = rows + 1
        else:
            words = phrase.split(' ')
            temp = ''
            for idx, word in enumerate(words):
                temp = temp + word + ' '
                # check if column width exceeded
                if len(temp) > width:
                    rows = rows + 1
                    temp = '' + word + ' '
                # check if it is not the last word
                if idx == len(words) - 1 and len(temp) > 0:
                    rows = rows + 1
    return rows
