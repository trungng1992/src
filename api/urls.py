from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

#from api.api import User
#from api.api import Connection

# user_view = User.as_view({
#     'get' : 'get',
# })

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index')
]
