import datetime
from django.db.models import IntegerField, DurationField 
from django.db.models import ExpressionWrapper, Func, F
from django.db.models.functions import Length, Upper
from django.db.models import Avg, Count, Max, Sum

data = Booking.objects.filter(GraderID__id=289, actionTime__week_day__in=[1,7]).select_related("FolderID", "GraderID").all()
data = data.extra(select={'day':'date(actionTime)'}).values('GraderID_id', 'GraderID__LessonID__name', 'GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 'day').annotate(actionDurationINTEGER=ExpressionWrapper( F('actionDuration'), output_field=IntegerField()))

for d in data: 
    print d['day'], d['GraderID__TeacherID__surname'], d['actionDurationINTEGER'], 
    if d['actionDurationINTEGER']: 
        t0= datetime.timedelta(microseconds=d['actionDurationINTEGER'])
        print t0

            .annotate(available=Count('actionTime')).annotate(sumDuration=Sum('actionDurationINTEGER'))
            .order_by('day', 'GraderID__LessonID','GraderID',)
            #.annotate(available=Count('actionTime')).annotate(sumDuration=Sum('actionDuration'))\

Booking.objects.annotate(
    total_items=Count('actionTime'),
    published=Sum('actionDuration', output_field=IntegerField() ),
)

Booking.objects.annotate(
    total_items=Count('items'),
    published=Sum(Case(When(items__published=True, then=1), output_field=IntegerField())),
    foo=Sum(Case(When(
        Q(history__action__name='argle') | Q(history__action__name='bargle'),
        history__since__lte=now,
        history__until__gte=now,
        then=1
    ), output_field=IntegerField()))
)

#####################################################
# 2nd TRY
#####################################################
data0 = Booking.objects.filter(GraderID__id=289, actionTime__week_day__in=[1,7]).annotate(
    total_items=Count('actionTime'),
    actionDurationINTEGER=Sum('actionDuration', output_field=IntegerField() ),
)

for d in data0: 
    print d.actionDuration

    if d['actionDurationINTEGER']: 
        t0= datetime.timedelta(microseconds=d['actionDurationINTEGER'])
        print t0
#####################################################
# 3rd TRY # MIGHT BE SUCCESS
#####################################################
from django.db.models import CharField, Case, Value, When

rs = Booking.objects.filter(GraderID__id=289, actionTime__week_day__in=[1,7]).extra(select={'day':'date(actionTime)'}).annotate(actionDuration1=ExpressionWrapper( F('actionDuration'), output_field=IntegerField())).order_by('-actionTime')
rs = rs.filter(actionDuration1__isnull=False).values('day','actionDuration1').annotate(dur1=Sum('actionDuration1')).annotate(available=Count('actionTime'))

for d in rs: 	
    print d['day'], d['available'], d['dur1']
    
rs1 = rs0.filter(actionDurationINTEGER__isnull=True)values('day', 'actionDurationINTEGER').annotate(dur=Sum(Case(When(actionDurationINTEGER__isnull=False, then='actionDurationINTEGER'), output_field=IntegerField() ) ))	
##############################################
#VAR
##############################################
class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'

Booking.objects.all().aggregate(Round(Sum('actionDuration')))
Booking.objects.values(Round('actionDuration'))
Booking.objects.all().aggregate(latest=Round(Func(F('actionDuration'), _field=IntegerField())))

4227823333.9999995
4227823334
4227823381
##############################################
#BOOKING INSERT TO VALIDATE DURATION
##############################################
#ERRONEOUS DB VALUES / SQLITE makes bigint to floats at 1% of time
"1580","0","0","328","289","22",,"0","2017-06-15 11:43:19.019649"
"1650","1","1","328","289","23","5239058051","0","2017-06-15 13:10:38.077708"
"1797","0","1","328","289","23",,"0","2017-06-15 16:57:24.104082"
"1950","1","1","328","289","23","13728155041","0","2017-06-15 20:46:12.259131"
"2278","0","1","328","289","23",,"0","2017-06-16 17:12:08.637065"
"2305","1","0","328","289","22","1594083798","0","2017-06-16 17:38:42.720910"
"2307","0","0","310","289","22",,"1","2017-06-16 17:39:54.350637"
"2331","1","1","310","289","23","2136682836.9999998","1","2017-06-16 18:15:31.033481"
"2638","0","1","310","289","23",,"1","2017-06-17 09:05:04.248152"
"2841","1","1","310","289","23","12077590255","1","2017-06-17 12:26:21.838415"
"3327","0","1","310","289","23",,"1","2017-06-18 08:01:47.815500"
"3418","1","0","310","289","22","4227823333.9999995","1","2017-06-18 09:12:15.638881"     # ERROR HERE

# TRY TO REPRODUCE PROBLEM HERE
import datetime
from django.contrib.auth.models import User

f = Folder.objects.get( id = 1)
g = Grader.objects.get(id=1)
u = User.objects.get(id=11)
INSERT INTO "someTable" VALUES ("2257","1","1","137","81","23","17138060785.000002","0","2017-06-16 16:47:57.206638");
#t0 = datetime.datetime.now()
t0 = datetime.datetime.strptime("2017-06-18 08:01:47.815500", "%Y-%m-%d %H:%M:%S.%f")
t1 = datetime.datetime.strptime("2017-06-18 09:12:15.638881", "%Y-%m-%d %H:%M:%S.%f")
tdur=t1-t0
tdur 

Booking (FolderID = f , GraderID = g, action = 0, station = 0, wasTypeOf= 1, operator=u, actionTime=datetime.datetime.now(), actionDuration=tdur).save()                    

#crop microseconds IN CASE this makes the problem 
t0NIMICRO=t0.replace(microsecond=0)
t1NIMICRO=t1.replace(microsecond=0)
tdurNOMICRO=t1NIMICRO-t0NIMICRO

Booking (FolderID

SELECT id, actionDuration, round(actionDuration) FROM personel_booking
where GraderID_Id=289;

UPDATE  personel_booking
SET actionDuration= round(actionDuration) 
where GraderID_Id=289 and id=3418;

rs = Booking.objects.all.extra(select={
    'for_date': 'CONCAT(CONCAT(extract( YEAR from for_date ), "-"),
        LPAD(extract(MONTH from for_date), 2, "00"))'
    }).values('for_date').annotate(price=Avg('price')).order_by('-for_date')


user_list = Booking.objects.annotate(
    rating=Avg('userrating__rating', output_field=IntegerField()))

Booking.objects.filter(GraderID=289).annotate(act=ExpressionWrapper( F('actionDuration'), output_field=IntegerField()))

expires=ExpressionWrapper( F('active_at'), output_field=DateTimeField()))

Booking.objects.annotate(actionDurationROUNDED=F('actionDuration'))

class Lower(Func):
    function = 'LOWER'
    
class Round(Func):
    function = 'ROUND'
queryset.annotate(field_lower=Lower('field'))

booking = Booking.objects.get(id=2331)
booking.actionDuration = F('actionDuration')+1
booking.save()

Booking.objects.all().update(actionDuration=F('actionDuration') + 1)

weekends=[1,7]
    """
    data = Booking.objects.filter(actionTime__week_day__in=weekdays).select_related("FolderID", "GraderID")\
         .values('GraderID__LessonID__name',
                            'GraderID_id', 'GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 
                            'actionTime'
                            )\
         .extra(select={'day':'date( actionTime )'})\
            .annotate(countTimes=Count('actionTime'))\
            .annotate(sumDuration=Sum('actionDuration'))\
            .order_by('GraderID__LessonID','GraderID','day',)\
            .values('GraderID__LessonID__name',
                    'GraderID_id', 'GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 
                    'sumDuration', 'countTimes',
                    )
            #.order_by('GraderID__LessonID', 'GraderID','actionTime',)
            #.values('GraderID__LessonID', 'GraderID','actionTime',)\
    """
data = Booking.objects.filter(actionTime__week_day__in=weekends).select_related("FolderID", "GraderID").all()
data = data.extra(select={'day':'date( actionTime )'}).values('GraderID_id', 'GraderID__LessonID__name', 'GraderID__TeacherID__surname', 'GraderID__TeacherID__name', 'day').annotate(available=Count('actionTime')).annotate(sumDuration=Sum('actionDuration')).order_by('day', 'GraderID__LessonID','GraderID',)

    #print "days (%2.2f) hours (%0.2f) minutes (%0.2f)" %(td.days, td.seconds//3600, (td.seconds//60)%60)
    print data    


