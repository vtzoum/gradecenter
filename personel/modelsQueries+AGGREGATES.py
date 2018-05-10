#!/usr/bin/env python
# -*- coding: utf-8 -*-

#python manage.py shell
import datetime
from personel.models import * 
from personel.helpScripts import * 
from django.db.models import Avg, Count, Max, Min, Sum
#************************************************************
#AGGREGATES
#************************************************************


#************************************************************
#ACCEPTANCES
#************************************************************
# PARALAVES, TETRADIA(SYGKENTRVTIKA)
Acceptance.objects.all().aggregate(Sum('books'))
#{'books__sum': 662}

# PARALAVES, TETRADIA(ANALYTIKA) / MATHIMA 
#SELECT LessonID, SUM(books) as SumBooks FROM Acceptance GROUPBY LessonID ORDERBY SumBooks DESC
Acceptance.objects.values('LessonID').all().annotate(sumBooks=Sum('books'), sumBooksAbscent=Sum('booksAbscent'), sumBooksZero=Sum('booksZero'), ).order_by('-sumBooks')
#[{'LessonID': 4, 'sumBooks': 662, 'sumBooksAbscent': 1, 'sumBooksZero': 1}, {'LessonID': 5, 'sumBooks': 0, 'sumBooksAbscent': 0, 'sumBooksZero': 0}, 

# PLITHOS PARALAVWN / MATHIMA (SYGKENTRVTIKA)
Acceptance.objects.all().values('LessonID').annotate(Count('LessonID')).order_by('LessonID')
#[{'LessonID': 4, 'LessonID__count': 61}, {'LessonID': 5, 'LessonID__count': 61}, {'LessonID': 6, 'LessonID__count': 61}, {'LessonID': 7, 'LessonID__count': 61}, {'LessonID': 8, 'LessonID__count': 61}, {'LessonID': 9, 'LessonID__count': 61}, {'LessonID': 10, 'LessonID__count': 61}, {'LessonID': 11, 'LessonID__count': 61}, {'LessonID': 12, 'LessonID__count': 61}, {'LessonID': 13, 'LessonID__count': 61}, {'LessonID': 14, 'LessonID__count': 61}, {'LessonID': 15, 'LessonID__count': 61}, {'LessonID': 16, 'LessonID__count': 61}]

# PARALAVES / SXOLEIO 
#SELECT LessonID, SUM(books) as SumBooks FROM Acceptance GROUPBY LessonID ORDERBY SumBooks DESC
#SchoolToGradeID
data = Acceptance.objects.all().annotate(sumBooks=Sum('books'), sumBooksAbscent=Sum('booksAbscent'), sumBooksZero=Sum('booksZero'), ).order_by('SchoolToGradeID')
#[{'LessonID': 4, 'sumBooks': 662, 'sumBooksAbscent': 1, 'sumBooksZero': 1}, {'LessonID': 5, 'sumBooks': 0, 'sumBooksAbscent': 0, 'sumBooksZero': 0}, 
for d in data: 
   print d.id, d.SchoolToGradeID.name, d.LessonID.name, d.books, d.booksAbscent, d.booksZero 
   #print d['id'], d['LessonID__name']

#############################
# OK-PARALAVES / SXOLEIO 
#############################
s=SchoolToGrade.objects.get(id=1)
print "%s %s %s %s" %(s.code, s.name, s.ddeCode, s.ddeName)
for a in s.acceptance_set.all():
    print a.id, a.LessonID.name, 
    print a.books, a.booksAbscent, a.booksZero



#************************************************************
#GRADER Model 
#************************************************************
# Select isgraderC, count(isgraderC) From Grader GroupBY isgraderC
p = Grader.objects.values('isgraderC').annotate(grader=Count('isgraderC'))
p

p = Grader.objects.values('isCoordinator').annotate(grader=Count('isgraderC'))
[x['isgraderC'] for x in p]
[x['isCoordinator'] for x in p]
[x[0] for x in p]
p

# Graders per Lesson
p = Grader.objects.values('LessonID').annotate(grader=Count('LessonID'))
p
# [{'grader': 4, 'LessonID': 4}, {'grader': 3, 'LessonID': 5}, {'grader': 8, 'LessonID': 6}, {'grader': 9, 'LessonID': 9}, {'grader': 8, 'LessonID': 10}, {'grader': 1, 'LessonID': 11}]


#************************************************************
#REPORTS
#************************************************************
import datetime
from personel.models import * 
from personel.helpScripts import * 
from django.db.models import Avg, Count, Max, Min, Sum


#************************************************************
#BOOKING
#************************************************************
Booking.objects.all().values()

#Where GraderId = 46
Booking.objects.filter( GraderID = 46).values()

#OrderBy time
Booking.objects.filter( GraderID = 46).values().order_by('actionTime')


#OrderBy Grader, time
Booking.objects.all().order_by('GraderID', 'actionTime').values()
#[{'actionTime': datetime.datetime(2016, 9, 23, 14, 51, 7, tzinfo=<UTC>), u'GraderID_id': 46, 'station': 0, 'action': 0, u'id': 16, u'FolderID_id': 1}, {'actionTime': datetime.datetime(2016, 9, 23, 14, 57, 59, tzinfo=<UTC>), u'GraderID_id': 46, 'station': 1, 'action': 1, u'id': 17, u'FolderID_id': 1}, {'actionTime': datetime.datetime(2016, 9, 24, 4, 24, 8, tzinfo=<UTC>), u'GraderID_id': 46, 'station': 1, 'action': 0, u'id': 20, u'FolderID_id': 1}, ... ]


#************************************************************
#BOOKING+TIME
#************************************************************
now = datetime.datetime.now()



#************************************************************
#BOOKING+TIME+DIffrence/duration
#************************************************************
t0 = Booking.objects.filter(FolderID__id =46, GraderID__id = 46, action = 0).order_by('actionTime')[0].actionDuration
t1 = datetime.datetime.now()
t0 = datetime.datetime(2017,5,10,10,0,0)

tDiff = t1-t0  # timedelta 
str(tDiff )    # print

#tDelta3H = timedelta(minutes=1)
tDelta3H = timedelta(hours=3) #ok
Booking.objects.filter(id=11).update(actionDuration=datetime.datetime.now()-datetime.datetime(2017,5,10,10,0,0))   #ok
tDuration = Booking.objects.get(id=11).actionDuration    # ok
if tDuration > tDelta3H: 
    print "elidgible"

Booking.objects.all().order_by('-actionTime').values('id', 'actionTime')   #ok
        #[0].actionDuration

Folder.objects.exclude(codeStatus=2).select_related("BookingID", "GraderID")

#************************************************************
#QUERY on SPECIFIC DAY 
# ... WHERE date > xxx OrderBy Grader, time
Booking.objects.filter(actionTime__gt=datetime(2017, 9, 23)).values().order_by('GraderID', 'actionTime')

# ... WHERE date = xxx OrderBy Grader, time
# ... OrderBy AA aka date OR id
Booking.objects.filter( actionTime__year='2016', actionTime__month='9', actionTime__day='23', )\
        .values('id', 'actionTime')\
        .order_by('actionTime')


#************************************************************
#QUERY on WEEKEDNS / SABATTA/KYRIAKES 
#weekno = date.weekday()
weekno = datetime.datetime.today().weekday()
if weekno<5:
    print "Weekday"
    return False
else:
    print "Weekend"
    return True 



# ISNULL
s0 = Booking.objects.all().values('id', 'actionTime').order_by('-actionTime')
for r in s0:                             # ok
    print r['actionTime'].weekday()     

# isnull is none
s0 = Booking.objects.filter(actionDuration__isnull=True).values('id', 'actionTime', 'actionDuration').order_by('-actionTime')
s1 = Booking.objects.exclude(actionDuration__isnull=True).values('id', 'actionTime', 'actionDuration').order_by('-actionTime')
s2 = Booking.objects.filter(actionDuration=None).values('id', 'actionTime', 'actionDuration').order_by('-actionTime')

print s1[0]['actionTime'].weekday()      # ok

for r in s1:                             # ok
    print str(r['actionDuration'])



#B. approach 
#http://stackoverflow.com/questions/14972601/exclude-weekends-in-python-django-query-set
weekends = [2, 3, 9, 10, 16, 17, 23, 24]
#Booking.objects.filter(actionTime__month=month).exclude(actionTime__day=weekends)
Booking.objects.filter(actionTime__day=weekends)


#LIST OF SABATTA/KYRIAKES 
# get all dates for the period
#date_list = [(start_date) + datetime.timedelta(days=day) for day in range(0, days_to_show)]
#(start_date, day, days_to_show) = ((datetime.date(2017, 5, 12), 0 , 10)
date_list = [(datetime.date(2017, 5, 12)) + datetime.timedelta(days=day) for day in range(0, 10)]
# filter out week ends 
date_list = [date.strftime("%A") for date in date_list if date.weekday() not in (5,6)]
print date.strftime("%A")

#https://docs.djangoproject.com/en/dev/ref/models/querysets/#week-day
#Entry.objects.filter(pub_date__week__gte=32, pub_date__week__lte=38)

#*************************************************
# FILTER ON WEEKENDS #OK
# Saturday = 7 Sunday = 1 | 1: SUNDAY, 2: MONDAY etc.
#DJANGO 1.11
s0=Booking.objects.filter(actionTime__week_day__in=[7,1]).values('id', 'actionTime').order_by('actionTime')
for s in s0:# ok
    print s['actionTime'].strftime("%A")
    
#*************************************************
# Synoliko xronos ergasias ana hmera
#SELECT LessonID, SUM(books) as SumBooks FROM Acceptance GROUPBY LessonID ORDERBY SumBooks DESC
s0=Booking.objects.filter(actionTime__week_day__in=[1,2,3,4,5,6,7])\
        .annotate(sumActionDuration=Sum('actionDuration'),)\
        .values('id', 'actionTime', 'actionDuration', 'sumActionDuration')\
        .order_by('actionTime')
[print s for s in s0: if s['sumActionDuration']!=None]
#{'sumActionDuration': datetime.timedelta(0,77, 248532), 'actionTime':, datetime.datetime(2017,5,17,16,30,45,341659), 'id':31, 'actionDuration':datetime.timedelta(0,77),} 

#returns timedelta (hours, seconds) 
td = datetime.timedelta(0,77) 
td.total_seconds()
# 77.0
td.seconds
# 77.0
print "days (%f:2) hours (%f) minutes (%f)" %(td.days, td.seconds//3600, (td.seconds//60)%60)
print "days (%2.2f) hours (%0.2f) minutes (%0.2f)" %(td.days, td.seconds//3600, (td.seconds//60)%60)

def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60

##
##
weekdays=[1,2,3,4,5,6,7]
WeekEnds=[1,7]

data = Booking.objects.filter(actionTime__week_day__in=weekdays)\
        .order_by('actionTime',)
        #.order_by('GraderID__LessonID', 'GraderID','actionTime',)
data = data.select_related("FolderID", "GraderID").all()
data.annotate(sumActionDuration=Sum('actionDuration'),).all()


###
### OK
data = Booking.objects\
    .annotate(sumDuration=Sum('actionDuration'),countTime=Count('actionTime__day'),)\
    .filter(actionTime__week_day__in=weekdays, action=1)\
    .select_related("FolderID", "GraderID").all()\
    .order_by('GraderID__LessonID', 'GraderID','actionTime',)
    #.order_by('actionTime',)


[(s.id,s.GraderID_id, s.sumDuration) for s in data]
#[s for s in data if s['sumActionDuration']!=None]


### SOS ANONTATIO OF QUERYSET 
# NA DW SIGOURA 
>>> q = Book.objects.annotate(Count('authors'))
>>> q = Book.objects.annotate(auth_count=Count('authors'))


## GROUP BY DATE
## DJANGO 1.11
from django.db.models.functions import TruncMonth, Trunc 
Booking.objects
    .annotate(month=TruncMonth('actionTime'))  # Truncate to month and add to select list
    .values('month')                          # Group By month
    .annotate(c=Count('id'))                  # Select the count of the grouping
    .values('month', 'c')                     # (might be redundant, haven't tested) select month and count 

Booking.objects.annotate(month=TruncMonth('actionTime')).values('month').annotate(c=Count('id')).values('month', 'c') 

### Trunc is NOT defined 
data = Booking.objects.annotate(start_day=Trunc('actionTime', 'day', output_field=DateTimeField())).filter(start_day=datetime(2017, 5, 10))
for exp in data:
    print(exp.start_datetime)


#data = Booking.objects.datetimes('actionTime', 'day').annotate(c=Count('id')).values()
data = Booking.objects.datetimes('actionTime', 'day').annotate(nowday=actionTime, c=Count('GraderID')).values('GraderID_id', 'actionTime', 'c', )
[s.GraderID_id, s.sumDuration) for s in data]


###################################################################
import datetime
from personel.models import * 
from personel.helpScripts import * 
from django.db.models import Avg, Count, Max, Min, Sum

#
#
#
#WORKS OK #WORKS OK #WORKS OK #WORKS OK #WORKS OK #WORKS OK #WORKS OK #WORKS OK 
data = Booking.objects.select_related("FolderID", "GraderID").all()
data = data.extra(select={'day':'date( actionTime )'}).values('GraderID_id', 'day').annotate(available=Count('actionTime')).annotate(sumDuration=Sum('actionDuration'))
print data    

###MINE
data = Booking.objects.filter(actionTime__week_day__in=weekdays).select_related("FolderID", "GraderID").all()
data = data.extra(select={'day':'date( actionTime )'}).values('GraderID_id', 'day', 'countTimes',)\
        .annotate(countTimes=Count('day')).annotate(sumDuration=Sum('actionDuration'))
print data



#************************************************************
#kinisi Hmeras / AA
now = datetime.datetime.now()
print now.year, now.month, now.day, now.hour, now.minute, now.second

#SELECT Lesson.id, Grader.isgraderC, Folder.codeStatus
#FROM (JOIN):BOOKING X GRADER X FOLDER
# WHERE date = '2016-9-23' ORDERBY actionTime
records = Booking.objects.select_related("FolderID", "GraderID").filter( 
        actionTime__year='2016', 
        actionTime__month='9', 
        actionTime__day='23', 
        ).order_by('GraderID__LessonID', 'actionTime')
#[<Booking: Booking object>, <Booking: Booking object>]

#(4, True, 1)
#(4, True, 1)


#************************************************************
#Fakeloi pou einai se vathmologiti (+Teacher data via Grader)
records = Booking.objects.select_related("FolderID", "GraderID").filter(GraderID__LessonID=4).order_by('GraderID__LessonID', 'actionTime')
records = Booking.objects.select_related("FolderID", "GraderID")\
        .filter(GraderID__LessonID=4, FolderID__codeLocation=1, action=0, station=0).distinct()     #ok   

for R in records:
    R.FolderID.id, R.FolderID.codeStatus, R.GraderID.LessonID.id, R.GraderID.isgraderC, R.GraderID.TeacherID.name, R.GraderID.TeacherID.surname



#************************************************************
# BOOKING + GRADERS
#************************************************************
records = BookingJoinTables(GraderID=GraderID).order_by('FolderID__LessonID__name','SchoolToGradeID__name')
records = BookingJoinTables().filter(GraderID=46).order_by('FolderID__LessonID__name')
            #.filter(LessonID=FolderID__LessonID)\


#************************************************************
# EIKONA ERGASIAS ANA BATHMOLOGHTH (ANALYTIKA)
# FAKELOUS POY PHRE 
Booking.objects.filter( GraderID=46, station=0, action=0 ).values().annotate(countAction=Count('action')).order_by('action')
#[{'actionTime': datetime.datetime(2016, 9, 23, 14, 51, 7), u'GraderID_id': 46, 'countAction': 1, 'station': 0, 'action': 0, u'id': 16, u'FolderID_id': 1}]

#Booking.objects.filter( GraderID=46, station=0, action=0 ).values('action', 'station', 'GraderID', ).annotate(countAction=Count('action')).order_by('action')

# FAKELOUS POY EDVSE ΠΙΣΩ
Booking.objects.filter( GraderID=46, station=0, action=1 ).values('GraderID', 'station', 'action').annotate(countAction=Count('action')).order_by('action')
#[{'actionTime': datetime.datetime(2016, 9, 24, 4, 34, 57), u'GraderID_id': 46, 'countAction': 1, 'station': 0, 'action': 1, u'id': 25, u'FolderID_id': 1}]

#************************************************************
# EIKONA ERGASIAS / OLOI BATHMOLOGHTES (ANALYTIKA)
Booking.objects.all().values('action', 'station', 'GraderID').order_by('GraderID', 'station', 'action' )
#[{'action': 0, 'station': 0, 'GraderID': 46}, {'action': 1, 'station': 0, 'GraderID': 46}, {'action': 0, 'station': 1, 'GraderID': 46}, {'action': 0, 'station': 1, 'GraderID': 46}, {'action': 0, 'station': 1, 'GraderID': 46}, {'action': 1, 'station': 1, 'GraderID': 46}, {'action': 1, 'station': 1, 'GraderID': 46}, {'action': 1, 'station': 1, 'GraderID': 46}]


#************************************************************
# EIKONA ERGASIAS / OLOI BATHMOLOGHTES (SYGKENTRVTIKA)
Booking.objects.all().values('GraderID', 'station', 'action').annotate(countAction=Count('GraderID'))
#[{'action': 0, 'station': 0, 'countAction': 1, 'GraderID': 46}, 
#{'action': 1, 'station': 0, 'countAction': 1, 'GraderID': 46}, 
#{'action': 0, 'station': 1, 'countAction': 3, 'GraderID': 46}, 
#{'action': 1, 'station': 1, 'countAction': 3, 'GraderID': 46}]


#************************************************************
# EIKONA ERGASIAS + HMERA / OLOI BATHMOLOGHTES (ANALYTIKA)
Booking.objects.all().values('action', 'station', 'actionTime', 'GraderID').order_by('GraderID', 'actionTime' )
#[{'action': 0, 'station': 0, 'GraderID': 46, 'actionTime': datetime.datetime(2016, 9, 23, 14, 51, 7)},

Booking.objects.all().values('action', 'station', 'actionTime', 'GraderID').order_by('GraderID', 'actionTime' )


#************************************************************
# EIKONA ERGASIAS + HMERA / OLOI BATHMOLOGHTES (SYGKENTRVTIKA)

#PLATFOM Specific/
#Django 1.09 and below
from django.db import connection
from django.db.models import Sum, Count

truncate_date = connection.ops.date_trunc_sql('day', 'actionTime')
Booking.objects.extra({'day':truncate_date}).values('day').annotate(Count('GraderID')) 
#[{'GraderID__count': 2, 'day': u'2016-09-23'}, 
#{'GraderID__count': 6, 'day': u'2016-09-24'}]

# EIKONA ERGASIAS + MHNA / OLOI BATHMOLOGHTES (SYGKENTRVTIKA)
truncate_date = connection.ops.date_trunc_sql('month', 'actionTime')
Booking.objects.extra({'month':truncate_date}).values('month').annotate(Count('GraderID')) 
#[{'GraderID__count': 8, 'month': u'2016-09-01'}]

#PLATFOM Specific/
#Django 1.10 and above
from django.db.models.functions import TruncMonth
Booking.objects.all().annotate(month=TruncMonth('actionTime'))\
        .values('month')\
        .annotate(c=Count('GraderID')).values('month', 'c')


# fakelous poy edvse + folder info
BookingJoinTables.objects.filter( graderid=46, station=0, action=1, )\
        .values('graderid', 'folderid__no', 'station', 'action')\
        .annotate(countaction=count('action')).order_by('action')
#[{'actiontime': datetime.datetime(2016, 9, 24, 4, 34, 57), u'graderid_id': 46, 'countaction': 1, 'station': 0, 'action': 1, u'id': 25, u'folderid_id': 1}]


BookingJoinTables().filter( GraderID=46, station=0, action=1)\
        .values('GraderID', 'GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 'FolderID__no', 'station', 'action')\
        .annotate(countaction=Count('action')).order_by('action')


#************************************************************
# eikona ergasias ana bathmologhth (sygkentrvtika)
BookingJoinTables.objects.filter( graderid=46, station=0, action=1 )\
        .values('graderid')\
        .annotate(countaction=count('graderid'))








#************************************************************
# GRADERS
#************************************************************

#########################################
#Graders of Lesson
Grader.objects.filter(LessonID=4).values()
#[{'status': 0, 'currentFolder': None, 'isCoordinator': False, u'id': 46, u'TeacherID_id': 16, 'isgraderC': True, u'LessonID_id': 4}, {'status': 0, 'currentFolder': u'', 'isCoordinator': True, u'id': 47, u'TeacherID_id': 17, 'isgraderC': False, u'LessonID_id': 4}, {'status': 0, 'currentFolder': None, 'isCoordinator': True, u'id': 51, u'TeacherID_id': 14, 'isgraderC': False, u'LessonID_id': 4}, {'status': 0, 'currentFolder': None, 'isCoordinator': False, u'id': 52, u'TeacherID_id': 15, 'isgraderC': False, u'LessonID_id': 4}]



#************************************************************
# FOLDERS
#************************************************************
import datetime
from personel.models import * 
from personel.helpScripts import * 
from django.db.models import Avg, Count, Max, Min, Sum

"""
#GRAD_TYPE = ( (0, u'Φ(Α)'), (1, u'Φ(Β)'),(1, u'Φ(ΑΝΑ)'), )
GRAD_TYPE = ( (0, u'Κανονικός'), (1, u'Αναβαθμολόγηση'), )
LOCATION_TYPE = ( (0, u'Αποθήκη'), (1, u'Βαθμολογητής'), (2, u'Φύλαξη'), )
STATUS_TYPE = ( (0, u'Αχρέωτος(A)'), (1, u'Αχρέωτος(Β)'), (2, u'Αχρέωτος(C)'), 
    (3, u'Χρεωμένος(A)'), (4, u'ΧρεωμένοςΒ)'), (5, u'Χρεωμένος(C)'), 
    (8, u'Επιστροφή' ), )
"""

"""
example GROUPBY ... HAVING ...
MyModel.objects.filter(row_id__in=[15,17])\
.distinct()\
.values('user_id')\
.annotate(user_count=Count('user_id'))\
.filter(user_count__gt=1)\
.order_by('user_id')

"""

records = Folder.objects.select_related("LessonID").filter(LessonID=4)
for r in records:
    print r.id


#########################################
#Synola / typo 


#Total F(ABC)
fABC = Folder.objects.all().values('LessonID')\
        .annotate(countId=Count('id'),)
fABC
#[{'countId': 27, 'LessonID': 4}, {'countId': 25, 'LessonID': 5}]


fABC = Folder.objects.all().values('LessonID', 'codeType')\
        .annotate(countType=Count('codeType'),)
fABC

dataDB = [{'LessonID': 4, 'countType': 23, 'codeType': 0}, 
{'LessonID': 4, 'countType': 3, 'codeType': 1}, 
{'LessonID': 4, 'countType': 1, 'codeType': 2}, 
{'LessonID': 5, 'countType': 25, 'codeType': 0}]

import itertools 
for key, group in itertools.groupby(dataDB, lambda item: item["LessonID"]):
    print key, group
    (fA, fB, fC) = (0, 0, 0)
    for x in group: 
        print key, x['codeType'], x['countType']
        if x['codeType']==0 : 
            fA = x['countType']
        elif x['codeType']==1 : 
            fB = x['countType']
        elif x['codeType']==2 : 
            fC = x['countType']
    print key, (fA, fB, fC)

#RESULTS OK
4 <itertools._grouper object at 0x7f0864ee6dd0>
4 0 23
4 1 3
4 2 1
4 (23, 3, 1)
5 <itertools._grouper object at 0x7f0864ee6fd0>
5 0 25
5 (25, 0, 0)


#########################################
#Folder Totals

#Folder Totals2
#T0 = Folder.objects.all().values('codeStatus', 'codeType', 'LessonID')\
T0 = Folder.objects.all().values('codeStatus', 'codeType', 'LessonID')\
        .annotate(countCodeType=Count('codeStatus'),)\
        .order_by('LessonID','codeType','codeStatus')
        #.annotate(countCodeType=Count('codeType'),)\

for R in T0:
    print R

dataDB = [
    {'codeType': 0, 'countCodeType': 21, 'LessonID': 4, 'codeStatus': 0}, 
    {'codeType': 0, 'countCodeType': 2, 'LessonID': 4, 'codeStatus': 1}, 
    {'codeType': 1, 'countCodeType': 1, 'LessonID': 4, 'codeStatus': 0}, 
    {'codeType': 1, 'countCodeType': 2, 'LessonID': 4, 'codeStatus': 2}, 
    {'codeType': 2, 'countCodeType': 1, 'LessonID': 4, 'codeStatus': 1}, 
    # foo 
    {'codeType': 1, 'countCodeType': 2, 'LessonID': 100, 'codeStatus': 2}, 
    {'codeType': 2, 'countCodeType': 1, 'LessonID': 100, 'codeStatus': 1}, 
    {'codeType': 0, 'countCodeType': 21, 'LessonID': 200, 'codeStatus': 0}, 
    {'codeType': 0, 'countCodeType': 2, 'LessonID': 200, 'codeStatus': 1}, 
    {'codeType': 1, 'countCodeType': 1, 'LessonID': 200, 'codeStatus': 0}, 
]


# SubGroups list of Folders #OK
import itertools
for key, group in itertools.groupby(dataDB, lambda item: item["LessonID"]):
    #print key, sum([item["tmst"] for item in group])
    print key, ([item for item in group])
    #print key, group



#Folder Totals1
T1 = Folder.objects.all().values('codeStatus', 'codeType','codeLocation', 'LessonID')\
        .annotate(countCodeType=Count('codeType'),)\
        .order_by('LessonID','codeType')



for R in records:
    print R
{'codeType': 0, 'countCodeType': 21, 'LessonID': 4, 'codeLocation': 0, 'codeStatus': 0}
{'codeType': 0, 'countCodeType': 3, 'LessonID': 4, 'codeLocation': 2, 'codeStatus': 1}
{'codeType': 1, 'countCodeType': 1, 'LessonID': 4, 'codeLocation': 0, 'codeStatus': 0}
{'codeType': 1, 'countCodeType': 1, 'LessonID': 4, 'codeLocation': 0, 'codeStatus': 2}
{'codeType': 2, 'countCodeType': 1, 'LessonID': 4, 'codeLocation': 2, 'codeStatus': 1}




#########################################
#Folders Out Now / ΔΙΟΡΘΩΝΟΝΤΙΑ ΤΩΡΑ
now = datetime.datetime.now()
print now.year, now.month, now.day, now.hour, now.minute, now.second

#SELECT Lesson.id, Grader.isgraderC, Folder.codeStatus
#FROM (JOIN):BOOKING X GRADER X FOLDER
# WHERE date = '2016-9-23' ORDERBY actionTime
records = Folder.objects.filter( codeLocation = 1 ).values()
records 

#########################################
# KATASTASH ΦΑΚΕΛΩΝ GIA OLA TA ΜΑΘΗΜΑTA (aka POREIA DIORTHOSIS)
records = Folder.objects.all().values('codeStatus', 'codeType', 'LessonID').annotate(countStatus=Count('codeStatus')).order_by('LessonID','codeType')
for R in records:
    print R

records = Folder.objects.all().values('codeStatus', 'codeType','codeLocation', 'LessonID')\
        .annotate(countCodeType=Count('codeType'), countCodeStatus=Count('codeStatus'), countCodeLocation=Count('codeLocation'))\
        .order_by('LessonID','codeType')


{'countCodeLocation': 4, 'countCodeType': 4, 'codeLocation': 0, 'codeStatus': 0, 'codeType': 0, 'LessonID': 4, 'countCodeStatus': 4}
{'countCodeLocation': 1, 'countCodeType': 1, 'codeLocation': 0, 'codeStatus': 1, 'codeType': 0, 'LessonID': 4, 'countCodeStatus': 1}
{'countCodeLocation': 5, 'countCodeType': 5, 'codeLocation': 0, 'codeStatus': 0, 'codeType': 1, 'LessonID': 4, 'countCodeStatus': 5}
{'countCodeLocation': 5, 'countCodeType': 5, 'codeLocation': 0, 'codeStatus': 0, 'codeType': 0, 'LessonID': 5, 'countCodeStatus': 5}
{'countCodeLocation': 1, 'countCodeType': 1, 'codeLocation': 0, 'codeStatus': 0, 'codeType': 1, 'LessonID': 5, 'countCodeStatus': 1}


valuesCodeStatus = Folder.objects.filter(LessonID=4).values('codeType', 'LessonID__name', 'codeStatus').annotate(countStatus=Count('codeStatus')).order_by('codeType') 
valuesCodeStatus = Folder.objects.filter(LessonID=4).values('codeStatus').annotate(countStatus=Count('codeStatus'))\
        #.order_by('codeType') 
print valuesCodeStatus 

#keys={}
values=[]
keys=[]
for r in valuesCodeStatus :
    for k in r.keys():
        #if 'count' in k:      # has substring
        if k not in keys: 
            keys.append(k)
        else: 
            keys.append(k)
        values.append(r[k])
        print k, r[k]
        
#var.values()
print keys 
print values


#########################################
# KATASTASH ΦΑΚΕΛΩΝ GIA TO ΜΑΘΗΜΑ (aka POREIA DIORTHOSIS)
STATUS_TYPE = ( (0, u'Αχρέωτος(A)'), (1, u'Αχρέωτος(Β)'), (2, u'Αχρέωτος(C)'), 
    (3, u'Χρεωμένος(A)'), (4, u'ΧρεωμένοςΒ)'), (5, u'Χρεωμένος(C)'), 
    (8, u'Επιστροφή' ), )

#recordsA = Folder.objects.filter(LessonID=4, codeType=0, codeStatus in []).values('codeType', 'LessonID', 'codeStatus').annotate(countStatus=Count('codeStatus')).order_by('codeType')
recordsB = Folder.objects.filter(LessonID=4).values('codeType', 'LessonID', 'codeStatus').annotate(countStatus=Count('codeStatus')).order_by('codeType')
recordsC = Folder.objects.filter(LessonID=4).values('codeType', 'LessonID', 'codeStatus').annotate(countStatus=Count('codeStatus')).order_by('codeType')
[R for R in records]

{'codeStatus': 0, 'countStatus': 4, 'LessonID': 4, 'codeType': 0}
{'codeStatus': 1, 'countStatus': 1, 'LessonID': 4, 'codeType': 0}
{'codeStatus': 0, 'countStatus': 5, 'LessonID': 4, 'codeType': 1}

# same result - change order for readability
records = Folder.objects.filter(LessonID=4).values('codeStatus', 'codeType', 'LessonID' ).annotate(countStatus=Count('codeStatus')).order_by('codeType')
[R for R in records]

[
{'countStatus': 24, 'codeType': 0, 'LessonID': 4, 'codeStatus': 0}, 
{'countStatus': 2, 'codeType': 0, 'LessonID': 4, 'codeStatus': 3}
]


#************************************************************
from django.db.models import Avg, Count, Max, Min, Sum

from personel.models import * 
from personel.helpScripts import * 


#************************************************************
#SXOLEIA
#************************************************************
# PLHTHOS / TYPO SXOLEIOY 
SchoolToGrade.objects.all().values('type').annotate(countType=Count('type')).order_by('type')
#[{'countStatus': 55, 'type': 1}, {'countStatus': 6, 'type': 2}]



