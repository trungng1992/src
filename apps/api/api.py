from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import ViewSet

from apps.api.models import Users
from apps.api.models import Connection
from apps.api.models import Connection_Parameter
from apps.api.models import Connection_Permission
from django.conf import settings
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

            m = hashlib.sha256()
            m.update(bytearray(_passhash,"UTF-8"))

            _queryDB.password_hash = m.digest()
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

        _rsp = _helperVNC.create_vnc(_userName, _randomPassword, id)

        if _rsp.status_code == 500:
            return Response({
                'response_code' : HTTP_500_INTERNAL_SERVER_ERROR,
                'response_msg': 'Internal Error. Please contact p.sns.tos@vng.ocm.vn to get more information'
            }, HTTP_500_INTERNAL_SERVER_ERROR)

        #return Response(_rsp.text)
        if not settings.DEBUG or 1:
            _jsonResponse = _rsp.json()
        else:
            _jsonResponse = {
                'response_code': 200,
                'response_msg' : {
                    'container_service' : 'vnc',
                    'container_port'    : '5901',
                    'container_ip'      : "10.10.10.10",
                    "container_name"    : "test_debug"
                }
            }

        _vnc_name = 'vnc-{}-{}'.format(_userName,id)

        if int(_jsonResponse['response_code']) == 200:
            #Create successfull
            _arrResponse = _jsonResponse['response_msg']
            _rsp_service = _arrResponse['container_service']
            _rsp_port    = _arrResponse['container_port']
            _rsp_ip      = _arrResponse['container_ip']
            _rsp_name    = _arrResponse['container_name']
            _rsp_user    = _arrResponse['container_user']


            try:
                _tmpConnection = Connection.objects.get(connection_name__contains=_vnc_name)

                _tmpHostnameParameter = Connection_Parameter(parameter_name="hostname",  connection_id=_rsp_ip)
                _tmpHostnameParameter.parameter_value = _rsp_ip
                _tmpHostnameParameter.save()

                _tmpPassParameter =  Connection_Parameter(id=None, parameter_name="password", parameter_value=_randomPassword,  connection_id=_tmpConnection)
                _tmpPassParameter.save()

                _tmpPortParameter = Connection_Parameter(id=None, parameter_name="port", parameter_value=_rsp_port,  connection_id=_tmpConnection)
                _tmpPortParameter.save()

            except Connection.DoesNotExist:
                _tmpConnection = Connection()
                _tmpConnection.connection_name = _rsp_name
                #_tmpConnection.protocol = _rsp_service.lower()
                _tmpConnection.protocol = "rdp"
                _tmpConnection.max_connections = 1
                _tmpConnection.max_connections_per_user = 1
                _tmpConnection.proxy_encryption_method = None
                _tmpConnection.proxy_hostname = None
                _tmpConnection.failover_only = 0
                _tmpConnection.save()

                _tmpColorParameter = Connection_Parameter(id=None, parameter_name="color-depth", parameter_value="16", connection_id=_tmpConnection)
                _tmpColorParameter.save()

                _tmpHostnameParameter = Connection_Parameter(id=None, parameter_name="hostname", parameter_value=_rsp_ip,  connection_id=_tmpConnection)
                _tmpHostnameParameter.save()

                _tmpPassParameter =  Connection_Parameter(id=None, parameter_name="password", parameter_value=_randomPassword,  connection_id=_tmpConnection)
                _tmpPassParameter.save()

                _tmpPortParameter = Connection_Parameter(id=None, parameter_name="port", parameter_value=_rsp_port,  connection_id=_tmpConnection)
                _tmpPortParameter.save()

                _tmpAudioParameter = Connection_Parameter(id=None, parameter_name="disable-audio", parameter_value="true", connection_id= _tmpConnection)
                _tmpAudioParameter.save()

                _tmpKeyboardParameter = Connection_Parameter(id=None, parameter_name="server-layout", parameter_value="en-us-qwerty", connection_id=_tmpConnection)
                _tmpAudioParameter.save()

                _tmpUserParameter = Connection_Parameter(id=None, parameter_name = "username", parameter_value=_rsp_user, connection_id= _tmpConnection)
                _tmpUserParameter.save()


                _tmpConnectionPermission = Connection_Permission(id=None,  connection_id=_tmpConnection, user_id = _queryDB, permission="READ")
                _tmpConnectionPermission.save()

        elif int(_jsonResponse['response_code']) == 201:
            #Connection is exists
            _tmpConnection = Connection.objects.get(connection_name__contains  = _vnc_name)

            if _tmpConnection.status_code == 200:
                _jsonTmpConnection = _tmpConnection.json()
                _tmpHostnameParameter = Connection_Parameter(parameter_name="hostname",  connection_id=_tmpConnection)
                _tmpHostnameParameter.parameter_value = _jsonTmpConnection['response_msg']['container_ip']

                _tmpHostnameParameter.save()

        return Response({
            'response_code': _jsonResponse['response_code'],
            'response_msg': {
                'container': _jsonResponse['response_msg'],
                'guacamole': {
                    'user': _userName,
                    'pass': _randomPasswordGuacamole
                }
            }
        }, status= _jsonResponse['response_code'])


class Authentication(ViewSet):
    def check_user(self, request, *agrs, **kwargs):
        _arrRequestParamKeys = request.data.keys()
        # return Response(request.POST.dict())
        if 'username' not in _arrRequestParamKeys or 'password' not in _arrRequestParamKeys:

            return Response({
                'response_code': HTTP_400_BAD_REQUEST,
                'response_msg': 'Invalid Requests'
            }, status = HTTP_400_BAD_REQUEST)

        _userName = request.data['username']
        _password = request.data['password']

        try:
            _queryDB = Users.objects.get(username=_userName)
        except Users.DoesNotExist:
            return Response({
                'response_code': HTTP_400_BAD_REQUEST,
                'response_msg' : 'User {} is not exists.'.format(_userName)
            }, status = HTTP_400_BAD_REQUEST)

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
                'response_msg'  : "Wrong password. Please contact p.sns.tos to renew password"
            }, status = HTTP_400_BAD_REQUEST)

