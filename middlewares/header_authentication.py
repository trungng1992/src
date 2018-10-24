from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from django.utils.deprecation import MiddlewareMixin
from oob import settings
import json, re
from time import time

class Checksum_Header(MiddlewareMixin):
    def _response(self, data, status):
        response = Response(
            data,
            content_type="application/json",
            status=status
        )
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}

        return response

    def process_request(self, request):
        request._request_time = int(time())

        url = request.get_full_path()

        if not re.match('^/api/v1/.*', url):
            return

        USER_API = settings.USER_API
        PASSWORD_API = settings.PASS_API

        nTimestamp   = str(int(time()))
        nTimestamp_bypass = 987654321


        #strtest = "%s - %s - %s" % (str(timestamp), str(checksum), str(strToken))

        checksumToken = request.META.get('CHECKSUM-TOKEN') # get the username request header
        timeStamp     = request.META.get('TIMESTAMP')
        #authorization = request.META.get('HTTP_AUTHORIZATION')

        return HttpResponse(timeStamp)

        if timeStamp == nTimestamp_bypass and settings.DEBUG:
            return

        if abs(int(nTimestamp) - int(timeStamp)) > 600:
            return self._response({
                'response_code': HTTP_400_BAD_REQUEST,
                'response_code': 'Please check timestamp'
            }, status=HTTP_400_BAD_REQUEST)

        strToken   = hashlib.sha256('_'.join([USER_API,PASSWORD_API,timeStamp]).encode('utf-8')).hexdigest()
        if strToken != checksumToken:
            return self._response({
                'response_code': HTTP_400_BAD_REQUEST,
                'response_code': 'Invalid Account'
            }, status=HTTP_400_BAD_REQUEST)

        return

    def process_response(self, request, response):
        _request_time = request._request_time
        _response_time = int(time())

        timeExcute = _response_time - _response_time

        return response
