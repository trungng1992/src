from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from api.models import Users
from api.models import Connection
from api.models import Connection_Parameter
from api.models import Connection_Permission

from helpers.container_vnc import ContainerVNC
import numpy as np
import binascii
import hashlib
import random
import string

class User(ViewSet):
    def get_user_detail(self, request, *agrs, **kwargs):
        if 'username' not in kwargs:
            return Response({
                'response_code': HTTP_400_BAD_REQUEST,
                'response_msg': 'Can not get information of requests'
            }, status = HTTP_400_BAD_REQUEST)
        else:
            name = Users.objects.get(username=kwargs['username'])
            try:
                name = Users.objects.get(username=kwargs['username'])

                return Response({
                    'response_code': HTTP_200_OK,
                    'response_msg': 'Success',
                    'data': name.user_id
                }, status = HTTP_200_OK)

            except Users.DoesNotExist:
                name = []

                return Response({
                    'response_code': HTTP_400_BAD_REQUEST,
                    'response_msg': 'Users invalid',
                    'data': name
                }, status = HTTP_400_BAD_REQUEST)

    def create_user(self, request, *args, **kwargs):
        _arrRequestParamKeys = request.data.keys()
        if 'username' not in _arrRequestParamKeys:
            return Response({
                'response_code': HTTP_400_BAD_REQUEST,
                'response_msg': 'Invalid Requests'
            }, status = HTTP_400_BAD_REQUEST)

        _userName = request.data['username']

        try:
            #update new password
            _queryDB = Users.objects.get(username=_userName)
            _randomPasswordGuacamole = ''.join([random.choice(
                    string.ascii_letters + string.digits)
                     for n in range(10)])

            _passSalt = np.random.bytes(32)
            _passhash = _randomPasswordGuacamole+binascii.hexlify(_passSalt).decode("utf-8").upper()

            _queryDB.password_hash = _passhash
            _queryDB.password_salt = _passSalt
            _queryDB.save()


            id = _queryDB.user_id

        except Users.DoesNotExist:
            #create Users
            _queryDB = Users()

            _randomPasswordGuacamole = ''.join([random.choice(
                    string.ascii_letters + string.digits)
                     for n in range(10)])

            _passSalt = np.random.bytes(32)
            _passhash = _randomPasswordGuacamole+binascii.hexlify(_passSalt).decode("utf-8").upper()

            m = hashlib.sha256()
            m.update(bytearray(_passhash,"UTF-8"))

            _queryDB.username = _userName
            _queryDB.password_hash = m.digest()
            _queryDB.password_salt = _passSalt
            _queryDB.disabled = 0
            _queryDB.expired = 0
            _queryDB.save()
            id = _queryDB.user_id

        _helperVNC = ContainerVNC(_userName)

        _randomPassword = ''.join([random.choice(
                string.ascii_letters + string.digits)
                 for n in range(8)])

        _rsp = _helperVNC.create_vnc(_userName, _randomPassword, 2)

        if _rsp.status_code == 500:
            return Response({
                'response_code' : HTTP_500_INTERNAL_SERVER_ERROR,
                'response_msg': 'Internal Error. Please contact p.sns.tos@vng.ocm.vn to get more information'
            }, HTTP_500_INTERNAL_SERVER_ERROR)

        #return Response(_rsp.text)
        _jsonResponse = json.load(_rsp.text)

        if _jsonResponse['response_code'] == 200:
            _arrResponse = _jsonResponse['response_msg']
            _rsp_service = _arrResponse['container_service']
            _rsp_port    = _arrResponse['container_port']
            _rsp_ip      = _arrResponse['container_ip']
            _rsp_name    = _arrResponse['container_name']

            _tmpConnection = Connection()
            _tmpConnection.connection_name = _rsp_name
            _tmpConnection.protocol = _rsp_service.lower()
            _tmpConnection.max_connections = 2
            _tmpConnection.max_connections_per_user = 1
            _tmpConnection.proxy_encryption_method = None
            _tmpConnection.proxy_hostname = None
            _tmpConnection.save()

            _tmpColorParameter = Connection_Parameter(id=None, parameter_name="color-depth", parameter_value="24", connection_id=_tmpConnection)
            _tmpColorParameter.save()

            _tmpHostnameParameter = Connection_Parameter(id=None, parameter_name="hostname", parameter_value=_rsp_ip,  connection_id=_tmpConnection)
            _tmpHostnameParameter.save()

            _tmpPassParameter =  Connection_Parameter(id=None, parameter_name="password", parameter_value=_randomPassword,  connection_id=_tmpConnection)
            _tmpPassParameter.save()

            _tmpPortParameter = Connection_Parameter(id=None, parameter_name="port", parameter_value=_rsp_port,  connection_id=_tmpConnection)
            _tmpPortParameter.save()

            _tmpConnectionPermission = Connection_Permission(id=None,  connection_id=_tmpConnection, user_id = _queryDB)
            _tmpConnectionPermission.save()

        return Response({
            'response_code': _jsonResponse['response_code'],
            'response_msg': _jsonResponse['response_msg']
        }, status= _jsonResponse['response_code'])
