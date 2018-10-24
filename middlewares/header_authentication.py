from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from oob import settings
from time import time
import json
import re
import logging
logger = logging.getLogger('api')
'''
Config log
'''


class Checksum_Header(MiddlewareMixin):
    def process_request(self, request):
        # return
        request._is_api = False
        request._request_time = int(time())

        url = request.get_full_path()

        if not re.match('^/api/v1/.*', url):
            return

        request._is_api = True
        request._body = request.body
        USER_API = settings.USER_API
        PASSWORD_API = settings.PASS_API

        nTimestamp   = str(int(time()))
        nTimestamp_bypass = "987654321"


        #strtest = "%s - %s - %s" % (str(timestamp), str(checksum), str(strToken))

        checksumToken = request.META.get('HTTP_CHECKSUM_TOKEN') # get the username request header
        timeStamp     = request.META.get('HTTP_TIMESTAMP')
        #authorization = request.META.get('HTTP_AUTHORIZATION')
        if not timeStamp or not checksumToken:
            return JsonResponse({
                'response_code': HTTP_400_BAD_REQUEST,
                'response_msg': 'Please insert timestamp and checksum'
            }, status = HTTP_400_BAD_REQUEST)

        if timeStamp == nTimestamp_bypass and settings.DEBUG:
            return

        if abs(int(nTimestamp) - int(timeStamp)) > 600:
            return JsonResponse({
                'response_code': HTTP_400_BAD_REQUEST,
                'response_msg': 'Please check timestamp'
            }, status=HTTP_400_BAD_REQUEST)

        strToken   = hashlib.sha256('_'.join([USER_API,PASSWORD_API,timeStamp]).encode('utf-8')).hexdigest()
        if strToken != checksumToken:
            return JsonResponse({
                'response_code': HTTP_401_UNAUTHORIZED,
                'response_msg': 'Invalid Account'
            }, status = HTTP_401_UNAUTHORIZED)

    def process_response(self, request, response):
        #return response
        if request._is_api:
            _request_time = request._request_time
            _response_time = int(time())

            timeExcute = _response_time - _response_time

            keys = sorted(filter(lambda k: re.match(r'(HTTP_|CONTENT_)', k), request.META))
            keys = ['REMOTE_ADDR'] + keys
            meta = {k: request.META[k] for k in keys}

            status = response.status_code
            response_headers = [(str(k), str(v)) for k, v in response.items()]

            for c in response.cookies.values():
                response_headers.append(('Set-Cookie', str(c.output(header=''))))

            headers = ';'.join("%s: %s" % c for c in response_headers)

            _tmpLog = {
                "client_ip": request.META.get('HTTP_HOST'),
                'method': request.method,
                'url': request.get_full_path(),
                'time_excute': timeExcute,
                'meta': meta,
                'headers': headers,
                'status': status,
                'context': json.loads(request._body),
                #'response_msg': json.loads(response.content)
            }

            logger.info(json.dumps(_tmpLog))

        return response

    def _get_logging_context(self, request, response):
        return {
            'args': (),
            'kwargs': {
                'extra': {
                    'request': request,
                    'response': response,
                },
            },
        }
