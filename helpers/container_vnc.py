'''
Author: TrungN

Call API use to check, create container
'''

import json, hashlib, requests
from time import time

TOSAPI_USER = "tosapi"
TOSAPI_PASSWORD = "eWEZ3UXugKV"

IP_URL = "10.12.167.200"

class ContainerVNC(object):
    def __init__(self, user_name):
        self.user_name = user_name
        self.url = "http://{}/api/docker/vnc".format(IP_URL)

    def __get_header(self):
        nTimestamp   = str(int(time()))
        strToken   = hashlib.sha256('_'.join([
                        TOSAPI_USER,
                        TOSAPI_PASSWORD,
                        nTimestamp]).encode('utf-8')).hexdigest()

        custom_header = {
            'Checksum-Token' : str(strToken),
            'TimeStamp' : str(nTimestamp),
            'Content-Type': 'application/json'
        }

        return custom_header

    def create_vnc(self, user, pswd, id):
        payload = {
            "id"        : str(id),
            "user"      : user,
            "pass"      : pswd
        }

        data = json.dumps(payload)

        r = requests.post(self.url + "/create", headers = self.__get_header(), data = data)
        return r

    def get_status_vnc(self, connection_name):
        r = requests.get(self.url + "/status/" + connection_name,   headers= self.__get_header())

        return r

    def delete_vnc(self, connection_name):
        r = requests.delete(self.url + '/delete' + connection_name, headers = self.__get_header())

        return r

    def get_connection_vnc(self, connection_name):
        r = requests.get(self.url + "/connection/" + connection_name,   headers= self.__get_header())

        return r


    def get_info_vnc(self, connection_name):
        r = requests.get(self.url + '/info/' + connection_name, headers = self.__get_header())

        return r
