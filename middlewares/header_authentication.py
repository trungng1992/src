from django.http import HttpResponse
from django.utils.six.moves.urllib.parse import urlparse


from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from django.utils.deprecation import MiddlewareMixin
from oob import settings
import json

class Checksum_Header(MiddlewareMixin):
    def process_request(self, request):
        return HttpResponse(json.dumps(request))
        url = build_absolute_uri()
        USER_API = settings.USER_API
        PASSWORD_API = settings.PASS_API

        nTimestamp   = str(int(time()))
        nTimestamp_bypass = 987654321


        #strtest = "%s - %s - %s" % (str(timestamp), str(checksum), str(strToken))

        checksumToken = request.META.get('CHECKSUM-TOKEN') # get the username request header
        timeStamp     = request.META.get('TIMESTAMP')
        #authorization = request.META.get('HTTP_AUTHORIZATION')

        if timeStamp == nTimestamp_bypass and settings.DEBUG:
            return

        if abs(int(nTimestamp) - int(timestamp)) > 600:
            return Response({
                'response_code': HTTP_400_BAD_REQUEST,
                'response_code': 'Please check timestamp'
            }, status=HTTP_400_BAD_REQUEST)


        strToken   = hashlib.sha256('_'.join([USER_API,PASSWORD_API,timeStamp]).encode('utf-8')).hexdigest()
        if strToken != checksumToken:
            raise Http403

        return
