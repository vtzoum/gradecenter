#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import StringIO
import xlsxwriter
from django.utils.translation import ugettext
from django.db.models import Avg, Sum, Max, Min, Count

from .models import Town, Weather

from personel.models import *

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
    header_STYLE = workbook.add_format({'bg_color': '#F7F7F7','color': 'black','align': 'center','valign': 'top','border': 1})
    cell_STYLE = workbook.add_format({'align': 'right','valign': 'top','text_wrap': True,'border': 1})
    cellC_STYLE = workbook.add_format({'align': 'center','valign': 'top','border': 1})
    cellL_STYLE = workbook.add_format({'align': 'left','valign': 'top','text_wrap': True,'border': 1})
    return title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE

"""
"""
def xlsTitle(lesson=None):
    # write title
    if lesson:
        lesson_text = lesson.name        
    else:
        lesson_text = ugettext(u"Όλα τα Μαθήματα")
    return lesson_text

"""
Prepares header for workbook 
@The workbook @The Lesson-or all
"""
def doXlsHeader(workbook, worksheet, lesson=None):
    
    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    
    # Header
    title_text =  u"43ο ΒΚ ΑΙΤ/ΝΙΑΣ (ΑΓΡΙΝΙΟ)"
    date_text =  datetime.now().strftime('%d/%m/%Y %H:%M')
    worksheet.write(0, 0, title_text, cell_STYLE)
    worksheet.write(0, 6, date_text, cell_STYLE)
    #worksheet.merge_range('G1:I1', date_text, cell_STYLE)

    # Lesson title
    lesson_text = "ΜΑΘΗΜΑ:" + lesson.name if lesson else ugettext(u"ΟΛΑ ΤΑ ΜΑΘΗΜΑΤΑ")
    #title_text = u"{0} {1}".format(ugettext(u"ΧΡΕΩΣΕΙΣ"), lesson_text)    
    worksheet.merge_range('A2:G2', lesson_text, title_STYLE)
    
    # write header
    return worksheet

#########################################
# XLS ACCEPTANCE
#########################################
def doXlsAcceptance (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("GraderWork")

    # Get formatters
    (title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE) = getWorkbookStyles(workbook)
    """
    title_STYLE, header_STYLE, cell_STYLE, cellC_STYLE, cellL_STYLE = formatAWorkbook(workbook)
    
    # write title
    lesson_text = xlsTitle(lesson)
    title_text = u"{0} {1}".format(ugettext(u"ΠΑΡΑΛΑΒΕΣ"), lesson_text)
    
    # merge cells
    worksheet_s.merge_range('B2:I2', title_text, title)

    #[{'FolderID__no': 1, 'action': 1, 'station': 0, 'countaction': 1, 'GraderID': 46}]
    """
    worksheet_s = doXlsHeader(workbook, worksheet_s, lesson)
    
    #report_title = u"{0} {1}".format(ugettext(u"ΧΡΕΩΣΕΙΣ"), lesson_text)    
    report_title = u"ΧΡΕΩΣΕΙΣ"
    worksheet_s.merge_range('A3:G3', report_title, title_STYLE)

    # write header
    start_row=4
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

    # column widths
    lesson_col_width = 15
    code_col_width = 15
    observations_col_width = 25

    #print dataDB
     
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = start_row + 1 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        val = data.LessonID.name
        worksheet_s.write_string(row, 1, val, cell_STYLE)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)

        val = data.SchoolToGradeID.code
        worksheet_s.write_string(row, 2, val, cell_STYLE)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)

        val = data.SchoolToGradeID.name
        worksheet_s.write_string(row, 3, val, cell_STYLE)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)

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
    worksheet_s.set_column('B:B', lesson_col_width)  # Lesson column

    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data

"""
"""
def doXlsAcceptanceSum (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("GraderWork")


    title, header, cell, cell_center = formatAWorkbook(workbook)
    
    # write title
    lesson_text = xlsTitle(lesson)
    title_text = u"{0} {1}".format(ugettext(u"ΠΑΡΑΛΑΒΕΣ (ΣΥΝΟΛΑ)"), lesson_text)
    
    # merge cells
    worksheet_s.merge_range('B2:I2', title_text, title)


    # write header
    worksheet_s.write(4, 0, ugettext(u"AA"), header)
    worksheet_s.write(4, 1, ugettext(u"Μάθημα"), header)
    worksheet_s.write(4, 2, ugettext(u"Σύνολο Τετραδίων"), header)
    #worksheet_s.write(4, 4, ugettext(u"Πλήθος Φακέλων"), header)
    worksheet_s.write(4, 3, ugettext(u"Σύνολο Απουσιών"), header)
    worksheet_s.write(4, 4, ugettext(u"Σύνολο Μηδενισμένων"), header)
    worksheet_s.write(4, 5, ugettext(u"Κατάσταση"), header)
    #worksheet_s.write(4, 6, ugettext(u"Σύνολο Παραλαβών (OK)"), header)

    # column widths
    lesson_col_width = 15
    code_col_width = 15
    observations_col_width = 25

    print dataDB
     
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = 5 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cell_center)

        #{'LessonID': 4, 'sumBooks': 662, 'sumBooksAbscent': 1, 'sumBooksZero': 1},

        val = data['LessonID__name']
        worksheet_s.write_string(row, 1, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)

        val = data['sumBooks']
        worksheet_s.write_number(row, 2, val, cell_center)        

        val = data['sumBooksAbscent']
        worksheet_s.write_number(row, 3, val, cell_center)        

        val = data['sumBooksZero']
        worksheet_s.write_number(row, 4, val, cell)        


    # change column widths
    worksheet_s.set_column('B:B', lesson_col_width)  # Lesson column

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
    title, header, cell, cell_center = formatAWorkbook(workbook)
    # write title
    lesson_text = xlsTitle(lesson)
    title_text = u"{0} {1}".format(ugettext(u"ΧΡΕΩΣΕΙΣ"), lesson_text)    
    worksheet_s.merge_range('A2:G2', title_text, title)
    # Headers
    worksheet_s.write(0, 3, u"43ο ΒΚ ΑΙΤ/ΝΙΑΣ (ΑΓΡΙΝΙΟ)", cell_center)
    worksheet_s.write(0, 6, datetime.now().strftime('%d/%m/%Y %H:%M'), cell_center)

    #[{'action': 0, 'station': 0, 'GraderID': 46, 'actionTime': datetime.datetime(2016, 9, 23, 14, 51, 7)},

    # write header
    worksheet_s.write(4, 0, ugettext(u"AA"), header)
    worksheet_s.write(4, 1, ugettext(u"Μάθημα"), header)
    worksheet_s.write(4, 2, ugettext(u"Σταθμός"), header)
    worksheet_s.write(4, 3, ugettext(u"Πράξη"), header)
    worksheet_s.write(4, 4, ugettext(u"Ημ-νία Ώρα"), header)
    worksheet_s.write(4, 5, ugettext(u"Φακ"), header)
    worksheet_s.write(4, 6, ugettext(u"Βαθμολογήτής"), header)
    #worksheet_s.write(4, 3, ugettext(u"Επωνυμία"), header)

    # column widths
    lesson_col_width = 15
    namesColWidth = 30
    numberColWidth = 10
    stringColWidth = 20

    #print dataDB
     
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = 5 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cell_center)
        
        #[{'action': 0, 'station': 0, 'GraderID': 46, 'actionTime': datetime.datetime(2016, 9, 23, 14, 51, 7)},
        val = data.FolderID.LessonID.name
        worksheet_s.write_string(row, 1, val, cell)        
        #if len(val) > lesson_col_width:
        #    lesson_col_width = len(val)

        #val = data.station
        val = (Booking.lexStationType(Booking, data.station))
        worksheet_s.write_string(row, 2, val, cell)

        val = (Booking.lexActionType(Booking, data.action))
        worksheet_s.write_string(row, 3, val, cell)        
        
        val = data.actionTime
        worksheet_s.write(row, 4, val.strftime('%d/%m/%Y %H:%M'), cell_center)        

        val = data.FolderID.no
        #val = data.FolderID.id
        worksheet_s.write_number(row, 5, val, cell_center)        

        #val = data.GraderID.id
        #orksheet_s.write_number(row, 6, val, cell_center)        
        
        #R.FolderID.codeStatus, R.GraderID.LessonID.id, R.GraderID.isgraderC, R.GraderID.LessonID.name, R.GraderID.LessonID.surname
        val = data.GraderID.TeacherID.surname
        val = val + " " + data.GraderID.TeacherID.name
        worksheet_s.write_string(row, 6, val, cell_center)        


        #val = u'OK' if data.status else u'-'
        #worksheet_s.write_string(row, 8, val, cell_center)

    # change column widths
    worksheet_s.set_column('B:E', stringColWidth)  # Lesson column
    worksheet_s.set_column('F:F', numberColWidth)  # Lesson column
    worksheet_s.set_column('G:G', namesColWidth)  # Lesson column

    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


#########################################
# XLS Grader Work GroupBy Weekdays
#########################################
# dataDB is 
def doXlsBookingWeekdays (dataDB, lesson=None):
    
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("GraderWeekdays")


    #Get formatters
    title, header, cell, cell_center = formatAWorkbook(workbook)    
    # write title
    lesson_text = xlsTitle(lesson)
    title_text = u"{0} {1}".format(ugettext(u"ΗΜΕΡΕΣ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΩΝ ΑΝΑ ΗΜΕΡΑ-"), lesson_text)   
    worksheet_s.merge_range('A2:H2', title_text, title)
    
    # write header
    worksheet_s.write(4, 0, ugettext(u"AA"), header)
    worksheet_s.write(4, 1, ugettext(u"Ημ-νία"), header)    
    worksheet_s.write(4, 2, ugettext(u"Μάθημα"), header)
    worksheet_s.write(4, 3, ugettext(u"Επώνυμο"), header)
    worksheet_s.write(4, 4, ugettext(u"Όνομα"), header)
    worksheet_s.write(4, 5, ugettext(u"Πράξεις"), header)    
    worksheet_s.write(4, 6, ugettext(u"Διάρκεια"), header)
    
    #worksheet_s.write(4, 4, ugettext(u"Πλήθος Φακέλων"), header)
    #worksheet_s.write(4, 3, ugettext(u"Ειδικ"), header)
    #worksheet_s.write(4, 4, ugettext(u"ΑΦΜ"), header)
    #worksheet_s.write(4, 5, ugettext(u"Κ.Βαθμ"), header)

    # column widths
    code_col_width = 15
    date_col_width = 15
    lesson_col_width = 15

    #print dataDB
   
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = 5 + idx        
        data
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cell_center)

        val = data['day']
        #val = data.actionTime
        #worksheet_s.write(row, 4, val.strftime('%d/%m/%Y'), cell_center)        
        worksheet_s.write(row, 1, val, cell_center)        

        #val = data.LessonID.name
        #val = data['GraderID__LessonID__name']
        val = data['GraderID__LessonID__name']        
        #val = data.GraderID.LessonID.name
        worksheet_s.write_string(row, 2, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)        
        
        val = data['GraderID__TeacherID__surname']
        #val = data.GraderID.TeacherID.surname
        worksheet_s.write_string(row, 3, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)        

        val = data['GraderID__TeacherID__name']
        #val = data.GraderID.TeacherID.name
        worksheet_s.write_string(row, 4, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)        
        

        #available=Count('actionTime')).annotate(sumDuration=Sum('actionDuration'))
        #val = data['actionTime']
        val = data['available']
        #val = data.actionTime
        #worksheet_s.write(row, 4, val.strftime('%d/%m/%Y'), cell_center)        
        worksheet_s.write(row, 5, val, cell_center)        

        val = data['sumDuration']
        #val = data.sumActionDuration
        if val is None:
            val= u"(00)ΩΩ (00)ΛΛ"
        else:
            #td = datetime.timedelta(0,77) #td.total_seconds()
            val= u"(%00.2f)ΩΩ (%00.2f)ΛΛ" %(val.seconds//3600, (val.seconds//60)%60)
            #val= "Days(%2.2f) hours (%0.2f) minutes (%0.2f)" %(td.days, td.seconds//3600, (td.seconds//60)%60)
        worksheet_s.write_string(row, 6, val)        
        """
        """

    # change column widths
    worksheet_s.set_column('B:F', lesson_col_width)  # Lesson column
    worksheet_s.set_column('G:G', 20)  # Lesson column

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
def doXlsBookingWeekendsSum (dataDB, lesson=None):
    
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("GraderWeekendsSum")


    #Get formatters
    title, header, cell, cell_center = formatAWorkbook(workbook)    
    # write title
    lesson_text = xlsTitle(lesson)
    title_text = u"{0} {1}".format(ugettext(u"ΣΑΒΒΑΤΟΚΥΡΙΑΚΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΩΝ -"), lesson_text)   
    worksheet_s.merge_range('A2:H2', title_text, title)
    
    # write header
    worksheet_s.write(4, 0, ugettext(u"AA"), header)
    worksheet_s.write(4, 1, ugettext(u"Ημ-νία"), header)    
    worksheet_s.write(4, 2, ugettext(u"Μάθημα"), header)
    worksheet_s.write(4, 3, ugettext(u"Επώνυμο"), header)
    worksheet_s.write(4, 4, ugettext(u"Όνομα"), header)
    worksheet_s.write(4, 5, ugettext(u"Πράξεις"), header)    
    worksheet_s.write(4, 6, ugettext(u"Διάρκεια"), header)
    
    #worksheet_s.write(4, 4, ugettext(u"Πλήθος Φακέλων"), header)
    #worksheet_s.write(4, 3, ugettext(u"Ειδικ"), header)
    #worksheet_s.write(4, 4, ugettext(u"ΑΦΜ"), header)
    #worksheet_s.write(4, 5, ugettext(u"Κ.Βαθμ"), header)

    # column widths
    code_col_width = 15
    date_col_width = 15
    lesson_col_width = 15

    #print dataDB
   
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = 5 + idx        
        data
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cell_center)

        val = data['day']
        #val = data.actionTime
        #worksheet_s.write(row, 4, val.strftime('%d/%m/%Y'), cell_center)        
        worksheet_s.write(row, 1, val, cell_center)        

        #val = data.LessonID.name
        #val = data['GraderID__LessonID__name']
        val = data['GraderID__LessonID__name']        
        #val = data.GraderID.LessonID.name
        worksheet_s.write_string(row, 2, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)        
        
        val = data['GraderID__TeacherID__surname']
        #val = data.GraderID.TeacherID.surname
        worksheet_s.write_string(row, 3, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)        

        val = data['GraderID__TeacherID__name']
        #val = data.GraderID.TeacherID.name
        worksheet_s.write_string(row, 4, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)        
        

        #available=Count('actionTime')).annotate(sumDuration=Sum('actionDuration'))
        #val = data['actionTime']
        val = data['available']
        #val = data.actionTime
        #worksheet_s.write(row, 4, val.strftime('%d/%m/%Y'), cell_center)        
        worksheet_s.write(row, 5, val, cell_center)        

        val = data['sumDuration']
        #val = data.sumActionDuration
        if val is None:
            val= u"(00)ΩΩ (00)ΛΛ"
        else:
            #td = datetime.timedelta(0,77) #td.total_seconds()
            val= u"(%00.2f)ΩΩ (%00.2f)ΛΛ" %(val.seconds//3600, (val.seconds//60)%60)
            #val= "Days(%2.2f) hours (%0.2f) minutes (%0.2f)" %(td.days, td.seconds//3600, (td.seconds//60)%60)
        worksheet_s.write_string(row, 6, val)        
        """
        """

    # change column widths
    worksheet_s.set_column('B:F', lesson_col_width)  # Lesson column
    worksheet_s.set_column('G:G', 20)  # Lesson column

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
    
    #Get formatters
    title, header, cell, cell_center = formatAWorkbook(workbook)        
    # write title
    lesson_text = xlsTitle(lesson)
    title_text = u"{0} {1}".format(ugettext(u"ΦΑΚΕΛΟΙ"), lesson_text)
    # merge cells
    worksheet_s.merge_range('B2:I2', title_text, title)

    # write header
    worksheet_s.write(4, 0, "AA", header)
    worksheet_s.write(4, 1, ugettext(u"Μάθημα"), header)
    worksheet_s.write(4, 2, ugettext(u"Κωδικός"), header)
    worksheet_s.write(4, 3, ugettext(u"Τύπος"), header)
    worksheet_s.write(4, 4, ugettext(u"Κατάσταση"), header)
    worksheet_s.write(4, 5, ugettext(u"Θέση"), header)
    worksheet_s.write(4, 6, ugettext(u"Τετράδια"), header)


    # column widths
    lesson_col_width = 15
    code_col_width = 15
    observations_col_width = 25
    stringColWidth = 20
    numberColWidth = 5

    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = 5 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cell_center)
        
        val = data.LessonID.name
        worksheet_s.write_string(row, 1, val, cell)        
        
        val = data.no
        worksheet_s.write_number(row, 2, val, cell)
                
        val = (Folder.lexCodeType(Folder, data.codeType))
        worksheet_s.write_string(row, 3, val, cell)
        
        #val = data.codeStatus
        val = (Folder.lexCodeStatus(Folder, data.codeStatus))
        worksheet_s.write_string(row, 4, val, cell_center)

        #val = data.codeLocation
        val = (Folder.lexCodeLocation(Folder, data.codeLocation))
        worksheet_s.write_string(row, 5, val, cell_center)

        val = data.books
        worksheet_s.write_number(row, 6, val, cell)

        #val = u'ΝΑΙ' if data.isgraderC else u'ΟΧΙ'
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)        

    # change column widths
    worksheet_s.set_column('B:F', stringColWidth)  
    worksheet_s.set_column('C:C', numberColWidth)  

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


    #Get formatters
    title, header, cell, cell_center = formatAWorkbook(workbook)    
    # write title
    lesson_text = xlsTitle(lesson)
    title_text = u"{0} {1}".format(ugettext(u"ΦΑΚΕΛΟΙ ΠΟΥ ΚΑΘΥΣΤΕΡΟΥΝ-"), lesson_text)   
    worksheet_s.merge_range('A2:H2', title_text, title)

    # write header
    worksheet_s.write(4, 0, ugettext(u"AA"), header)
    worksheet_s.write(4, 1, ugettext(u"Μάθημα"), header)
    worksheet_s.write(4, 2, ugettext(u"Τύπος"), header)
    worksheet_s.write(4, 3, ugettext(u"Φάκελος "), header)
    worksheet_s.write(4, 4, ugettext(u"Τετράδια"), header)
    worksheet_s.write(4, 5, ugettext(u"Κατάσταση"), header)
    worksheet_s.write(4, 6, ugettext(u"Θέση"), header)
    worksheet_s.write(4, 7, ugettext(u"Βαθμολογητής"), header)

    # column widths
    lesson_col_width = 15
    stringColWidth = 20
    numberColWidth = 10
     
    #print dataDB
    # add data to the sheet
    row = 0 
    for idx, data in enumerate(dataDB):
        row = 5 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cell_center)
        
        #val = data['LessonID__name']
        val = data.GraderID.LessonID.name
        worksheet_s.write_string(row, 1, val, cell)        
        #if len(val) > lesson_col_width: lesson_col_width = len(val)

        #val = (Folder.lexCodeType(Folder, data['codeType']))
        val = (Folder.lexCodeType(Folder, data.FolderID.codeType))
        worksheet_s.write_string(row, 2, val, cell)        

        val = data.FolderID.no
        worksheet_s.write_number(row, 3, val, cell_center)        

        val = data.FolderID.books
        worksheet_s.write_number(row, 4, val, cell_center)        
        
        val = (Folder.lexCodeStatus(Folder, data.FolderID.codeStatus))
        worksheet_s.write_string(row, 5, val, cell)        
        
        val = (Folder.lexCodeLocation(Folder, data.FolderID.codeLocation))
        worksheet_s.write_string(row, 6, val, cell)        

        #R.FolderID.codeStatus, R.GraderID.LessonID.id, R.GraderID.isgraderC, R.GraderID.LessonID.name, R.GraderID.LessonID.surname
        val = data.GraderID.TeacherID.surname
        val = val + " " + data.GraderID.TeacherID.name
        worksheet_s.write_string(row, 7, val, cell_center)        


    # change column widths
    worksheet_s.set_column('B:B', stringColWidth) 
    worksheet_s.set_column('C:E', numberColWidth) 
    worksheet_s.set_column('F:G', stringColWidth) 
    worksheet_s.set_column('H:H', 40) 

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


    #Get formatters
    title, header, cell, cell_center = formatAWorkbook(workbook)    
    # write title
    lesson_text = xlsTitle(lesson)
    title_text = u"{0} {1}".format(ugettext(u"ΦΑΚΕΛΟΙ ΠΟΥ ΔΙΟΡΘΩΝΟΝΤΑΙ ΤΩΡΑ-"), lesson_text)   
    # merge cells
    worksheet_s.merge_range('A2:H2', title_text, title)

    # write header
    worksheet_s.write(4, 0, ugettext(u"AA"), header)
    worksheet_s.write(4, 1, ugettext(u"Μάθημα"), header)
    worksheet_s.write(4, 2, ugettext(u"Τύπος"), header)
    worksheet_s.write(4, 3, ugettext(u"Φάκελος "), header)
    worksheet_s.write(4, 4, ugettext(u"Τετράδια"), header)
    worksheet_s.write(4, 5, ugettext(u"Κατάσταση"), header)
    worksheet_s.write(4, 6, ugettext(u"Θέση"), header)
    worksheet_s.write(4, 7, ugettext(u"Βαθμολογητής"), header)

    # column widths
    lesson_col_width = 15
    stringColWidth = 20
    numberColWidth = 10
     
    #print dataDB
    # add data to the sheet
    row = 0 
    for idx, data in enumerate(dataDB):
        row = 5 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cell_center)
        
        #val = data['LessonID__name']
        val = data.GraderID.LessonID.name
        worksheet_s.write_string(row, 1, val, cell)        
        #if len(val) > lesson_col_width: lesson_col_width = len(val)

        #val = (Folder.lexCodeType(Folder, data['codeType']))
        val = (Folder.lexCodeType(Folder, data.FolderID.codeType))
        worksheet_s.write_string(row, 2, val, cell)        

        val = data.FolderID.no
        worksheet_s.write_number(row, 3, val, cell_center)        

        val = data.FolderID.books
        worksheet_s.write_number(row, 4, val, cell_center)        
        
        val = (Folder.lexCodeStatus(Folder, data.FolderID.codeStatus))
        worksheet_s.write_string(row, 5, val, cell)        
        
        val = (Folder.lexCodeLocation(Folder, data.FolderID.codeLocation))
        worksheet_s.write_string(row, 6, val, cell)        

        #R.FolderID.codeStatus, R.GraderID.LessonID.id, R.GraderID.isgraderC, R.GraderID.LessonID.name, R.GraderID.LessonID.surname
        val = data.GraderID.TeacherID.surname
        val = val + " " + data.GraderID.TeacherID.name
        worksheet_s.write_string(row, 7, val, cell_center)        


    # change column widths
    worksheet_s.set_column('B:B', stringColWidth) 
    worksheet_s.set_column('C:E', numberColWidth) 
    worksheet_s.set_column('F:G', stringColWidth) 
    worksheet_s.set_column('H:H', 40) 

    row = row + 1
	
    # close workbook
    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data



"""
"""
def doXlsFolderStatus (dataDB, lesson=None):
    pass

def doXlsFolderStatus0 (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("FolderStatus0")

    title, header, cell, cell_center = formatAWorkbook(workbook)
    
    # write title
    lesson_text = xlsTitle(lesson)
    title_text = u"{0} {1}".format(ugettext(u"ΣΥΝΟΛΑ ΦΑΚΕΛΩΝ"), lesson_text)
    
    # merge cells
    worksheet_s.merge_range('A2:F2', title_text, title)

    # write header
    worksheet_s.write(4, 0, ugettext(u"AA"), header)
    #worksheet_s.write(4, 1, ugettext(u"Μάθημα"), header)
    worksheet_s.write(4, 2, ugettext(u"Τύπος"), header)
    worksheet_s.write(4, 3, ugettext(u"Κατάσταση"), header)
    #worksheet_s.write(4, 4, ugettext(u"Θέση"), header)
    worksheet_s.write(4, 5, ugettext(u"Πλήθος"), header)

    # column widths
    lesson_col_width = 15
    stringColWidth = 20
    numberColWidth = 5

     
    dataDB = [{'codeType': 0, 'countCodeType': 21, 'LessonID': 4, 'codeStatus': 0}, 
        {'codeType': 0, 'countCodeType': 2, 'LessonID': 4, 'codeStatus': 1}, 
        {'codeType': 1, 'countCodeType': 1, 'LessonID': 4, 'codeStatus': 0}, 
        {'codeType': 1, 'countCodeType': 2, 'LessonID': 4, 'codeStatus': 2}, 
        {'codeType': 2, 'countCodeType': 1, 'LessonID': 4, 'codeStatus': 1}, 
    ]

    #print dataDB

    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = 5 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cell_center)

        #[{'countCodeLocation': 4, 'countCodeType': 4, 'codeStatus': 0, 'codeType': 0, 'LessonID': 4, 'countCodeStatus': 4},
        #val = data['LessonID__name']
        val = 'LessonID__name'
        worksheet_s.write_string(row, 1, val, cell)        
        #if len(val) > lesson_col_width: lesson_col_width = len(val)

        val = (Folder.lexCodeType(Folder, data['codeType']))
        #val = data['codeType']
        worksheet_s.write_string(row, 2, val, cell)        
        
        val = (Folder.lexCodeStatus(Folder, data['codeStatus']))
        #val = data['codeStatus']
        worksheet_s.write_string(row, 3, val, cell)        
        
        val = 'Foo'
        #val = data['codeLocation']
        worksheet_s.write_string(row, 4, val, cell)        
        
        # Same value for countCodeType, countCodeStatus, countCodeLocation
        val = data['countCodeType']
        worksheet_s.write_number(row, 5, val, cell_center)        
        
    # change column widths
    worksheet_s.set_column('B:E', stringColWidth) 

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

    title, header, cell, cell_center = formatAWorkbook(workbook)
    
    # write title
    lesson_text = xlsTitle(lesson)
    title_text = u"{0} {1}".format(ugettext(u"ΣΥΝΟΛΑ ΦΑΚΕΛΩΝ"), lesson_text)
    
    # merge cells
    worksheet_s.merge_range('A2:F2', title_text, title)

    # write header
    worksheet_s.write(4, 0, ugettext(u"AA"), header)
    worksheet_s.write(4, 1, ugettext(u"Μάθημα"), header)
    worksheet_s.write(4, 2, ugettext(u"Τύπος"), header)
    worksheet_s.write(4, 3, ugettext(u"Κατάσταση"), header)
    worksheet_s.write(4, 4, ugettext(u"Θέση"), header)
    worksheet_s.write(4, 5, ugettext(u"Πλήθος"), header)

    # column widths
    lesson_col_width = 15
    stringColWidth = 20
    numberColWidth = 5

    #print dataDB
     
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = 5 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cell_center)

        #[{'countCodeLocation': 4, 'countCodeType': 4, 'codeStatus': 0, 'codeType': 0, 'LessonID': 4, 'countCodeStatus': 4},
        val = data['LessonID__name']
        worksheet_s.write_string(row, 1, val, cell)        
        #if len(val) > lesson_col_width: lesson_col_width = len(val)

        val = (Folder.lexCodeType(Folder, data['codeType']))
        #val = data['codeType']
        worksheet_s.write_string(row, 2, val, cell)        
        
        val = (Folder.lexCodeStatus(Folder, data['codeStatus']))
        #val = data['codeStatus']
        worksheet_s.write_string(row, 3, val, cell)        
        
        val = (Folder.lexCodeLocation(Folder, data['codeLocation']))
        #val = data['codeLocation']
        worksheet_s.write_string(row, 4, val, cell)        
        
        # Same value for countCodeType, countCodeStatus, countCodeLocation
        val = data['countCodeType']
        worksheet_s.write_number(row, 5, val, cell_center)        
        
    # change column widths
    worksheet_s.set_column('B:E', stringColWidth) 

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
    
    # GLOBAL excel styles
    title = workbook.add_format({ 'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})
    header = workbook.add_format({'bg_color': '#F7F7F7','color': 'black','align': 'center','valign': 'top','border': 1})
    cell = workbook.add_format({'align': 'left','valign': 'top','text_wrap': True,'border': 1})
    cell_center = workbook.add_format({'align': 'center','valign': 'top','border': 1})

    # write title
    if lesson:
        lesson_text = lesson.name        
    else:
        lesson_text = ugettext(u"Όλα τα Μαθήματα")
    #print lesson_text

    title_text = u"{0} {1}".format(ugettext(u"ΒΑΘΜΟΛΟΓΗΤΕΣ"), lesson_text)
    # merge cells
    worksheet_s.merge_range('B2:I2', title_text, title)

    # write header
    worksheet_s.write(4, 0, "AA", header)
    worksheet_s.write(4, 1, ugettext(u"Επώνυμο"), header)
    worksheet_s.write(4, 1, ugettext(u"Επώνυμο"), header)
    worksheet_s.write(4, 2, ugettext(u"Όνομα"), header)
    worksheet_s.write(4, 3, ugettext(u"Ειδικ"), header)
    worksheet_s.write(4, 4, ugettext(u"ΑΦΜ"), header)
    worksheet_s.write(4, 5, ugettext(u"Κ.Βαθμ"), header)
    worksheet_s.write(4, 6, ugettext(u"Συντ"), header)
    worksheet_s.write(4, 7, ugettext(u"ΑναΒαθ"), header)
    worksheet_s.write(4, 8, ugettext(u"Μάθημα"), header)

    # column widths
    lesson_col_width = 15
    code_col_width = 15
    observations_col_width = 25

    #print dataDB

    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = 5 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cell_center)
        
        val = data.TeacherID.surname
        worksheet_s.write_string(row, 1, val, cell)
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)
        
        val = data.TeacherID.name
        worksheet_s.write_string(row, 2, val, cell)
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)

        val = data.TeacherID.codeSpec
        worksheet_s.write_string(row, 3, val, cell)
        
        val = data.TeacherID.codeGrad
        worksheet_s.write_string(row, 4, val, cell_center)
        
        val = data.TeacherID.codeAfm
        worksheet_s.write_string(row, 5, val, cell_center)        
        
        val = u'ΝΑΙ' if data.isCoordinator else u'ΟΧΙ'
        worksheet_s.write_string(row, 6, val, cell_center)
        
        val = u'ΝΑΙ' if data.isgraderC else u'ΟΧΙ'
        worksheet_s.write_string(row, 7, val, cell_center)

        val = data.LessonID.name
        worksheet_s.write_string(row, 8, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)        


    # change column widths
    worksheet_s.set_column('B:B', lesson_col_width)  # Lesson column

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
def doXlsGraderWork (dataDB, lesson=None):
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet_s = workbook.add_worksheet("GraderWork")
    
    # GLOBAL excel styles
    title = workbook.add_format({ 'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})
    header = workbook.add_format({'bg_color': '#F7F7F7','color': 'black','align': 'center','valign': 'top','border': 1})
    cell = workbook.add_format({'align': 'left','valign': 'top','text_wrap': True,'border': 1})
    cell_center = workbook.add_format({'align': 'center','valign': 'top','border': 1})
    
    """
    # write title
    if lesson:
        lesson_text = lesson.name        
    else:
        lesson_text = ugettext(u"Όλα τα Μαθήματα")
    print lesson_text
    title_text = u"{0} {1}".format(ugettext(u"ΕΙΚΟΝΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΗ"), lesson_text)
    """

    title_text = u"{0} {1}".format(ugettext(u"ΕΙΚΟΝΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΗ"), '')
    # merge cells
    worksheet_s.merge_range('B2:I2', title_text, title)

    #[{'FolderID__no': 1, 'action': 1, 'station': 0, 'countaction': 1, 'GraderID': 46}]

    # write header
    worksheet_s.write(4, 0, ugettext(u"AA"), header)
    worksheet_s.write(4, 1, ugettext(u"Μάθημα"), header)
    worksheet_s.write(4, 2, ugettext(u"Επώνυμο"), header)
    worksheet_s.write(4, 3, ugettext(u"Όνομα"), header)
    worksheet_s.write(4, 4, ugettext(u"Πλήθος Φακέλων"), header)
    #worksheet_s.write(4, 3, ugettext(u"Ειδικ"), header)
    #worksheet_s.write(4, 4, ugettext(u"ΑΦΜ"), header)
    #worksheet_s.write(4, 1, ugettext(u"Σταθμός"), header)
    #worksheet_s.write(4, 1, ugettext(u"Πράξη"), header)
    #worksheet_s.write(4, 5, ugettext(u"Κ.Βαθμ"), header)
    #$worksheet_s.write(4, 6, ugettext(u"Συντ"), header)

    # column widths
    lesson_col_width = 15
    code_col_width = 15
    observations_col_width = 25

    #print dataDB
    
    #[{'FolderID__no': 1, 'action': 1, 'station': 0, 'countaction': 1, 'GraderID': 46}]
    
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = 5 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cell_center)
        
        #val = data.LessonID.name
        #[{'GraderID__TeacherID__surname': u'\u0391\u0398\u0391\u039d\u0391\u03a3\u039f\u03a0\u039f\u03a5\u039b\u039f\u03a5', 'countaction': 1, 'GraderID': 46, 'GraderID__TeacherID__name': u'\u0395\u039b\u0395\u039d\u0397', 'action': 1, 'station': 0, 'FolderID__no': 1}]

        val = data['FolderID__LessonID__name']
        worksheet_s.write_string(row, 1, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)        

        val = data['GraderID__TeacherID__surname']
        worksheet_s.write_string(row, 2, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)        

        val = data['GraderID__TeacherID__name']
        worksheet_s.write_string(row, 3, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)        

        
        val = data['FolderID__no']
        worksheet_s.write_number(row, 4, val, cell_center)        


    # change column widths
    worksheet_s.set_column('B:B', lesson_col_width)  # Lesson column

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
    
    # GLOBAL excel styles
    title = workbook.add_format({ 'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter'})
    header = workbook.add_format({'bg_color': '#F7F7F7','color': 'black','align': 'center','valign': 'top','border': 1})
    cell = workbook.add_format({'align': 'left','valign': 'top','text_wrap': True,'border': 1})
    cell_center = workbook.add_format({'align': 'center','valign': 'top','border': 1})
    
    title_text = u"{0} {1}".format(ugettext(u"ΕΙΚΟΝΑ ΕΡΓΑΣΙΑΣ ΒΑΘΜΟΛΟΓΗΤΗ"), '')
    # merge cells
    worksheet_s.merge_range('B2:I2', title_text, title)

    # write header
    worksheet_s.write(4, 0, ugettext(u"AA"), header)
    worksheet_s.write(4, 1, ugettext(u"Μάθημα"), header)
    worksheet_s.write(4, 2, ugettext(u"Επώνυμο"), header)
    worksheet_s.write(4, 3, ugettext(u"Όνομα"), header)
    worksheet_s.write(4, 4, ugettext(u"Σταθμός"), header)
    worksheet_s.write(4, 5, ugettext(u"Πράξη"), header)
    worksheet_s.write(4, 6, ugettext(u"Ημ-νία"), header)

    # column widths
    lesson_col_width = 20
    code_col_width = 25
    date_col_width = 20
    observations_col_width = 25

    #print dataDB
        
    # add data to the table
    row = 0 
    for idx, data in enumerate(dataDB):
        row = 5 + idx        
        
        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cell_center)
        
        val = data['FolderID__LessonID__name']
        worksheet_s.write_string(row, 1, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)

        val = data['GraderID__TeacherID__surname']
        worksheet_s.write_string(row, 2, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)
        #worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)        

        val = data['GraderID__TeacherID__name']
        worksheet_s.write_string(row, 3, val, cell)        
        if len(val) > lesson_col_width:
            lesson_col_width = len(val)

        
        val = data['station']
        worksheet_s.write_number(row, 4, val, cell_center)        

        val = data['action']
        worksheet_s.write_number(row, 5, val, cell_center)        

        val = data['actionTime']
        worksheet_s.write(row, 6, val.strftime('%d/%m/%Y'), cell_center)        


    # change column widths
    worksheet_s.set_column('B:D', lesson_col_width)  # Lesson column
    worksheet_s.set_column('G:G', date_col_width)  # Lesson column

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

    title, header, cell, cell_center = formatAWorkbook(workbook)
    
    # write title
    lesson_text = xlsTitle(lesson)
    title_text = u"{0} {1}".format(ugettext(u"ΣΥΝΟΛΑ"), lesson_text)
    
    # merge cells
    #worksheet_s.merge_range('B2:I2', title_text, title)

    # write header
    """
    worksheet_s.write(4, 0, ugettext(u"AA"), header)
    """

    # column widths
    lesson_col_width = 15
    code_col_width = 15
    observations_col_width = 25

    #print dataDB
     
    # add data to the table
    row = 0 
    """
    #val = u'OK' if data.status else u'-'
    #worksheet_s.write_string(row, 8, val, cell_center)
    """
    # change column widths
    worksheet_s.set_column('B:B', lesson_col_width)

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
    worksheet_s.write(4, 0, ugettext("No"), header)
    worksheet_s.write(4, 1, ugettext("Town"), header)
    worksheet_s.write(4, 2, ugettext("Date"), header)
    worksheet_s.write(4, 3, ugettext("Description"), header)
    worksheet_s.write(4, 4, ugettext(u"Max T. (℃)"), header)
    worksheet_s.write(4, 5, ugettext(u"Min T. (℃)"), header)
    worksheet_s.write(4, 6, ugettext("Wind (km/h)"), header)
    worksheet_s.write(4, 7, ugettext("Precip. (mm)"), header)
    worksheet_s.write(4, 8, ugettext("Precip. (%)"), header)
    worksheet_s.write(4, 9, ugettext("Observations"), header)

    # column widths
    town_col_width = 10
    description_col_width = 10
    observations_col_width = 25

    # add data to the table
    for idx, data in enumerate(weather_data):
        row = 5 + idx
        worksheet_s.write_number(row, 0, idx + 1, cell_center)

        worksheet_s.write_string(row, 1, data.town.name, cell)
        if len(data.town.name) > town_col_width:
            town_col_width = len(data.town.name)

        worksheet_s.write(row, 2, data.date.strftime('%d/%m/%Y'), cell_center)
        worksheet_s.write_string(row, 3, data.description, cell)
        if len(data.description) > description_col_width:
            description_col_width = len(data.description)

        worksheet_s.write_number(row, 4, data.max_temperature, cell_center)
        worksheet_s.write_number(row, 5, data.min_temperature, cell_center)
        worksheet_s.write_number(row, 6, data.wind_speed, cell_center)
        worksheet_s.write_number(row, 7, data.precipitation, cell_center)
        worksheet_s.write_number(row, 8,
                                 data.precipitation_probability, cell_center)

        observations = data.observations.replace('\r', '')
        worksheet_s.write_string(row, 9, observations, cell)
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
