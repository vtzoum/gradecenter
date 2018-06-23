#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime    
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime    
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.models import User

from django.db import DatabaseError, IntegrityError, transaction

#from helpScripts import helperMessageLog
# Create your models here.

#Date: 2017-May 
""" """
def helperMessageLog(request, msg='Null log', tag='info'):
    """
    Handles 3to1 statements for ajax messages & logging
    """
    if tag=='error':
        messages.error(request, msg, tag, fail_silently=True)
    elif tag=='info':
        messages.info(request, msg, tag, fail_silently=True)
    elif tag=='success':
        messages.warning(request, msg, tag, fail_silently=True)
    elif tag=='success':
        messages.warning(request, msg, tag, fail_silently=True)
    else: 
        messages.info(request, msg, tag, fail_silently=True)
    print msg


###################################
# GLOBALS to CHECK  for Use in Classes
###################################
FOLDER_TYPE = ( (0, u'Φ(Α)'), (1, u'Φ(Β)'),(2, u'Φ(ΑΝΑ)'), )


###################################
# CG Information
#UPD: 2018-04
###################################
"""
FIELDS: [folderBooks, minFolderBooks, maxActionDuration, 
name, article, presidentName, presidentSurname,     
phone, ]
"""
class GradeCenterInfo(models.Model):

    #Grading Folders
    folderBooks= models.SmallIntegerField(null = False, default=25) #books/folder    (eg. full folder has 25 books)
    minFolderBooks= models.SmallIntegerField(null = False, default=4)           #books    (eg. folder has at least 4 books)
    maxActionDuration=models.SmallIntegerField(null = False, default=3)         #days     (eg. keep folder max 3 days)

    #Reporting
    name=models.CharField(max_length=24, default=u'43ο ΒΚ ΑΓΡΙΝΙΟY')
    article=models.CharField(max_length=2, default=u'o')
    presidentName=models.CharField(max_length=24, default=u'ΒΑΣΙΛΕΙΟΣ')
    presidentSurname=models.CharField(max_length=16, default=u'ΤΖΟΥΜΑΚΑΣ')
    
    phone = models.CharField(max_length=14, default='')

    #idSchool
    """    
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    
    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})
        return reverse('contacts-view', kwargs={'pk': self.id})

    class Meta:
        unique_together = ('contact', 'address_type',)
    """    


    @staticmethod
    def getGCInfo(cls):        
        """
        Gets latest record using (id)
        """
        id = GradeCenterInfo.objects.latest('id').id
        gcinfo = GradeCenterInfo.objects.filter(id=id)[0]
        #record.update( name, article,  presidentName, presidentSurname, phone, folderBooks, minFolderBooks, 
        return gcinfo

###################################
# TEACHER
###################################
"""
codeAfm codeGrad codeSpec name surname 
"""
class Teacher(models.Model):

    codeAfm = models.CharField(max_length=12, null = False, unique = True )
    codeGrad = models.CharField(max_length=12, null = False, unique = True)
    
    codeSpec = models.CharField(max_length=8)
    codeSpecId = models.SmallIntegerField(null = True)

    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    
    #added 2018-04
    phoneHom = models.CharField(max_length=14, default='26410')
    phoneMob = models.CharField(max_length=14, default='0000-')

    #idSchool
    """    
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    """    

    #def get_absolute_url(self):
        #return reverse('author-detail', kwargs={'pk': self.pk})
        #return reverse('contacts-view', kwargs={'pk': self.id})

    #class Meta:
    #    unique_together = ('contact', 'address_type',)


###################################
# SCHOOL
###################################
class School(models.Model):
    SCHOOL_TYPE = ( (0, 'ΓΥΜΝΑΣΙΟ'), (1, 'ΛΥΚΕΙΟ'), (3, 'ΙΔΙΩΤΙΚΟ'), (4, 'ΑΛΛΟ'), )
    
    name = models.CharField(max_length=64)
    stype = models.IntegerField(choices=SCHOOL_TYPE)
    
    #UPD:2018-05
    address = models.CharField(max_length=48, default='')
    city = models.CharField(max_length=32, default='')
    tk = models.CharField(max_length=6, default='')

    def __unicode__(self):
        return self.name

    def average_rating(self):
        #all_ratings = map(lambda x: x.rating, self.review_set.all())
        #return np.mean(all_ratings)
        pass

    @staticmethod
    def lexSchoolType(cls, id):
        if id in[0,1]: 
            return cls.SCHOOL_TYPE[id][1]
        else: 
            return "ΑΓΝΩΣΤΟ"


###################################
# SCHOOLTOGRADE
###################################
""" School to get books from """
class SchoolToGrade (models.Model):
    SCHOOL_TYPE = ( (0, u'ΗΜΕΡΗΣΙΟ'), (1, u'ΕΣΠΕΡΙΝΟ'), ) 
    #SCHOOL_TYPE = ( (0, 'KENO'), (1, 'ΗΜΕΡΗΣΙΟ'), (2, 'ΕΣΠΕΡΙΝΟ'), ) 

    code = models.CharField(max_length=6, blank=False, null = False)
    name = models.CharField(max_length=64)
    type = models.SmallIntegerField(choices=SCHOOL_TYPE, default=0, blank=False, null=False)   # default='ΗΜΕΡΗΣΙΟ'
    #type = models.SmallIntegerField(default=0, blank=False, null=False)                        #0:Ημερήσιο, 1:Εσπερινό

    #DDE
    ddeCode = models.SmallIntegerField(null=True)      # Na allaxei se Int
    ddeName = models.CharField(max_length=64, blank=True, null=True)

    #UPD:2018-05
    address = models.CharField(max_length=48, default='')
    city = models.CharField(max_length=32, default='')
    tk = models.CharField(max_length=6, default='')

    @staticmethod
    def lexSchoolToGradeType(cls, id):
        if id in[0,1]:
            return cls.SCHOOL_TYPE[id][1]
        else: 
            return "ΑΓΝΩΣΤΟ"

    def __unicode__(self):
        return "%s %s" %(self.SCHOOL_TYPE[type], self.name)
        #dict(Scoop.FLAVOR_CHOCIES)[self.flavor]

###################################
# DDE
###################################
""" """
class Dde(models.Model):
    
    code = models.CharField(max_length=8, null= False, unique = True)
    name = models.CharField(max_length=64, null=False, unique = True)
    
    def __unicode__(self):
        return self.code, ', ', self.name, 


###################################
# SPECIALTY
###################################
""" """
class Specialty(models.Model):
    #ΠΕ01 κλπ
    code = models.CharField(max_length=12, null= False, unique = True)
    name = models.CharField(max_length=64, null=False)
    
    def __unicode__(self):
        return self.code, ', ', self.name, 



###################################
# LESSON
###################################
"""
Fields: booksAB booksABFolders booksC booksCFolders category name status type 
"""        
class Lesson(models.Model):

    #TYPE_TYPE = ( (0, 'ΗΜΕΡΗΣΙΟ'), (1, 'ΕΣΠΕΡΙΝΟ'), ) 
    LESSON_TYPE = ( (0, u'ΗΜΕΡΗΣΙΟ'), (1, u'ΕΣΠΕΡΙΝΟ'), ) 
    #SchoolToGradeType (@ ORM as CHOICES)
    #['ΚΕΝΟ', 'ΗΜΕΡΗΣΙΟ', 'ΕΣΠΕΡΙΝΟ']; OK 
    
    #Fakeloi 1o 2o xeri (AB)
    booksAB = models.IntegerField(default=0, blank=False)
    booksABFolders = models.IntegerField(default=0, blank=False)    
    #Fakeloi > anavathm. C
    booksC = models.IntegerField(default=0, blank=False)
    booksCFolders = models.IntegerField(default=0, blank=False)
    
    category = models.CharField(max_length=16, blank=False, default='Θετικής')      #OP: anth|thetikh|oikon
    name = models.CharField(max_length=64, blank=False)
    status = models.SmallIntegerField(default=0, blank=False, null=False)              #
    
    #type = models.SmallIntegerField(choices=LESSON_TYPE, default=0, blank=False, null=False)  # default='ΗΜΕΡΗΣΙΟ'
    type = models.SmallIntegerField(default=0, blank=False, null=False)                        #0:Ημερήσιο, 1:Εσπερινό
    #type = models.CharField(max_length=16, blank=False, default='Ημερήσιο')                   #Ημερήσιο, Εσπερινό

    #Related Table (M:N)
    graders = models.ManyToManyField(Teacher, through="Grader")
    acceptances = models.ManyToManyField(SchoolToGrade, through="Acceptance")
            
    #field constraint
    class Meta:
        unique_together = ('name', 'category', 'type',)     # eg. accept A-GENIKIS-imerisio A-GENIKIS-esperino
    
    """    
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    """    
    @staticmethod
    def lexLessonType(cls, id):
        if id in[0,1]: 
            return cls.LESSON_TYPE[id][1]
        else: 
            return "ΑΓΝΩΣΤΟ"

    #get next Folder no
    def getNextFolderNo(self, codeType=-1):
        #res = self.folder_set.filter(type = type).order_by("-no")[0].no + 1  #reverse
        if codeType == -1:              # count ALL Folders
            res = self.folder_set.order_by("-no")
        else:                           # count codeType Folders Only 
            res = self.folder_set.filter(codeType = codeType).order_by("-no")
        return 1 if (len(res) == 0) else res[0].no + 1

    def prepareGradingAB(self):      #aka Make AB-Folders for Lesson        
        #@settings.py => CONST_MINFOLDERBOOKS=4 #(eg. Folder has at least 4 books)
        folderCount = 0

        #Get params
        gcinfo = GradeCenterInfo.getGCInfo(GradeCenterInfo)
        folderSize = gcinfo.folderBooks
        folderSizeMargin = gcinfo.minFolderBooks
        #folderSize = settings.CONST_FOLDERBOOKS #25 
        #folderSizeMargin = settings.CONST_MINFOLDERBOOKS
        #folderSizeMargin = 2 
        
        if self.status != 4:
            print "Error: Acceptance not Completed"
        else:                                     
            bookCount = self.booksAB
            lastFolderSize = 0 
            folderCount = 0
            
            while ( bookCount > 0 ) :                
                if bookCount >= folderSize:
                    try:    #with transaction.atomic():
                        folderCount += 1
                        thisFolderSize = folderSize
                        #folderResidue = bookCount - folderSize
                        bookCount = bookCount - folderSize
                        Folder( LessonID = self, books = thisFolderSize , no = folderCount, codeStatus = 0, codeType = 0, codeLocation = 0,).save()
                        self.booksABFolders =+ folderCount
                        #self.booksABFolders =+ 1
                        self.save()
                        print 'NewFOLDER: folderCount(%d) thisFolderSize(%d) bookCount(%d)' % (folderCount, thisFolderSize, bookCount)
                        #msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                        #helperMessageLog(request, msg, tag='info')
                    except DatabaseError:
                        msg = "Αδυναμία Δημιουργίας Φακέλου (%s)!" %(folderCount)
                        #helperMessageLog(request, msg, tag='error')
                        print "ERROR====>", msg
                # until 4                                    
                elif bookCount in range ( folderSizeMargin+1, folderSize ):
                    try:    #with transaction.atomic():
                        folderCount += 1
                        thisFolderSize = bookCount
                        bookCount = 0 
                        Folder( LessonID = self, books = thisFolderSize , no = folderCount, codeStatus = 0, codeType = 0, codeLocation = 0,).save()
                        self.booksABFolders =+ folderCount
                        #self.booksABFolders =+ 1
                        self.save()
                        print 'NewFOLDER: folderCount(%d) thisFolderSize(%d) bookCount(%d)' % (folderCount, thisFolderSize, bookCount)
                        #msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                        #helperMessageLog(request, msg, tag='info')
                    except DatabaseError:
                        msg = "Αδυναμία Δημιουργίας Φακέλου (%d)!" %(folderCount)
                        #helperMessageLog(request, msg, tag='error')
                        print "ERROR====>", msg
                
                elif bookCount in range ( 0, folderSizeMargin+1 ):
                    try:    #with transaction.atomic():
                        if (folderCount==0):            # 1 folder =>  make folder
                            folderCount = 1
                            thisFolderSize = bookCount
                            Folder(LessonID=self, books=bookCount, no=folderCount, codeStatus=0, codeType=0, codeLocation=0,).save()
                            self.booksABFolders=1
                            self.save()
                            print 'New ZERO SMALL FOLDER: folderCount(%d) thisFolderSize(%d) bookCount(%d)' % (folderCount, thisFolderSize, bookCount)
                        else:                           # get last folder (aka folderCount) > add books
                            thisFolderSize = folderSize + bookCount
                            Folder.objects.filter(LessonID = self, no=folderCount).update(books = thisFolderSize)
                            print 'Ενημέρωση Φακέλου: folderCount(%d) thisFolderSize(%d) bookCount(%d)' % (folderCount, thisFolderSize, bookCount)
                        bookCount = 0 
                    except DatabaseError:
                        msg = "Αδυναμία Ενημέρωσης Φακέλου (%d) με υπόλοιπο %(d)!" %(folderCount, bookCount)
                        #helperMessageLog(request, msg, tag='error')                
                        print "ERROR====>", msg
                else: 
                    print "Unkown Case in prepareGradingAB"
                    break 


    #ACCEPTING Methods
    def changeStatus(self, status = None):        #aka Make changes
        
        print "Lesson Status (%d) Change to Status (%d)" % (self.status , status)
        #Status value check
        if self.status + 1 != status:
            #log
            msg, tag = ('Σφάλμα τιμών για το Status του Μαθήματος (Status not +1)!', 'error')
            return False, msg, tag

        #Status=0->1 'ΠΡΟΕΤΟΙΜΑΣΙΑ ΠΑΡΑΛΑΒΩΝ'  | 'PREPARE Accepting'
        elif self.status == 0:
            # make a record for each school 
            # 2017 May > Cater for Hmerisia/Esperina via lesson.type~school.type  (matches)
            for s in SchoolToGrade.objects.filter(type=self.type): # 
            #for s in SchoolToGrade.objects.all():
                try:    
                    Acceptance ( LessonID = self , SchoolToGradeID = s ).save() 
                    #Acceptance ( LessonID = lesson, SchoolToGradeID = school ).save() 
                    #msg = "Επιτυχής εισαγωγή εγγραφής! (addfull)"              
                    #helperMessageLog(request, msg, tag='info')
                except DatabaseError:
                    transaction.rollback()   
                    msg = "Αδυναμία εισαγωγής εγγραφής!"
                    print "ERROR===>", msg 
                    #helperMessageLog(request, msg, tag='error')
                #Acceptance ( LessonID = self , SchoolToGradeID = s ).save() 
                #,  books = , booksAbscent = , booksZero = , status = ,  statusTime = , )
            #self.prepareAccepting()    #aka Make Acceptance Records for Lesson 
            self.status = 1
            self.save()            
            #log
            msg, tag = ('(0->1)ΠΡΟΕΤΟΙΜΑΣΙΑ ΠΑΡΑΛΑΒΩΝ! (PREPARE Accepting!)', 'success')
            return True, msg, tag

        #Status=1->2 'ΕΝΑΡΞΗ ΠΑΡΑΛΑΒΩΝ' | 'START Accepting'
        elif self.status == 1:
            self.status = 2
            self.save()
            #log
            #helperMessageLog(request,'(1->2)ΕΝΑΡΞΗ ΠΑΡΑΛΑΒΩΝ! (START Accepting!)', tag='success')
            #return True
            msg, tag = ('(1->2)ΕΝΑΡΞΗ ΠΑΡΑΛΑΒΩΝ! (START Accepting!)', 'success')
            return True, msg, tag

        #Status=2->3  'ΕΛΕΓΧΟΣ/ΟΛΟΚΛΗΡΩΣΗ ΠΑΡΑΛΑΒΩΝ' | 'CHECK Accepting'
        elif self.status == 2:
            #print "CHECK Accepting- Status = 3"
            if not self.checkAccepting():
                #helperMessageLog(request,'(2->34)Υπάρχουν ΕΚΡΕΜΜΟΤΗΤΕΣ ΠΑΡΑΛΑΒΩΝ!', tag='error')
                #return False
                msg, tag = ('(2->34)Υπάρχουν ΕΚΡΕΜΜΟΤΗΤΕΣ ΠΑΡΑΛΑΒΩΝ!', 'error')
                return False, msg, tag
            
            else: 
                self.status = 4
                self.save()                
                #helperMessageLog(request,'CHECK/COMPLETE Accepting OK', tag='success'):
                #helperMessageLog(request,'(2->34)ΕΛΕΓΧΟΣ/ΟΛΟΚΛΗΡΩΣΗ ΠΑΡΑΛΑΒΩΝ! (CHECK/COMPLETE Accepting!)', tag='success')
                #return "Success: Status Changed. in 4 - CHECK/COMPLETE Accepting OK"
                msg, tag = ('(2->34)ΕΛΕΓΧΟΣ/ΟΛΟΚΛΗΡΩΣΗ ΠΑΡΑΛΑΒΩΝ! (CHECK/COMPLETE Accepting!)', 'success')
                return True, msg, tag

        #Status=3->4
        elif self.status == 3:          # Double Check
            if not self.checkAccepting():                
                #helperMessageLog(request,'(3->4)Υπάρχουν ΕΚΡΕΜΜΟΤΗΤΕΣ ΠΑΡΑΛΑΒΩΝ!', tag='error')
                #return False
                msg, tag = ('(3->4)Υπάρχουν ΕΚΡΕΜΜΟΤΗΤΕΣ ΠΑΡΑΛΑΒΩΝ!', 'error')
                return False, msg, tag
            else: 
                self.status = 4
                self.save()                
                #helperMessageLog(request,'(3->4)ΕΛΕΓΧΟΣ/ΟΛΟΚΛΗΡΩΣΗ ΠΑΡΑΛΑΒΩΝ! (CHECK/COMPLETE Accepting!)', tag='success')
                #return True
                msg, tag = ('(3->4)ΕΛΕΓΧΟΣ/ΟΛΟΚΛΗΡΩΣΗ ΠΑΡΑΛΑΒΩΝ! (CHECK/COMPLETE Accepting!)', 'success')
                return True, msg, tag

        #Status=4->5    'ΠΡΟΕΤΟΙΜΑΣΙΑ ΒΑΘΜΟΛΟΓΗΣΗΣ | 'PREPARE Grading ' (make Folders+Barcodes)
        elif self.status == 4:
            #print "PREPARE Grading (make Folders+Barcodes)"
            self.prepareGradingAB()
            self.makeBarcodes()
            self.status = 5
            self.save()
            msg, tag = ('(4->5)ΠΡΟΕΤΟΙΜΑΣΙΑ ΒΑΘΜΟΛΟΓΗΣΗΣ! \
                    (PREPARE Grading - Folders+Barcodes!)', 'success')
            return True, msg, tag

        #Status=5->6     'ΕΝΑΡΞΗ ΒΑΘΜΟΛΟΓΗΣΗΣ | 'START Grading ' 
        elif self.status == 5:
            self.status = 6
            self.save()
            msg, tag = ('(5->6)ΕΝΑΡΞΗ ΒΑΘΜΟΛΟΓΗΣΗΣ! (START Grading!)', 'success')
            return True, msg, tag

        #Status=6->7     'ΕΛΕΓΧΟΣ ΒΑΘΜΟΛΟΓΗΣΗΣ | 'CHECK Grading ' 
        elif self.status == 6:
            #print "CHECK Grading"
            if not self.checkGrading():
                msg, tag = ('(6->7) Υπάρχουν ΕΚΡΕΜΜΟΤΗΤΕΣ ΒΑΘΜΟΛΟΓΗΣΗΣ!', 'error')
                return False, msg, tag
            else: 
                self.status = 7
                self.save()
                msg, tag = ('(6->7)ΕΛΕΓΧΟΣ ΒΑΘΜΟΛΟΓΗΣΗΣ! (CHECK Grading!)', 'success')
                return True, msg, tag

        #Status=7->8     'ΟΛΟΚΛΗΡΩΣΗ ΒΑΘΜΟΛΟΓΗΣΗΣ | 'COMPLETE Grading ' 
        elif self.status == 7:
            if not self.checkGrading():
                msg, tag = ('(7->8)ΑΔΥΝΑΤΗ ΟΛΟΚΛΗΡΩΣΗΣ ΒΑΘΜΟΛΟΓΗΣΗΣ!<br/>Eκκρεμμότητες!', 'error')
                return False, msg, tag
            else:
                self.status = 8
                self.save()
                msg, tag = ('ΟΛΟΚΛΗΡΩΣΗ ΒΑΘΜΟΛΟΓΗΣΗΣ! (7->8) (COMPLETE Grading!)', 'success')
                return True, msg, tag
        else:
            msg, tag = ('ΑΝΥΠΑΡΚΤΟΣ Κωδικός STATUS!', 'error')
            return False, msg, tag

    #ACCEPTING Methods
    def prepareAccepting(self):    #aka Make Acceptance Records for Lesson 
        for s in SchoolToGrade.objects.all():
            try:
                a = Acceptance (LessonID=self, SchoolToGradeID=s) #,books/booksAbscent/booksZero/status/statusTime)
                a.save()
                #msg = "Επιτυχής εισαγωγή εγγραφής!"                 
                #helperMessageLog(request, msg, tag='info')
            except DatabaseError:
                transaction.rollback()   
                msg = "Αδυναμία εισαγωγής εγγραφής!"
                helperMessageLog(request, msg, tag='error')

        self.status = 1
        self.save()
        print "Prepare Accepting OK"
        return True
    """ """


    """ BARCODES """
    def makeBarcodes(self):
        """
        makes barcodes for folders of Lesson 
        call as => Lesson.objects.get(pk=4).makeBarcodes()
        """
        for f in Folder.objects.filter(LessonID=self.id).all():
            f.codeBarcode ='%04d-%010d' %(self.id, f.id)
            f.save() 
        print "makeBarcodes OK"
        return True


    def startAccepting(self):      #aka Make Acceptance Records for Lesson 
        self.status = 2 
        self.save()
        return True

    """ Check each Acceptance Record for OK """
    def checkAccepting(self):      
        fail = False
        booksAB = 0
        # Check status for each school in lessson
        for a in Acceptance .objects.filter(LessonID = self): 
            if a.status == 0:  # still open 
                print "CHECK Accepting Fail"
                fail = True
                return False
            else: 
                booksAB = booksAB + a.books   # get Total
        
        self.booksAB = booksAB      # Total Books
        self.status = 3             # status = ok -> change status 
        self.save()
        print "CHECK Accepting OK"
        return True

    def completeAccepting(self):      #aka Make Acceptance Records for Lesson 
        self.status = 4
        self.save()
        return True

    #GRADING Methods
    def prepareGrading(self):      #aka Make C-Folders for Lesson 
        self.makeBarcodes()
        self.status = 5
        self.save()
        return True

    def startGrading(self):      
        self.status = 6 
        self.save()
        return True

    def checkGrading(self):      
        for f in Folder.objects.filter(LessonID=self.id).all():
            if f.codeStatus != 2:
                print "CHECK Grading FAILED"
                return False
        return True

    def completeGrading(self):      #aka Make Acceptance Records for Lesson 
        self.status = 8 
        self.save()
        return True

###################################
# GRADER
###################################
""" M:N with Lesson, Teacher (django Through Table) """
class Grader(models.Model):
    
    #M:N-FKs
    TeacherID = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    LessonID = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    # synton.
    isCoordinator = models.BooleanField(default=False)
    # anavath.
    isgraderC = models.BooleanField(default=False)
    status = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    # used to check availability
    currentFolder = models.IntegerField(blank=True, null=True)        #
    currentFolderID = models.IntegerField(blank=True, null=True) 

    """
    def __unicode__(self):
        return "Grader"
    """
    
    """
    #SELECT_RELATED OK
    graders = Grader.objects.all().select_related("LessonID, TeacherID")
    for grader in graders:
        print grader.TeacherID.name, grader.LessonID.name, grader.isCoordinator
    """
      

# HELPERS
def GraderJoinTables(LessonID=None, exclude=False):
    if LessonID is None:
        data = Grader.objects.select_related("LessonID", "TeacherID")
    else: 
        if not exclude:
            data = Grader.objects.select_related("LessonID", "TeacherID").filter(LessonID=LessonID)
        else:
            data = Grader.objects.select_related("LessonID", "TeacherID").exclude(LessonID=LessonID)
    
    return data

"""        
#get data
for grader in data:
    grader.TeacherID.name, grader.LessonID.name, grader.isCoordinator
"""                


""" 
helpfull joined info on related M:N
To see again if it can go as Model Manager/QuerySet
"""
"""
def RelatedGraderInfo(LessonID=None):
    
    #def get_queryset(self, GraderID=None):
    dictData = []
    if LessonID is None:
        relData = Grader.objects.select_related('TeacherID')
    else: 
        relData = Grader.objects.select_related('TeacherID').filter(LessonID=LessonID)
    for g in relData: 
        t, l = g.TeacherID, g.LessonID 
        dictData.append({'id': g.id, 'isCoordinator': g.isCoordinator,  'isgraderC': g.isgraderC,  'status': g.status, 
            'TeacherID': t.id, 'surname': t.surname,  'name': t.name,  'codeGrad': t.codeGrad,  'codeAfm': t.codeAfm,  
        })
    #print dictData
    return dictData
"""

""" 
TO HANDLE EXCLUDE - CHECK
"""
"""
def RelatedGraderInfov2(LessonID=None, exclude=False):
    
    #def get_queryset(self, GraderID=None):
    dictData = []
    if LessonID is None:
        relData = Grader.objects.select_related('TeacherID')
    else: 
        if not exclude:  # filter 
            relData = Grader.objects.select_related('TeacherID').filter(LessonID=LessonID)
        else:            # exclude
            relData = Grader.objects.select_related('TeacherID').exclude(LessonID=LessonID)
    for g in relData: 
        t, l = g.TeacherID, g.LessonID 
        dictData.append({'id': g.id, 'isCoordinator': g.isCoordinator,  'isgraderC': g.isgraderC,  'status': g.status, 
            'TeacherID': t.id, 'surname': t.surname,  'name': t.name,  'codeGrad': t.codeGrad,  'codeAfm': t.codeAfm,  
        })
    #print dictData
    return dictData

"""

###################################
# FOLDER
###################################
"""
SOS Field DEPENDENCIES in MODELS 
class Meta:
    unique_together = (('first_name', 'last_name'),)
    stype = models.IntegerField(choices=SCHOOL_TYPE)

HAS REL(1:N) -> LESSON
HAS REL(M:N) -> BOOKING
"""
class Folder(models.Model):    
    
    GRAD_TYPE = ( (0, u'Φ(Α)'), (1, u'Φ(Β)'),(2, u'Φ(ΑΝΑ)'), )
    #GRAD_TYPE = ( (0, u'Κανονικός'), (1, u'Αναβαθμολόγηση'), )
    
    LOCATION_TYPE = ( (0, u'Αποθήκη'), (1, u'Βαθμολογητής'), (2, u'Φύλαξη'), )
    
    STATUS_TYPE = ( (0, u'Αχρέωτος'), (1, u'Χρεωμένος'), (2, u'Ολοκληρώθηκε' ), )

    #STATUS_TYPE = ( (0, u'Αχρέωτος(A)'), (1, u'Αχρέωτος(Β)'), (2, u'Αχρέωτος(C)'), 
    #        (3, u'Χρεωμένος(A)'), (4, u'ΧρεωμένοςΒ)'), (5, u'Χρεωμένος(C)'), 
    #        (8, u'Επιστροφή' ), )
    
    books = models.PositiveSmallIntegerField(default=0, blank=False, null=False)            # 0:
    no = models.IntegerField(blank=False, null=False)                                       # AA fakelou / mathima
    
    codeBarcode =  models.CharField(max_length=16, blank=False, default='0000-0000')        #OP: anth|thetikh|oikon
    #f.codeBarcode ='%04d-%010d' %(self.id, f.id)
    codeLocation  = models.PositiveSmallIntegerField(default=0, blank=False, null=False)    #0: 
    codeStatus = models.PositiveSmallIntegerField(default=0, blank=False, null=False)       #
    codeType = models.PositiveSmallIntegerField(default=0, blank=False, null=False)         #A/B/ANA

    #typeChar  = models.CharField(max_length=1, default='A', blank=False, null=False)
    #isNow = models.CharField(max_length=1)

    # 1:N
    LessonID = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    #M:N
    bookings = models.ManyToManyField(Grader, through="Booking")
    
    class Meta:
        #2017 June update: due to different coding (serial no for each a/b/ana)
        unique_together = ('LessonID', 'no')  # folder no 4 / lesson 4 / type 

        #unique_together = ('LessonID', 'no', 'codeType',)  # folder no 4 / lesson 4 / type
    
    # Call without instances as >> MyClass.the_static_method(2) # outputs 2
    @staticmethod
    def lexCodeType(cls, id):
        if id in[0,1,2]: 
            return cls.GRAD_TYPE[id][1]
        else:
            return u"ΑΓΝΩΣΤΟ"

    @staticmethod
    def lexCodeLocation(cls, id):
        if id in[0,1,2]: 
            return cls.LOCATION_TYPE[id][1]
        else: 
            return u"ΑΓΝΩΣΤΟ"

    @staticmethod
    def lexCodeStatus(cls, id):
        if id in [0,1,2]: 
        #if id in range(0,7): 
            return cls.STATUS_TYPE[id][1]
        else: 
            return u"ΑΓΝΩΣΤΟ"

    def getAction(self, station): 
        
        """
        This is WRONG. Action is f(station,location) related.
        Returns action to be taken (IN-OUT) on Folder based on status
        """
        if ((station == 0) and (location == 0)) or ((station == 1) and (location == 2)):
        #if (station=0 and self.location in [0,1,2]):
            return  0   #OUT
        #if self.codeStatus in [3,4,5]:
        elif ((station == 0) and (location == 1)) or ((station == 1) and (location == 1)):
            return  1   #IN
        else:
            #return  None #UNKNOWN - STOP
            return  -1 #UNKNOWN - STOP


# HELPERS
def FolderJoinTables(LessonID=None, exclude=False):
    if LessonID is None:
        data = Folder.objects.select_related("LessonID")
    else: 
        if not exclude:
            data = Folder.objects.select_related("LessonID").filter(LessonID=LessonID)
        else:
            data = Folder.objects.select_related("LessonID").exclude(LessonID=LessonID)
    
    return data

"""        
#get data
for folder in data:
    folder.LessonID.name, folder.status
"""                



###################################
# ACCEPTANCE
###################################
""" 
Accept Incoming Books for Lessons from SchoolsToGrade
M:N with Lessons, SchoolsToGrade (django Through Table) 
"""
class Acceptance(models.Model):
    
    LessonID = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    SchoolToGradeID = models.ForeignKey(SchoolToGrade, on_delete=models.CASCADE)

    books = models.PositiveSmallIntegerField(default=0)      #Tetradia
    booksAbscent = models.PositiveSmallIntegerField(default=0)    #Apoysies
    booksZero = models.PositiveSmallIntegerField(default=0)  #Tetradia Midenismena
    
    status = models.PositiveSmallIntegerField(default=0, blank=False, null=False)    # 0:
    #addedDate = datetime.now().replace(microsecond=0)
    statusTime = models.DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), blank=True)
    #statusTime = models.DateTimeField(default=datetime.now, blank=True)
    
    # 2017-may Added note to help with 
    notes = models.CharField(max_length=32, blank=True)

    class Meta:
        unique_together = (('LessonID', 'SchoolToGradeID'),)


# HELPERS
def AcceptanceJoinTables(LessonID=None):
    if LessonID is None:
        data = Acceptance.objects.select_related("SchoolToGradeID")
    else: 
        data = Acceptance.objects.select_related("SchoolToGradeID").filter(LessonID=LessonID)
    
    return data

# HELPERS
def AcceptanceJoinTablesX2(LessonID=None):
    if LessonID is None:
        data = Acceptance.objects.select_related("SchoolToGradeID", "LessonID")
    else: 
        data = Acceptance.objects.select_related("SchoolToGradeID", "LessonID").filter(LessonID=LessonID)
    
    return data

"""        
#get data
for folder in data:
    folder.LessonID.name, folder.status
"""             

"""
def RelatedAcceptanceInfo(LessonID=None):
    
    #def get_queryset(self, GraderID=None):
    dictData = []
    if LessonID is None:
        relData = Acceptance.objects.select_related('SchoolToGradeID')
    else: 
        relData = Acceptance.objects.select_related('SchoolToGradeID').filter(LessonID=LessonID)

    for r in relData: 
        l, s = r.LessonID, r.SchoolToGradeID 
        dictData.append({'id': r.id, 'books': r.books,  'booksAbscent': r.booksAbscent,  'booksZero': r.booksZero,  'status': r.status,  'statusTime': r.statusTime, 
            'SchoolToGradeID': r.SchoolToGradeID_id, 'code': s.code, 'name': s.name, 'type': s.type, 
            #'FolderID': r.FolderID_id, 'books': f.books, 'no': f.no,  'status': f.status,  'type': f.type, 
            })
    #print dictData
    return dictData
"""


###################################
# BOOKING
###################################
""" 
M:N with Grader, Folder (django Through Table) 
"""
#class Holding(models.Model):
class Booking(models.Model):
    
    # USed for reference. Not used in DB model 
    ACTION_TYPE = ( (0, u'Χρέωση'), (1, u'Παραλαβή'), )
    STATION_TYPE = ( (0, u'Αποθήκη'), (1, u'Φύλαξη'), )
    
    FolderID = models.ForeignKey(Folder, on_delete=models.CASCADE)
    GraderID = models.ForeignKey(Grader, on_delete=models.CASCADE)

    #no = models.IntegerField()
    action = models.PositiveSmallIntegerField(null=False)     # 0:OUT | 1:IN
    actionTime = models.DateTimeField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), null=False)
    #actionTime = models.DateTimeField(default=datetime.now, blank=True)
    station = models.PositiveSmallIntegerField(default=0, blank=False, null=False)   # 0: apoth , 1: filaksi
    #status = models.PositiveSmallIntegerField(default=0, blank=False, null=False)   # 0: idle , 1: out , 2: in 
    #regAction = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    #date = models.DateTimeField(auto_now_add=True, blank=True)
    
    #2017-May
    #actionDuration = models.DateTimeField(default=None, blank=True, null=True)
    actionDuration = models.DurationField(default=None, blank=True, null=True)
    
    #objects = models.Manager()
    #relatedBooking = RelatedBookingInfo()
    
    # 2017-May; To cater for operator accounting
    operator = models.ForeignKey(User, on_delete=models.CASCADE)


    # 2017-June; OnFOlderType > To cater for history-keeping on folder-type
    wasTypeOf = models.PositiveSmallIntegerField(default=-1, blank=False)         #A/B/ANA

    #typeChar  = models.CharField(max_length=1, default='A', blank=False, null=False)
    #isNow = models.CharField(max_length=1)


    # Call without instances as >> MyClass.the_static_method(2) # outputs 2
    @staticmethod
    def lexActionType(cls, id):
        if id in[0,1]: 
            return cls.ACTION_TYPE[id][1]
        else:
            return u"ΑΓΝΩΣΤΟ"

    @staticmethod
    def lexStationType(cls, id):
        if id in[0,1]: 
            return cls.STATION_TYPE[id][1]
        else:
            return u"ΑΓΝΩΣΤΟ"

    # Call without instances as >> MyClass.the_static_method(2) # outputs 2
    @staticmethod
    def lexCodeType(cls, id):
        if id in[0,1,2]: 
            return FOLDER_TYPE[id][1]
        else:
            return u"ΑΓΝΩΣΤΟ"


# HELPERS
def BookingJoinTables(GraderID=None):
    if GraderID is None:
        data = Booking.objects.select_related("FolderID", "GraderID")
    else: 
        data = Booking.objects.select_related("FolderID", "GraderID").filter(GraderID=GraderID)
    return data

# HELPERS
def BookingJoinTablesX3(GraderID=None):
    if GraderID is None:
        data = Booking.objects.select_related("LessonID", "FolderID", "GraderID")
    else: 
        data = Booking.objects.select_related("LessonID", "FolderID", "GraderID").filter(GraderID=GraderID)
    return data

"""        
#get data
for booking in data:
    booking.GraderID.isgraderC, booking.FolderID.codeStatus
"""             


""" 
helpfull joined info on related M:N
To see again if it can go as Model Manager/QuerySet
"""
"""
def RelatedBookingInfo2 (GraderID=None):
    
    #def get_queryset(self, GraderID=None):
    dictData = []
    setBooking = Booking.objects.select_related('FolderID')
    setFolder = Booking.objects.select_related('FolderID')
    relData = Booking.objects.select_related('FolderID').filter(GraderID=GraderID)

    for r in relData: 
        g, f = r.GraderID, r.FolderID 
        dictData.append({'id': r.id, 'action': r.action,  'actionTime': r.actionTime,  'station': r.station,  
            'FolderID': r.FolderID_id, 'books': f.books, 'no': f.no,  'status': f.status,  'type': f.type, 
            #'FolderID': r.FolderID_id, 'books': f.books, 'no': f.no,  'status': f.status,  'type': f.type, 
            })
    #print dictData
    return dictData

def RelatedBookingInfo(GraderID=None):
    
    #def get_queryset(self, GraderID=None):
    dictData = []
    if GraderID is None:
        relData = Booking.objects.select_related('FolderID')
    else: 
        relData = Booking.objects.select_related('FolderID').filter(GraderID=GraderID)

    for r in relData: 
        g, f = r.GraderID, r.FolderID 
        dictData.append({'id': r.id, 'action': r.action,  'actionTime': r.actionTime,  'station': r.station,  
            'FolderID': r.FolderID_id, 'books': f.books, 'no': f.no,  'status': f.status,  'type': f.type, 
            #'FolderID': r.FolderID_id, 'books': f.books, 'no': f.no,  'status': f.status,  'type': f.type, 
            })
    #print dictData
    return dictData
"""



from django.db import DatabaseError, IntegrityError, transaction

#from helpScripts import helperMessageLog
# Create your models here.

#Date: 2017-May 
""" """
def helperMessageLog(request, msg='Null log', tag='info'):
    """
    Handles 3to1 statements for ajax messages & logging
    """
    if tag=='error':
        messages.error(request, msg, tag, fail_silently=True)
    elif tag=='info':
        messages.info(request, msg, tag, fail_silently=True)
    elif tag=='success':
        messages.warning(request, msg, tag, fail_silently=True)
    elif tag=='success':
        messages.warning(request, msg, tag, fail_silently=True)
    else: 
        messages.info(request, msg, tag, fail_silently=True)
    print msg



