#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
SOS Field DEPENDENCIES in MODELS 
class Meta:
    unique_together = (('first_name', 'last_name'),)
'''

#////////////////////////
# from django.contrib.auth.models import User
# User
#////////////////////////
from personel.models import * 
from django.contrib.auth.models import User, Group
#u1 = User.objects.create(name="tzoumak")
#u1 = User.objects.create(name="gta")
#{% if request.user is has_group("Admin") or request.user is has_group("Grammateia") or 
#request.user is has_group("Filaxi") or request.user is has_group("Apothiki") %} 
#obj, created = Person.objects.get_or_create(first_name='John',last_name='Lennon',defaults={'birthday': date(1940, 10, 9)},)

######################################
#GROUPS
#g = Group.objects.get(name='groupname') 
#g.user_set.add(your_user)
groupnames=['Admin','Grammateia','Apothiki','Fylaxi']
for n in groupnames:
    obj, created = Group.objects.get_or_create(name=n)
    #g = Group.objects.create(name=n)

######################################
#USERS
usernames=['u1','u2','u3','u4','u5']
for name in usernames:
    u1 = User.objects.create(username=name)

user = User.objects.get(username='vtzoum')
print user.id
#2

user = User.objects.get(id=1)
print user.id
1

# Where 'request' obj. is avail
user = request.user
gta = Game.objects.create(name="gta", owner=user)

"""


"""

