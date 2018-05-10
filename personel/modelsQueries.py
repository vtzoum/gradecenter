#!/usr/bin/env python
# -*- coding: utf-8 -*-

#python manage.py shell

from personel.models import * 
from personel.helpScripts import * 

'''
SOS Field DEPENDENCIES in MODELS 

class Meta:
    unique_together = (('first_name', 'last_name'),)
'''

#////////////////////////
# from django.contrib.auth.models import User
# User
#////////////////////////
from django.contrib.auth.models import User
user = User.objects.get(username='vtzoum')
print user.id
2

user = User.objects.get(id=1)
print user.id
1

# Where 'request' obj. is avail
user = request.user
gta = Game.objects.create(name="gta", owner=user)

#////////////////////////
# ACCEPTANCE > RELATION M:N 
#////////////////////////
Acceptance.objects.all().values()
Acceptance.objects.filter(id=4).values()
a = Acceptance.objects.get(id=)

Lesson.objects.get(id=4)
Lesson.objects.filter(id=4).values()

SchoolToGrade.objects.get(id=1)
SchoolToGrade.objects.all().values()
SchoolToGrade.objects.filter(id=1).values()

l = Lesson.objects.get(id=4)
s = SchoolToGrade.objects.get(id=1)
a= Acceptance(LessonID = l , SchoolToGradeID = s, )
a.save()
    #books = , booksAbscent = , booksZero = ,   status = ,  statusTime = , )
    a = Acceptance ( LessonID = self , SchoolToGradeID = s ) #,  books = , booksAbscent = , booksZero = , status = ,  statusTime = , )

#Start 
l = Lesson.objects.get(id=4)
for a in Acceptance.objects.filter(LessonID = l):
    if a.books == 0:
        a.books = 10
        a.save()

for a in Acceptance.objects.filter(LessonID = l):
    if (a.status == 0) and (a.books != 0):
        a.status = 1
        a.save()
#End 


#////////////////////////
# BOOKING > RELATION M:N 
#////////////////////////
f = Folder.objects.get( id = 1)    
g = Grader.objects.get(id=1)
u = User.objects.get(id=3)
actionTime = datetime.datetime.now()
timeDelta = datetime.timedelta(minutes=1)
for i in range (2,50000):
    action = i%2
    actionTime += timeDelta 
    Booking (FolderID = f , GraderID = g, action = action, station = 1, operator=u, actionTime=actionTime).save()
    print i, action, actionTime 

#OK
l = Lesson.objects.get(id=4)        # 
f = Folder.objects.get( id = 1)  # ΒΙΟΛΟΓΙΑ - Φ1
g = Grader.objects.get(id=46)       # ΑΘΑΝΑΣΟΠΟΥΛΟΥ
reg0 = Booking ( FolderID = f , GraderID = g, action= 0, station = 0, )
reg0.save()
#OK
Booking.objects.all().values()
Booking.objects.filter( GraderID = g).all().values()   
Booking.objects.filter( GraderID = 46).all().values()



#////////////////////////
# FOLDER 
#////////////////////////
#RELATED > 
Folder.objects.get(id=1).bookings.all()       # Grader
Grader.objects.get(id=46).folder_set.all()
Grader.objects.get(id=46).folder_set.all().values()


#////////////////////////
# GRADER
#////////////////////////
#RELATED > 
Grader.objects.get(id=46).folder_set.all()
Grader.objects.get(id=46).folder_set.all().values()
Grader.objects.get(id=46).booking_set.all().values()

Grader.objects.filter(LessonID__id=9)[0].booking_set.filter(action=0, station=0).values()

gs = Grader.objects.filter(LessonID__id=9)

for g in gs: 
    z = g.booking_set.filter(action=0, station=0).annotate(countCodeType=Count('id'))#
    #z = g.booking_set.filter(action=0, station=0).values()      # OK
    print g.id, g.TeacherID.surname
    if len(z) > 0:
        print z[0].countCodeType, 
    else:
        print 0, 

    

        g = data.booking_set.filter(action=0, station=0)
        print g
        g1 = g.annotate(countCodeType=Count('id'))
            
        print g1

        #write cell data
        worksheet_s.write_number(row, 0, idx + 1, cellC_STYLE)
        
        #val = data.LessonID.name
        val = 'LESSON'
        #print val 
        worksheet_s.write_string(row, 1, val, cell_STYLE)        


        #val = data['FolderID__LessonID__name']
        val = str(g1['GraderID__id'])



#Grader.objects.raw("SELECT Grader.* FROM Grader LEFT OUTER JOIN Booking ON (Grader.id = Booking.GraderID_id AND foo.user_id = %s)", [request.user.id])
#OK
qsRaw = Grader.objects.raw("SELECT personel_grader.*, personel_booking.* FROM personel_grader LEFT OUTER JOIN personel_booking ON (personel_grader.id = personel_booking.GraderID_id) WHERE (station=0) AND (action =1) ;")
for o in qsRaw: 
    print o.id, #o.station

b = Blog.objects.get(id=1)
e = Entry.objects.get(id=234)


# List of Objects
gList = Grader.objects.filter(LessonID__id=9)
#new_list = [obj1, obj2, obj3]
e.related_set.set(new_lis)




#////////////////////////
# BOOKING 
#////////////////////////
Grader.objects.get(id=46).booking_set.all().values()
#RELATED > select_related 
Booking.objects.select_related('GraderID').get(id=1)                           #Booking
Booking.objects.select_related('GraderID').get(id=1).GraderID.status           #OK
Booking.objects.select_related('GraderID').filter(status=0)[0].GraderID.id     #OK
Booking.objects.select_related('GraderID').all()[0].GraderID                   # Grader


#SERIALIZERS
brelObj = Booking.objects.select_related('GraderID').get(id=2)     # instance
serializers.serialize('json', brel, use_natural_foreign_keys=True, use_natural_primary_keys=True)

brelSet = Booking.objects.select_related('GraderID')        # set
object_dict = {id(x): b.FolderID for b in brelSet}
#print [ b.FolderID for b in brelSet]                       # OK

bJSON = serializers.serialize('json', brelSet, use_natural_foreign_keys=True, use_natural_primary_keys=True)
fJSON = serializers.serialize('json', [ b.FolderID for b in brelSet], use_natural_foreign_keys=True, use_natural_primary_keys=True)

#FIELDNAMES
print list(brelSet) + [x.FolderID for x in brelSet if x.FolderID not in brelSet]
print brelSet.values()      # dict
print [x.FolderID for x in brelSet]
# FIELD NAMES
#get_all_field_names()
for f in Folder._meta.get_all_field_names():
    

#{ k: v    for d in l for k, v in d.items() }
#print { k: v for i in brelset for k, v in i.items() }
#{ k: v for thedict in thedicts for k, v in thedict.items() }
'''
import json
#print jsondata
bjson = json.dumps(list(brel), default=date_handler)  # handle datetime json ser.
fjson = json.dumps( [ b.folderid for b in brel] ,  default=date_handler)
'''


#************************************************************
#BOOKING DURATION
now = datetime.datetime.now()
dayFlag = datetime.timedelta(days=3)
pastDate = now - dayFlag

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



print "One day in the future is:", now + difference1
#=> One day in the future is: 2003-08-07

print "Two weeks in the past is:", now + difference2
#=> Two weeks in the past is: 2003-07-23

print datetime.date(2003, 8, 6) - datetime.date(2000, 8, 6)




"""
"""
# booking logic helpers
def graderisowneroffolder (folderid=none, graderid=none):
    
    f = folder.objects.get( id = folderid)
    g = grader.objects.get(id=graderid)
    if g.currentfolder == f.id:
        return true        
    else: 
        return false
    #pass

"""
"""
def graderwasowneroffolder (folderid=none, graderid=none):
    f = folder.objects.get( id = folderid)
    g = grader.objects.get(id=graderid)
    # exists previous αποθηκη(εισοδοσ, φακελοσ, βαθμολογ)
    if booking.objects.filter(station=0, action=1, folderid=folderid, graderid=graderid ).count()==1:
        return true
    else: 
        return false


# booking logic
#def dobooking (station=none, action=none, f=none):
"""
check arguments and change folder status (and insert booking)
"""
"""
def dobooking (station=none, action=none, folderid=none, graderid=none):

    f = folder.objects.get( id = folderid)
    g = grader.objects.get(id=graderid)
    
    #αποθηκη
    if station == 0:

        if f.status == 0 and action == 0:                   # folderis(idle)+action(out)
            if g.currentfolder is not none:                 # grader is not available
                print "error: grader is not available!"
            elif graderwasowneroffolder (f.id, g.id):       # grader was owner
                print "error: grader was owner!"
            elif f.type==2 and not g.isgraderc:             # folder = c and grader not allowed
                print "error: grader not allowed to grade c folder!"
            else:                                           # pass
                # make booking
                print "make booking"
                booking (folderid = f , graderid = g, action = action, station = station ).save()
                f.status = 1
                f.save()
                g.currentfolder = f.id 
                g.save()
                print 'station(%s) action(%s) folder status(%s)' % ('αποθήκη', 'χρέωση', '1-out')
                #break
        elif f.status == 1 and action == 1:         # folderis(out)+action(in)
            if g.currentfolder != f.id:             # grader not owner
                print "error: grader is not owner of folder !"
            else:                                           #pass
                print "make booking"
                # make booking
                booking (folderid = f , graderid = g, action = action, station = station ).save()
                g.currentfolder = none  # grader release
                g.save()
                if f.type == 0: #a
                    f.type = 1                          # folder type a-> b
                    f.status = 0                        # folder return 
                    f.save()                            # folder type a-> b
                    print 'station(%s) action(%s) folder status(%s)' % ('αποθήκη', 'παραλαβή', '3-return')
                    #break
                else: 
                    f.status = 4                        # folder complete
                    f.save()                            # folder type a-> b
                    print 'station(%s) action(%s) folder status(%s)' % ('αποθήκη', 'παραλαβή', '3-return')
        else:
            print "error in station 0."
    
    #φυλαξη
    if station == 1:
        if f.status == 1 and action == 1:
            if g.currentfolder != f.id:
                print "error. grader is not owner of folder !"
            else:
                # make booking
                booking (folderid = f , graderid = g, action = action, station = station ).save()
                f.status = 2                # folder save
                f.save()
                print 'station(%s) action(%s) folder status(%s)' % ('φύλαξη', 'παραλαβή', '2-save')
        elif f.status == 2 and action == 0:     # folderis(save)+action(out)
            if g.currentfolder != f.id:         # grader not owner
                print "error. grader is not owner of folder !"
            else:                               # pass
                # make booking
                booking (folderid = f , graderid = g, action = action, station = station ).save()
                f.status = 1                        # folder out
                f.save()                            # folder out
                print 'station(%s) action(%s) folder status(%s)' % ('φύλαξη', 'παράδοση', '1-out')
        else:   # unauthorised
            print "error in station 1"


"""


#def dobooking (station=none, action=none, f=none):
"""
check arguments and change folder status (and insert booking)
"""
"""
def dobookingv1 (station=none, action=none, folderid=none, graderid=none):

    f = folder.objects.get( id = folderid)
    g = grader.objects.get(id=graderid)
    #αποθηκη
    if station == 0:
        if f.status == 0 and action == 0:   # folderis(idle)+action(out)
            if g.currentfolder is none:     # grader is available
                print "grader is available!"
                # make booking
                booking (folderid = f , graderid = g, action = action, station = station ).save()
                f.status = 1
                f.save()
                g.currentfolder = f.id 
                g.save()
                print 'station(%s) action(%s) folder status(%s)' % ('αποθήκη', 'χρέωση', '1-out')
                #break
            else: 
                print "error: grader not available!"
        elif f.status == 1 and action == 1: # folderis(out)+action(in)
            if g.currentfolder == f.id:
                print "grader is owner of folder !"
                #break
                # make booking
                booking (folderid = f , graderid = g, action = action, station = station ).save()
                g.currentfolder = none  # grader release
                g.save()
                if f.type == 0: #a
                    f.type = 1                          # folder type a-> b
                    f.status = 0                        # folder return 
                    f.save()                            # folder type a-> b
                    print 'station(%s) action(%s) folder status(%s)' % ('αποθήκη', 'παραλαβή', '3-return')
                    #break
                else: 
                    f.status = 4                        # folder complete
                    f.save()                            # folder type a-> b
                    print 'station(%s) action(%s) folder status(%s)' % ('αποθήκη', 'παραλαβή', '3-return')
                    #break
            else: 
                print "error: grader not owner!"
        else: 
            print "error in station 0."
            #break
        
    #φυλαξη
    if station == 1: 
        if f.status == 1 and action == 1: # folderis(out)+action(in)
            if g.currentfolder == f.id:
                print "error. grader is owner of folder !"
                #break
                # make booking
                booking (folderid = f , graderid = g, action = action, station = station ).save()
                f.status = 2                # folder save
                f.save()       
                print 'station(%s) action(%s) folder status(%s)' % ('φύλαξη', 'παραλαβή', '2-save')
                #break
            else:
                print "error. grader not owner of folder !"
        
        elif f.status == 2 and action == 0: # folderis(save)+action(out)
            if g.currentfolder == f.id:
                print "error. grader is owner of folder !"
                #break
                # make booking
                booking (folderid = f , graderid = g, action = action, station = station ).save()
                f.status = 1                        # folder out
                f.save()                            # folder out
                print 'station(%s) action(%s) folder status(%s)' % ('φύλαξη', 'παράδοση', '1-out')
                #break
            else:
                print "error. grader not owner of folder !"
        
        else:   # unauthorised
            print "error in station 1"
            #break
            
"""


""" run the tests """
f = folder.objects.get( id = 1)     # βιολογια - φ1
g = grader.objects.get(id=46)       # αθανασοπουλου
#dobooking (station=none, action=none, folderid=none, graderid=none):
dobooking (0, 0, 1, 46)     # xrewsi
dobooking (0, 0, 1, 46)     # xrewsi pali is error 
dobooking (1, 1, 1, 47)     # filaksi:paradosi:notowner: is error 
dobooking (1, 1, 1, 46)     # filaksi:paradosi:owner: ok 
dobooking (0, 1, 1, 46)     # apothiki:paralavi:owner: error (is in filaksi)
dobooking (1, 0, 1, 47)     # filaksi:paralavi:notowner: is error 
dobooking (1, 0, 1, 46)     # filaksi:paralavi:owner: ok 
dobooking (0, 1, 1, 46)     # apothiki:paralavi:owner: ok now


#test
print graderwasowneroffolder (1, 46)  # wasowner is true


'''
for g in booking.objects.select_related('graderid').all():
    #print g.graderid.objects.select_related('lessonid')    #fail
    print g.graderid.objects.select_related('lessonid')    #
    print g.graderid
'''


'''
location = models.positivesmallintegerfield(default=0, blank=false, null=false)   # 0: apoth , 1: filaksi
status = models.positivesmallintegerfield(default=0, blank=false, null=false)   # 0: idle , 1: out , 2: in 
actiontime = models.datetimefield(default=datetime.now, blank=true)
'''


#////////////////////////
# folders > relation 1:n 
#////////////////////////
lesson = Lesson.objects.get(id=4)
f = folder( lessonid = lesson , books = 25, no = 1, status = 0, type = 0, typechar = 'a',)
f.save()

for i in xrange(4): # make 4 folders
    f = folder( lessonid = lesson , books = 25, no = i + 1, status = 0, type = 0, typechar = 'a',)
    f.save()

# make 5 folder sfor history
lessonhistory = lesson.objects.get(id=5)
for i in xrange(5): # make 5 folders
    f = folder( lessonid = lessonhistory , books = 25, no = i + 1, status = 0, type = 0, typechar = 'a',)
    f.save()




Folder.objects.all().values()
l = Lesson.objects.get(id=4)
Folder.objects.filter( LessonID = l ).all().values()
#Folder.getNextNo(type = 0)
#maxNo = l.folder_set.filter(type = type).order_by("-no")[0] 

# maxNo is OK
l = Lesson.objects.get(id=4)
l.getNextFolderNo(type = 0)



Folder.objects.filter( LessonID = l ).all().values()

Folder.objects.filter( LessonID = 4 ).all().values('id', 'codeBarcode')


"""
for x in xrange(3):
    print x
    if x == 1:
        break
lessonid = models.foreignkey(lesson, on_delete=models.cascade)
bookcount = models.integerfield()
folderno = models.integerfield()
folderstatus = models.charfield(max_length=1)
isnow = models.charfield(max_length=1)
"""


#teacher.objects.create(author=me, title='sample title', text='test')
t.save()

lesson = lesson.objects.filter(id=4)
print lesson.values()
lesson.update(folders=127)

# make folders
foldersize = 25 
lesson = lesson.objects.get(id__exact=4)
books= lesson.folders
# make folders


books= 2
lastfoldercount = 0 
foldercount = books / foldersize
folderresidue = books % foldersize
print 'foldercount(%d) folderresidue(%d) lastfoldercount(%d)' % (foldercount, folderresidue, lastfoldercount)

# 2nd try
if (folderresidue <=2):
    if (foldercount != 0):
        lastfoldercount = foldersize + folderresidue
    else:
        foldercount += 1
        lastfoldercount = folderresidue
else: 
    foldercount += 1
    lastfoldercount = folderresidue

print 'foldercount(%d) folderresidue(%d) lastfoldercount(%d)' % (foldercount, folderresidue, lastfoldercount)




#////////////////////////
# MAKE FOLDER
#////////////////////////
def prepareGradingAB(booksAB):      #aka Make AB-Folders for Lesson
    """
    UPDATED 2018-04-30: Works as expected
    """
    folderCount = 0 
    folderSize = 25 
    folderSizeMargin = 4
    #folderSizeMargin = 2 
    
    bookCount = booksAB
    lastFolderSize = 0 
    folderCount = 0
        
    P = bookCount/20
    Y = bookCount%20
    
    folders=[]
    for i in range(0,P):
        folderCount=folderCount+1
        folders.append((folderCount,20))
        bookCount = booksAB-20*folderCount
        print 'BATCH NewFOLDER: folderCount(%d) thisFolderSize(%d) bookCount(%d)' % (folderCount, 20, bookCount)
    
    if P==0:
        folders.append((P+1,Y))
        folderCount=folderCount+1
        bookCount = bookCount - Y
        print 'MAKE New FOLDER: Y(%d) folderCount(%d) thisFolderSize(%d) bookCount(%d)' % (Y, folderCount, Y, bookCount)
    elif P>0 and Y<=folderSizeMargin:
        folders[folderCount-1]= (folders[folderCount-1][0], folders[folderCount-1][1]+Y)
        bookCount = bookCount - Y
        print 'UPDATE LAST FOLDER:  Y(%d) folderCount(%d) thisFolderSize(%d) bookCount(%d)' % (Y, folderCount, folders[folderCount-1][1], bookCount)
    elif P>0 and Y>folderSizeMargin:
        folderCount=folderCount+1
        bookCount = bookCount - Y   # must be 0 now 
        folders.append((folderCount+1,Y))
        print 'BATCH NewFOLDER:  Y(%d) folderCount(%d) thisFolderSize(%d) bookCount(%d)' % (Y, folderCount, Y, bookCount)
    else: 
        print 'UNKNOWN'


prepareGradingAB(4)
prepareGradingAB(5)
prepareGradingAB(20)
prepareGradingAB(24)
prepareGradingAB(25)
prepareGradingAB(30)
prepareGradingAB(60)



#////////////////////////
# relations m:n graders
#////////////////////////
from personel.models import * 
from personel.helpScripts import * 

lesson = Lesson.objects.filter(name__exact='βιολογια γ.π.')
lesson = Lesson.objects.filter(id=4)
print lesson.values()
teacher = teacher.objects.filter(surname__exact='τζουμάκας')
print teacher.values()

#prosoxi sta ellhnika-unicode. na dw ti ginetai 
# na dw ta __str__ k __unicode__ 
# get lesson, teachers are objects not querysets
#object
lesson.objects.get(id__exact=1)
teacher.objects.get(id__exact=1)
#>>> entry = entry.objects.get(pk=1)
# insert
grader = grader(lessonid = lesson, teacherid = teacher, ) 
grader.save() 
#iscoordinator = models.booleanfield(default=false)
#isgraderc = models.booleanfield(default=false)
#status = models.positivesmallintegerfield(default=0, blank=true, null=true)
######################################################
# m:n reference related objects
######################################################
# publication.objects.get(id=4).article_set.all()
teacher.objects.get(id=1).lesson_set.all()   # ok
teacher.objects.get(id=1).grader_set.all()   # ok
#>>> a2.publications.all()
lesson.objects.get(id=4).graders.all()       # ok
lesson.objects.get(id=4).teacher_set.all()       # ok

######################################################
# m:n reference related objects
######################################################
#querysets
grader.objects.all()    
grader.objects.all().values()

#######################
#objects
objg = grader.objects.get(id=1)
objt = grader.objects.get(id=1).teacherid
objg.update(objt)
print objg

#######################
#related objects

#related objects > select_related 
grader.objects.select_related('teacherid').all()[0].teacherid

objgt = grader.objects.select_related('teacherid').get(id=1)
grader.objects.select_related('teacherid').get(id=1).teacherid.name
grader.objects.select_related('teacherid').filter(status=1)[0].teacherid.name   #ok


#ok
grader.objects.select_related('teacherid').filter(status=1).all()
objgt = grader.objects.select_related('teacherid').filter(status=1)
[gt.teacherid.name for gt in objgt]


objgt = grader.objects.select_related('teacherid').only('teacherid__name','teacherid__surname', 'status')

lesson.objects.get(id=4).graders.all().values()   


#related objects > prefetch_related  
grader.objects.prefetch_related('teacherid').filter(status=1)[0].teacherid.name
objgt = grader.objects.prefetch_related('teacherid').filter(status=1)
[gt.teacherid for gt in objgt]

grader.objects.prefetch_related('teacherid').only('teacherid__name','teacherid__surname', 'status').get(id=1)


#######################
#record values
recg = grader.objects.filter(id=1).values()
rect = grader.objects.filter(id=1).values()[0]['teacherid_id']     # value

#recordsets/queryset
objg = grader.objects.filter(id=1)
#recg = grader.objects.get(id=1).teacherid
#recg = grader.objects.filter(id=1)
#valuest = teacher.objects.filter(id=1).teacher_set.values()
#valuesgt = objg.values().update(d1)




#1
#////////////////////////
# teachers
#////////////////////////
t = teacher(name='βασίλης', surname='τζουμάκας', codeafm = '10000000', codegrad = '02000000', codespec = 'πε19-01',)
#teacher.objects.create(author=me, title='sample title', text='test')
t.save()
"""
t1 = teacher.objects.get(pk=1)
#cheese_blog = blog.objects.get(name="cheddar talk")
#>> entry.blog = cheese_blog
t1.codespec = 'πε19-01'
t1.save()
"""
#queryset
teacher.objects.all()    
teacher.objects.filter(id=1)
teacher.objects.filter(id=1).values()
teacher.objects.filter(name__contains='βασ')

teacher.objects.order_by('name')        #asc
teacher.objects.order_by('-name')       #desc

teacher.objects.filter(name__contains='βασ').order_by('codespec')

# exclude
teacher.objects.exclude(name__contains='βασ')
teacher.objects.exclude(id__in=[1,2,3,4,5])




#////////////////////////
# lessons
#////////////////////////
from personel.models import * 
from personel.helpScripts import * 

Lesson.objects.all()
lesson(name ='μαθηματικα κατευθυνσησ',).save()
#lesson(name ='αρχαια ελληνικα κατευθυνσησ',).save()


Folder.objects.filter( LessonID = 4 ).all().values('id', 'codeBarcode')


for lessonname in [ 'βιολογια γ.π.','ιστορια γ.π.', 'μαθηματικα και στοιχεια στατιστικησ γ.π.', 'νεοελληνικη γλωσσα γ.π.', 'αρχαια ελληνικα ο.π.', 'ιστορια ο.π.','λατινικα ο.π.', 'βιολογια ο.π.', 'μαθηματικα ο.π.', 'φυσικη	ο.π.','χημεια ο.π.', 'αρχεσ οικονομικησ θεωριασ ο.π.','αναπτυξη εφαρμογων σε π.π. ο.π.',]:
    lesson(name = lessonname).save()

#Traversal LESSON 
for x in lesson.objects.all(): 
    if x.id < 3: 
        x.delete()
for x in lesson.objects.all(): 
    print x.name, 

# exclude
lesson.objects.exclude(name__contains='γ.π.')
lesson.objects.exclude(name__contains='ο.π.')

# update
l = lesson.objects.exclude(name__contains='γ.π.')
lesson.objects.exclude(name__contains='ο.π.')

#SET
l1= Lesson.objects.filter(pk=4)
l1.values()
Lesson.folder_set
Folder.filter(LessonID=4).all()

#BARCODES
Lesson.objects.get(pk=4).makeBarcodes()

#Fodler traversal 
id=4
for f in Folder.objects.filter(LessonID=4):
    print f.codeBarcode
    f.codeBarcode = 'a'
    f.save()
    print f.codeBarcode
    print '%04d-%010d' %(id, f.id)

Lesson.FolderID.all()


for f in Folder.lesson_set.objects.all():
    print 'foo'

#////////////////////////
#school
#////////////////////////
s0 = school(name ='παπαστρατειο γυμνασιο αγρινιου', stype = 1, )
s0.save()

