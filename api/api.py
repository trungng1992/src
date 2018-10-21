from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

from api.models import User
class User(ViewSet):
    def get(self, request, *agrs, **kwargs):
        return Response({
            response_code: 'asdasd'
        })
        if 'username' not in kwargs:
            return Response({
                'response_code': HTTP_400_BAD_REQUEST,
                'response_msg': 'Can not get information of requests'
            })
        else:
            name = User.objects.get(username=kwargs['username'])
            return Response({
                'response_code': HTTP_200_OK,
                'response_msg': 'Success',
                'data': name.user_id
            })
