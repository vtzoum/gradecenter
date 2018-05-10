from django.db import models
from django.utils.translation import ugettext_lazy
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib import messages

try: import simplejson as json
except ImportError: import json

#2017-April
#A1. Check another AjaxMessage implementaions

#from .utils import get_message_dict
class AjaxMessaging1(object):
    """
    Middlware for JSON responses. It adds to each JSON response array with
    messages from django.contrib.messages framework.
    It allows handle messages on a page with javascript
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)

        if request.is_ajax():
            if response['Content-Type'] in ["application/javascript",
                                            "application/json"]:
                try:
                    content = simplejson.loads(response.content)
                    assert isinstance(content, dict)
                except (ValueError, AssertionError):
                    return response
                """
                VTZOUM>>SKIP get_message_dict(message) ERROR
                content['django_messages'] = [get_message_dict(message) for
                                              message in
                                              messages.get_messages(request)]
                """

                response.content = simplejson.dumps(content)
        return response

#A0. Original AjaxMessage implementaions
class AjaxMessaging(object):

    def process_response(self, request, response):
        if request.is_ajax():
            if response['Content-Type'] in ["application/javascript", "application/json"]:
                try:
                    content = json.loads(response.content)
                    #print content
                except ValueError:
                    print 'ERROR'
                    return response

                django_messages = []

                for message in messages.get_messages(request):
                    django_messages.append({
                        "level": message.level,
                        "message": message.message,
                        "extra_tags": message.tags,
                    })
                
                #print "AjaxMessages.py AjaxMessaging" , django_messages
                
                contentb = {}
                contentb['data'] = content
                contentb['django_messages'] = django_messages
                
                #print content
                #content['django_messages'] = django_messages
                response.content = json.dumps(contentb)
                #print response.content 
        return response



class FilterIPMiddleware(object):
    # Check if client IP is allowed
    def process_request(self, request):
        allowed_ips = ['192.168.1.1', '123.123.123.123',] # Authorized ip's
        ip = request.META.get('REMOTE_ADDR') # Get client IP
        if ip not in allowed_ips:
            raise Http403 # If user is not allowed raise Error
        # If IP is allowed we don't do anything
        return None


