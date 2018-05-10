#!/usr/bin/env python
# -*- coding: utf-8 -*-

#python manage.py shell
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
#************************************************************
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
#*************************************************
s0=Booking.objects.filter(actionTime__week_day__in=[7,1]).values('id', 'actionTime').order_by('actionTime')
for s in s0:# ok
    print s['actionTime'].strftime("%A")
    

#*************************************************
# Synoliko xronos ergasias ana hmera
#SELECT LessonID, SUM(books) as SumBooks FROM Acceptance GROUPBY LessonID ORDERBY SumBooks DESC
#*************************************************
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
    .select_related("FolderID", "GraderID").all()\
    .annotate(sumDuration=Sum('actionDuration'),countTime=Count('actionTime__day'),)\
    .order_by('GraderID__LessonID', 'GraderID','actionTime',)
    #.order_by('actionTime',)


[(s.id,s.GraderID_id, s.sumDuration) for s in data]
#[s for s in data if s['sumActionDuration']!=None]


### SOS ANONTATIO OF QUERYSET 
# NA DW SIGOURA 
>>> q = Book.objects.annotate(Count('authors'))
>>> q = Book.objects.annotate(auth_count=Count('authors'))


#*************************************************
## GROUP BY DATE
## DJANGO 1.11
#*************************************************
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


#*************************************************
import datetime
from personel.models import * 
from personel.helpScripts import * 
from django.db.models import Avg, Count, Max, Min, Sum
#*************************************************

''' 
-OK
SELECT (COUNT(DISTINCT(DATE(actionTime)))) AS 'TotalWeekdays', personel_booking.GraderID_id
FROM personel_booking
GROUP BY GraderID_id;
TotalWeekdays | GraderID_id
"9","1"
"7","2"
"5","3"
"4","4"
"5","5"
"9","6"
'''

#*************************************************
#WORKS OK #WORKS OK #WORKS OK #WORKS OK #WORKS OK #WORKS OK #WORKS OK #WORKS OK 
#*************************************************
data = Booking.objects.select_related("FolderID", "GraderID").all()
data = data.extra(select={'day':'date( actionTime )'}).values('GraderID_id', 'day')\
        .annotate(available=Count('actionTime'))\
        .annotate(sumDuration=Sum('actionDuration'))
print data    


###MINE
data = Booking.objects.filter(actionTime__week_day__in=weekdays).select_related("FolderID", "GraderID").all()
data = data.extra(select={'day':'date( actionTime )'}).values('GraderID_id', 'day', 'countTimes',)\
        .annotate(countTimes=Count('day', distinct = True)).annotate(sumDuration=Sum('actionDuration'))
print data


#************************************************************
# HMERES ERGASIAS 
#************************************************************
''' 
TO QUERY doulevei sthn sqlite
Afto prepei na kanw map sto Django ORM

SELECT (COUNT(DISTINCT(DATE(actionTime)))) AS 'TotalWeekdays', personel_booking.GraderID_id
FROM personel_booking
GROUP BY GraderID_id;
TotalWeekdays | GraderID_id
"9","1"
"7","2"
"5","3"
"4","4"
"5","5"
"9","6"
'''

weekdays=[1,2,3,4,5,6,7]
weekends=[1,7]

#OK-HMERES ERGASIAS
#data = data.extra(select={'day':'date( actionTime )'}).values('GraderID_id', 'day')
''' extra(select{}) ''' 
qs = Booking.objects.filter(actionTime__week_day__in=weekdays)\
    .extra(select={'TotalDates':'COUNT(DISTINCT(date(actionTime)))',})\
    .values('graderid_id', 'totaldates',)\
    .annotate(countGraderDates=Count('GraderID_id'))\
    .values('GraderID_id', 'countGraderDates',)\
    .order_by('GraderID_id')

qs 
print qs.query


#************************************************************
# OK-RAW SQL
#************************************************************
''' 
TO QUERY doulevei sthn sqlite
Afto prepei na kanw map sto Django ORM

SELECT (COUNT(DISTINCT(DATE(actionTime)))) AS 'TotalWeekdays', personel_booking.GraderID_id
FROM personel_booking
GROUP BY GraderID_id;
TotalWeekdays | GraderID_id
"9","1"
"7","2"
"5","3"
"4","4"
"5","5"
"9","6"
'''
#OK- WEEKDAYS
SQL = "SELECT id, (COUNT(DISTINCT(DATE(actionTime)))) AS 'TotalWeekdays', personel_booking.GraderID_id FROM personel_booking GROUP BY GraderID_id;"
raw = Booking.objects.raw(SQL)
for r in raw[0:10]: 
    print  r.GraderID_id, r.TotalWeekdays #r.TeacherName, r.TotalDays


#NOT OK- WEEKENDS
SQL = "SELECT id, (COUNT(DISTINCT(DATE(actionTime,'N')))) AS 'TotalWeekdays', personel_booking.GraderID_id FROM personel_booking GROUP BY GraderID_id;"
raw = Booking.objects.raw(SQL)
for r in raw[0:10]: 
    print  r.GraderID_id, r.TotalWeekdays #r.TeacherName, r.TotalDays

#WHERE ('%Y%m%d',Date) between '20161001' AND '20161005'

#************************************************************
# NEW TRY
#************************************************************
.extra(select={'date':'DATE(actionTime)','count':'COUNT(GraderID_id)'})\
.values('countTimes', 'GraderID__TeacherID_id','GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 'GraderID__TeacherID__codeAfm')\

data = Booking.objects.filter(actionTime__week_day__in=weekdays).select_related("FolderID", "GraderID")\
        .extra(select={'date':'DATE(actionTime)',})\
        .values('date','GraderID_id',)\
        .annotate(countTimes=Count('GraderID_id', distinct = True))\
        .order_by('GraderID_id')
data

for d in data: 
    print  d['GraderID_id'], d['countTimes']


#sum(1 for x in d.values() if some_condition(x))
""" Custom fuct. to couint days in dbData dict for each Grader """
def countDays0(data):
    countDict = {}  # a Dict of Dicts
    for d in data:
        gid = d['GraderID_id']
        gsurname = d['GraderID__TeacherID__surname']
        gname = d['GraderID__TeacherID__name']
        gafm = d['GraderID__TeacherID__codeAfm']
        date = d['date']
        #print gid, date
        if gid not in countDict.keys():   # .count('date') > 1:
            print gid
            countDict[gid]={}
            countDict[gid]['dates']=[]
            countDict[gid]['surname']=gsurname
            countDict[gid]['name']=gname
            countDict[gid]['afm']=gafm
        if date not in countDict[gid]['dates']:
            countDict[gid]['dates'].append(date)
    return countDict

print countDays0(data) 

countDict = countDays0(data) 
for g in countDays0(data).keys(): 
    print countDict[g]['surname'], len(countDict[g]['dates'])
    

print countDays0(data) 
#>>> countDict
#{512: [u'2017-06-15', u'2017-06-16', u'2017-06-17', u'2017-06-18', u'2017-06-19'], 1: [u'2017-06-09',



#************************************************************
# RAW SQL NEW TRY
#************************************************************
"""
SQL = "SELECT (COUNT(DISTINCT(date(actionTime)))) AS 'TotalWeekdays', personel_booking.GraderID_id FROM personel_booking WHERE django_datetime_extract('week_day', personel_booking.actionTime, None) IN (1, 2, 3, 4, 5, 6, 7)"
"""
raw = Booking.objects.raw(SQL)
for r in raw: 
    print r.TotalWeekdays, #r.TeacherSurname, r.TeacherName, r.TotalDays


#************************************************************
# NEW TRY
# DJANGO 1.11
#************************************************************
from django.db.models.functions import Extract
Experiment.objects.create(start_datetime=start, start_date=start.date(),end_datetime=end, end_date=end.date())
# Add the experiment start year as a field in the QuerySet.
experiment = Experiment.objects.annotate(start_year=Extract('start_datetime', 'year')).get()
experiment.start_year
#2015
# How many experiments completed in the same year in which they started?
Experiment.objects.filter(start_datetime__year=Extract('end_datetime', 'year')).count()


# MY TRY
# Add the experiment start year as a field in the QuerySet.
rec = Booking.objects.annotate(date=Extract('actionTime', 'date')).get()
rec.date
#2015
# How many experiments completed in the same year in which they started?
Experiment.objects.filter(start_datetime__year=Extract('end_datetime', 'year')).count()



'''Date=Func(F '''
Booking.objects.annotate(Date=Func(F('actionTime'), function='DATE')).values('GraderID_id', 'Date').annotate(Count('Date')).order_by('GraderID_id')


#Booking.objects.filter(actionTime__week_day__in=weekdays).extra(select={'TotalWeekdays':'COUNT(date(actionTime))'}).values('id', 'GraderID_id', 'TotalWeekdays')



#************************************************************
#+ SK ERGASIAS
#************************************************************
#data = data.extra(select={'day':'date( actionTime )'}).values('GraderID_id', 'day')
data = Booking.objects.filter(actionTime__week_day__in=WeekEnds).select_related("FolderID", "GraderID").all()
data = data.extra(select={'day':'date( actionTime )', 'TotalWeekends':'COUNT(DISTINCT(date(actionTime)))'}).values('GraderID_id', 'TotalWeekends')
data
print data.query


    .values('GraderID_id', 'date_visited').distinct().annotate(Count('date_visited'))



Booking.objects.filter.
    .extra({'date_visited': "date(actionTime)"})
    .values('date_visited')
    .distinct()
    .annotate(Count('date_visited'))


from django.db.models import Count, Avg
Booking.objects.annotate(num_authors=Count('authors')).aggregate(Avg('num_authors'))

    .annotate(num_authors=count('authors')
            
Booking.objects.filter(GraderID_id=289, actionTime__week_day__in=weekdays).select_related("FolderID", "GraderID")\
    .values('GraderID_id','actionTime')\
    .aggregate(Count(connection.ops.date_trunc_sql('day', 'actionTime')))

aggregate(Count('entry'))




#************************************************************
#+ http://agiliq.com/blog/2009/08/django-aggregation-tutorial/
#************************************************************
#d
Booking.objects.all().annotate(Count('GraderID'))
#If you are only interested in name of department and employee count for it, you can do, 
#Department.objects.values('dept_name').annotate(Count('employee'))
Booking.objects.values('actionTime').annotate(Count('GraderID'))

''' OK- Graders per Date '''
Booking.objects.extra(select={'date':'date( actionTime )',}).values('date',).annotate(Count('GraderID'))

''' OK- Graders per Date '''
#Which combination of Employee and Deparments employes the most people
#We can order on the annotated fields, so the last query is modified to,
#Employee.objects.values('department__dept_name', 'level__level_name').annotate(employee_count = Count('id')).order_by('-employee_count')[:1]

Booking.objects.extra(select={'date':'date( actionTime )',}).values('date',).annotate(Count('GraderID'))
Booking.objects.values('GraderID__TeacherID_id', 'level__level_name').annotate(employee_count = Count('id')).order_by('-employee_count')[:1]


#Which employee name is the most common.


#************************************************************
#
#************************************************************
from django.db import models
.annotate(Count('date_visited'))\

#.annotate(num=models.Sum(models.Case(models.When(actionTime__week_day__in=weekdays,then=1,),default=0,output_field=models.IntegerField(),)))\
qs = Booking.objects\
    .extra(select={'date':'date( actionTime )',})\
    .values('date','GraderID',).distinct()\
    .annotate(Count('GraderID'))\
    .order_by('GraderID')
qs

qs.values('GraderID',).annotate(Count('GraderID'))


for d in data:
    print d.num_books, 





#************************************************************
# RAW SQL HMERES ERGASIAS + SK ERGASIAS
#************************************************************
''' IS OK - SYNOLO HMERES ERGASIAS '''
#GraderID__TeacherID__surname, GraderID__TeacherID__name, 
SQL='SELECT personel_booking.id, GraderID_id, personel_teacher.name AS TeacherName, personel_teacher.surname AS TeacherSurname, ' 
SQL+='Date(actionTime) AS Day , Count(Distinct(Date(actionTime))) AS TotalDays '
SQL+='FROM personel_booking INNER JOIN personel_grader ON personel_booking.GraderID_id=personel_grader.id '
SQL+='INNER JOIN personel_teacher ON personel_grader.TeacherID_id=personel_teacher.id '
SQL+='GROUP BY GraderID_id;'
raw = Booking.objects.raw(SQL)
for r in raw: 
    print r.GraderID_id, r.TeacherSurname, r.TeacherName, r.TotalDays





#************************************************************
#CONNECTIONS.ops
# EIKONA ERGASIAS + HMERA / OLOI BATHMOLOGHTES (SYGKENTRVTIKA)
#************************************************************
#PLATFOM Specific/
#Django 1.09 and below
from django.db import connection
from django.db.models import Sum, Count
import itertools
from itertools import groupby

truncate_date = connection.ops.date_trunc_sql('day', 'actionTime')
Booking.objects.extra({'day':truncate_date}).values('GraderID', 'day').annotate(Count('GraderID'))
#{'GraderID__count': 6, 'day': u'2016-09-24'}]


#distinct_fieldname
#results = Attachments.objects.filter(currency='current').values('filename').annotate(num_attachments=Count('article_id')).order_by("num_attachments")
truncate_date = connection.ops.date_trunc_sql('day', 'actionTime')
Booking.objects.extra({'day':truncate_date}).values('day').annotate(Count('GraderID')) 



def extract_date(entity):
    'extracts the starting date from an entity'
    return entity.actionTime.date()



entities = Booking.objects.order_by('actionTime')
list_of_lists = [list(g) for t, g in groupby(entities, key=extract_date)]
list_of_lists

for l in list_of_lists:
    print l.GraderID, l.actionTime.date()

from django.db.models.aggregates import Count
jobs = Job.objects.filter(date_added__gte=last_14_days).extra({"day": "date_trunc('day', date_added)"}).values("day").order_by().annotate(count=Count("id"))
#[{'count': 1423, 'day': datetime.datetime(2012, 2, 17, 0, 0)}, {'count': 147, 'day': datetime.datetime(2012, 2, 11, 0, 0)}, {'count': 1351, 'day': datetime.datetime(2012, 2, 20, 0, 0)}, {'count': 1665, 'day': datetime.datetime(2012, 2, 16, 0, 0)}, {'count': 1774, 'day': datetime.datetime(2012, 2, 15, 0, 0)}, {'count': 200, 'day': datetime.datetime(2012, 2, 19, 0, 0)}, {'count': 157, 'day': datetime.datetime(2012, 2, 18, 0, 0)}, {'count': 1, 'day': datetime.datetime(2012, 2, 22, 0, 0)}, {'count': 958, 'day': datetime.datetime(2012, 2, 10, 0, 0)}, {'count': 1503, 'day': datetime.datetime(2012, 2, 21, 0, 0)}, {'count': 1635, 'day': datetime.datetime(2012, 2, 13, 0, 0)}, {'count': 1533, 'day': datetime.datetime(2012, 2, 14, 0, 0)}, {'count': 170, 'day': datetime.datetime(2012, 2, 12, 0, 0)}]    


#************************************************************
# EIKONA ERGASIAS + MHNA / OLOI BATHMOLOGHTES (SYGKENTRVTIKA)
#************************************************************
truncate_date = connection.ops.date_trunc_sql('month', 'actionTime')
Booking.objects.extra({'month':truncate_date}).values('month').annotate(Count('GraderID')) 
#[{'GraderID__count': 8, 'month': u'2016-09-01'}]

#************************************************************
#PLATFOM Specific/
#Django 1.10 and above
#************************************************************
from django.db.models.functions import TruncMonth
Booking.objects.all().annotate(month=TruncMonth('actionTime'))\
        .values('month')\
        .annotate(c=Count('GraderID')).values('month', 'c')



#************************************************************
#kinisi Hmeras / AA
#************************************************************
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
#************************************************************
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
#************************************************************
Booking.objects.filter( GraderID=46, station=0, action=0 ).values().annotate(countAction=Count('action')).order_by('action')
#[{'actionTime': datetime.datetime(2016, 9, 23, 14, 51, 7), u'GraderID_id': 46, 'countAction': 1, 'station': 0, 'action': 0, u'id': 16, u'FolderID_id': 1}]
#Booking.objects.filter( GraderID=46, station=0, action=0 ).values('action', 'station', 'GraderID', ).annotate(countAction=Count('action')).order_by('action')


#************************************************************
# FAKELOUS POY EDVSE ΠΙΣΩ
#************************************************************
Booking.objects.filter( GraderID=46, station=0, action=1 ).values('GraderID', 'station', 'action').annotate(countAction=Count('action')).order_by('action')
#[{'actionTime': datetime.datetime(2016, 9, 24, 4, 34, 57), u'GraderID_id': 46, 'countAction': 1, 'station': 0, 'action': 1, u'id': 25, u'FolderID_id': 1}]

#************************************************************
# EIKONA ERGASIAS / OLOI BATHMOLOGHTES (ANALYTIKA)
#************************************************************
Booking.objects.all().values('action', 'station', 'GraderID').order_by('GraderID', 'station', 'action' )
#[{'action': 0, 'station': 0, 'GraderID': 46}, {'action': 1, 'station': 0, 'GraderID': 46}, {'action': 0, 'station': 1, 'GraderID': 46}, {'action': 0, 'station': 1, 'GraderID': 46}, {'action': 0, 'station': 1, 'GraderID': 46}, {'action': 1, 'station': 1, 'GraderID': 46}, {'action': 1, 'station': 1, 'GraderID': 46}, {'action': 1, 'station': 1, 'GraderID': 46}]


#************************************************************
# EIKONA ERGASIAS / OLOI BATHMOLOGHTES (SYGKENTRVTIKA)
Booking.objects.all().values('GraderID', 'station', 'action').annotate(countAction=Count('GraderID'))
#************************************************************
#[{'action': 0, 'station': 0, 'countAction': 1, 'GraderID': 46}, 
#{'action': 1, 'station': 0, 'countAction': 1, 'GraderID': 46}, 
#{'action': 0, 'station': 1, 'countAction': 3, 'GraderID': 46}, 
#{'action': 1, 'station': 1, 'countAction': 3, 'GraderID': 46}]


#************************************************************
# EIKONA ERGASIAS + HMERA / OLOI BATHMOLOGHTES (ANALYTIKA)
#************************************************************
Booking.objects.all().values('action', 'station', 'actionTime', 'GraderID').order_by('GraderID', 'actionTime' )
#[{'action': 0, 'station': 0, 'GraderID': 46, 'actionTime': datetime.datetime(2016, 9, 23, 14, 51, 7)},

Booking.objects.all().values('action', 'station', 'actionTime', 'GraderID').order_by('GraderID', 'actionTime' )


#************************************************************
# fakelous poy edvse + folder info
#************************************************************
BookingJoinTables.objects.filter( graderid=46, station=0, action=1, )\
        .values('graderid', 'folderid__no', 'station', 'action')\
        .annotate(countaction=count('action')).order_by('action')
#[{'actiontime': datetime.datetime(2016, 9, 24, 4, 34, 57), u'graderid_id': 46, 'countaction': 1, 'station': 0, 'action': 1, u'id': 25, u'folderid_id': 1}]


BookingJoinTables().filter( GraderID=46, station=0, action=1)\
        .values('GraderID', 'GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 'FolderID__no', 'station', 'action')\
        .annotate(countaction=Count('action')).order_by('action')


#************************************************************
# eikona ergasias ana bathmologhth (sygkentrvtika)
#************************************************************
BookingJoinTables.objects.filter( graderid=46, station=0, action=1 )\
        .values('graderid')\
        .annotate(countaction=count('graderid'))


