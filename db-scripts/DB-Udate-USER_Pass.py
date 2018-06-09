#!/usr/bin/env python
# -*- coding: utf-8 -*-

#python manage.py shell

from personel.models import * 
from personel.helpScripts import * 

"""
Change pass as following 
User:uA1 -> Pass:043@A1, User:uF1 -> Pass: 043@F1, etc.
"""
for u in User.objects.all():
    if u.username[0] == 'u':
        newpass= "043@"+ u.username[1:]         
        u.set_password(newpass)
        u.save()
    print u.username, 
    print u.password 

