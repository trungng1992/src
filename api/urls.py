from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from api.vnc.api import User
from api.auth.authentication import Authentication

user_get = User.as_view({
    'get' : 'get',
})

user_post = User.as_view({
    'post': 'create_user'
})

ctrl_auth = Authentication.as_view({
    'post': 'check_user'
})

urlpatterns = [
    url(r'user/get/(?P<user_name>[a-zA-Z0-9]+)', user_get),
    url(r'user/create', user_post),
    url(r'auth/check', ctrl_auth)
]
