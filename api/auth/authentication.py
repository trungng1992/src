from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from api.models import Users

from helpers.container_vnc import ContainerVNC
import numpy as np
import binascii
import hashlib

class Authentication(ViewSet):
    def check_user(self, request, *agrs, **kwargs):
        _arrRequestParamKeys = request.data.keys()
        if 'username' not in _arrRequestParamKeys or 'password' not in _arrRequestParamKeys:

            return Response({
                'response_code': HTTP_400_BAD_REQUEST,
                'response_msg': 'Invalid Requests'
            }, status = HTTP_400_BAD_REQUEST)

        _userName = request.data['username']
        _password = request.data['password']

        _queryDB = Users.objects.get(username=_userName)

        _passSalt = _password + binascii.hexlify(_queryDB.password_salt).decode("utf-8").upper()

        m = hashlib.sha256()
        m.update(bytearray(_passSalt,"UTF-8"))

        _passhash = binascii.hexlify(m.digest())
        _passHashInDB = binascii.hexlify(_queryDB.password_hash)

        if _passhash == _passHashInDB:
            return  Response({
                'response_code': HTTP_200_OK,
                'response_msg' : "Success",
            }, status = HTTP_200_OK)
        else:
            return Response({
                'response_code' : HTTP_400_BAD_REQUEST,
                'response_msg'  : "Faied"
            }, status = HTTP_400_BAD_REQUEST)
