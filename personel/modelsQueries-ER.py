#!/usr/bin/env python
# -*- coding: utf-8 -*-

#python manage.py shell

from personel.models import * 

'''
SOS Field DEPENDENCIES in MODELS 

class Meta:
    unique_together = (('first_name', 'last_name'),)
'''



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
lesson.objects.all()
lesson(name ='μαθηματικα κατευθυνσησ',).save()
#lesson(name ='αρχαια ελληνικα κατευθυνσησ',).save()

for lessonname in [ 'βιολογια γ.π.','ιστορια γ.π.', 'μαθηματικα και στοιχεια στατιστικησ γ.π.', 'νεοελληνικη γλωσσα γ.π.', 'αρχαια ελληνικα ο.π.', 'ιστορια ο.π.','λατινικα ο.π.', 'βιολογια ο.π.', 'μαθηματικα ο.π.', 'φυσικη	ο.π.','χημεια ο.π.', 'αρχεσ οικονομικησ θεωριασ ο.π.','αναπτυξη εφαρμογων σε π.π. ο.π.',]:
    lesson(name = lessonname).save()

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


#////////////////////////
#school
#////////////////////////
s0 = school(name ='παπαστρατειο γυμνασιο αγρινιου', stype = 1, )
s0.save()

