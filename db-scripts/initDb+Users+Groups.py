#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
SOS Field DEPENDENCIES in MODELS 
class Meta:
    unique_together = (('first_name', 'last_name'),)
'''
######################################
#A.CMD
python manage.py createsuperuser
######################################


######################################
#B.SHELL
python manage.py shell

from personel.models import * 
from django.contrib.auth.models import user, group
#{% if request.user is has_group("Admin") or request.user is has_group("Grammateia") or 
#request.user is has_group("Filaxi") or request.user is has_group("Apothiki") %} 
#obj, created = Person.objects.get_or_create(first_name='John',last_name='Lennon',defaults={'birthday': date(1940, 10, 9)},)

######################################
#GROUPS
#g = Group.objects.get(name='groupname') 
#g.user_set.add(your_user)
groupnames=['Admin','Grammateia','Apothiki','Filaxi']
for n in groupnames:
    obj, created = Group.objects.get_or_create(name=n)
    #g = Group.objects.create(name=n)
#1
#group = Group.objects.get(name='groupname') 
#user.groups.add(group)
#2
#g = Group.objects.get(name='groupname') 
#g.user_set.add(your_user)

######################################
#USERS
user = User.objects.create(username="username", password = "password", email="email")
u1 = User.objects.create(name="tzoumak")

user = User.objects.get(username="username")
user.set_password("password")
user.save()

#USERS+BATCH
usernames=['u1','u2','u3','u4','u5']
for name in usernames:
    u1 = User.objects.create(username=name, password="1234")

usernames=['u1','u2','u3','u4','u5']
for name in usernames:
    User.objects.get(username=name).set_password('1234'+name)


#USERS+BATCH+LIST
userList=[ 
        #{'name':'tzoumak', 'passw':'1234', 'group':'Admin', 'staff': True},
        {'name':'u1', 'passw':'1234', 'group':'Apothiki', 'staff': False},
        {'name':'u2', 'passw':'1234', 'group':'Apothiki', 'staff': False},
        {'name':'u3', 'passw':'1234', 'group':'Filaxi', 'staff': False},
        {'name':'u4', 'passw':'1234', 'group':'Filaxi', 'staff': False},
        ]
for u in userList:
    #username
    objUser, createdUser = User.objects.get_or_create(username=u['name'])
    print createdUser, objUser
    #update
    objUser.set_password(u['passw'])
    objUser.is_staff=u['staff']
    objUser.save()
    #set group
    objGroup, createdGroup = Group.objects.get_or_create(name=u['group'])
    objUser.groups.add(objGroup)
    #group = Group.objects.get(name=u['group']) 



