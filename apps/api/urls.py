from django.conf.urls import url

from apps.api.api import User
from apps.api.api import Authentication

user_get = User.as_view({
    'get' : 'get_user_detail',
})

user_post = User.as_view({
    'post': 'create_user'
})

ctrl_auth = Authentication.as_view({
    'post': 'check_user'
})

urlpatterns = [
    url(r'user/get/(?P<username>[a-zA-Z0-9]+)', user_get),
    url(r'user/create', user_post),
    url(r'auth/check', ctrl_auth)
]
