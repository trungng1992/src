from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from api.models import User

from helpers.container_vnc import ContainerVNC
from numpy as np
import binascii
import hashlib

class User(ViewSet):
    def get_user_detail(self, request, *agrs, **kwargs):
        return Response({
            response_code: 'asdasd'
        })
        if 'username' not in kwargs:
            return Response({
                'response_code': HTTP_400_BAD_REQUEST,
                'response_msg': 'Can not get information of requests'
            }, status = HTTP_400_BAD_REQUEST)
        else:
            try:
                name = User.objects.get(username=kwargs['username'])

                return Response({
                    'response_code': HTTP_200_OK,
                    'response_msg': 'Success',
                    'data': name.user_id
                }, status = HTTP_200_OK)

            except User.DoesNotExist:
                name = []

                return Response({
                    'response_code': HTTP_400_BAD_REQUEST,
                    'response_msg': 'User invalid',
                    'data': name
                }, status = HTTP_400_BAD_REQUEST)

    def create_user(self, request, *args, **kwargs):

        _arrRequestParamKeys = kwargs.keys()
        if 'username' not in _arrRequestParamKeys:
            return Response({
                'response_code': HTTP_400_BAD_REQUEST,
                'response_msg': 'Invalid Requests'
            }, status = HTTP_400_BAD_REQUEST)

        _userName = kwargs['username']

        try:
            #update new password
            _queryDB = User.object.get(_userName)
            _randomPasswordGuacamole = ''.join([random.choice(
                    string.ascii_letters + string.digits)
                     for n in range(10)])

            _passSalt = np.random.bytes(32)
            _passhash = _randomPasswordGuacamole+binascii.hexlify(_passSalt).upper()

            _queryDB.password_hash = _passhash
            _queryDB.password_salt = _passSalt
            _queryDB.save()


            id = _queryDB.user_id

        except User.DoesNotExist:
            #create User
            _queryDB = User()

            _randomPasswordGuacamole = ''.join([random.choice(
                    string.ascii_letters + string.digits)
                     for n in range(10)])

            _passSalt = np.random.bytes(32)
            _passhash = _randomPasswordGuacamole+binascii.hexlify(_passSalt).upper()

            m = hashlib.sha256()
            m.update(bytearray(_passhash,"UTF-8"))

            _queryDB.username = _userName
            _queryDB.password_hash = m.digest()
            _queryDB.password_salt = _passSalt
            _queryDB.save()
            id = _queryDB.user_id

        _helperVNC = ContainerVNC(k)

        _randomPassword = ''.join([random.choice(
                string.ascii_letters + string.digits)
                 for n in range(8)])

        _rsp = _helperVNC.create_vnc(_userName, pswd, id)

        if _rsp.status_code == 500:
            return Response({
                'response_code' : HTTP_500_INTERNAL_SERVER_ERROR,
                'response_msg': 'Internal Error. Please contact p.sns.tos@vng.ocm.vn to get more information'
            }, HTTP_500_INTERNAL_SERVER_ERROR)


        _jsonResponse = json.load(_rsp.text)
        return Response({
            'response_code': _jsonResponse['response_code'],
            'response_msg': _jsonResponse['response_msg']
        }, status= _jsonResponse['response_code'])
