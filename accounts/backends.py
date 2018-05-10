#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
When we call authenticate() in our view, we’re going to be calling this instead of Django’s built-in authenticate method. We simply look up the users by email address, rather than email. From there, if we find a user, we check the password and return the User object if all is good. Not too hard. In order to use this backend, we’ll need to add it to our settings.py file, along with the custom user model which we’ll be using.
settings.py

...
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = ['accounts.backends.EmailAuthBackend', ]
...

"""


from django.conf import settings
from django.contrib.auth.models import check_password
from accounts.models import User

class EmailAuthBackend(object):
    """
    A custom authentication backend. Allows users to log in using their email address.
    """

    def authenticate(self, email=None, password=None):
        """
        Authentication method
        """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None

