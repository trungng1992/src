from django.conf import Settings
from django.http import HttpResponseRedirect

class LimitIP(object):
    def process_request(self, request):
        print(request.META)
