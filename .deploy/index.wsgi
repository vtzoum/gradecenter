import os
import sys
import site

# Add site-packages work with
site.addsitedir('/usr/local/lib/python2.7/dist-packages')

# OR Add the site-packages of the chosen virtualenv to work with
#site.addsitedir('~/.virtualenvs/myprojectenv/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/var/www/html/grade-center-app')
sys.path.append('/var/www/html/grade-center-app/bk043')
#/media/tzoumak/CRUZER32GB/Web-SITES-Code/DJANGO-python/APPS/grade-center-app/
#sys.path.append('/home/django_projects/MyProject')
#sys.path.append('/home/django_projects/MyProject/myproject')

os.environ['DJANGO_SETTINGS_MODULE'] = 'bk043.settings'

# Activate your virtual env
#activate_env=os.path.expanduser("~/.virtualenvs/myprojectenv/bin/activate_this.py")
#execfile(activate_env, dict(__file__=activate_env))

#Causes Error in Apache2
#To fix the error, in WSGI dispatcher, change the following lines:
#import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
#to
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
#OR
#import django
#django.setup()
