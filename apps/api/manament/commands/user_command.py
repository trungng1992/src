from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.api.models import Users
from apps.api.models import Connection_Permission
from apps.api.models import Connection
import random
import string
import hashlib
import binascii
import numpy as np

class Command(BaseCommand):
    help = "Command to check or create user"

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Action: create|check|changepwd|remove|connection')
        parser.add_argument('user', type=str, help='Username')

    def handle(self,  *args, **kwargs):
        _user = kwargs['user']
        _action = kwargs['action']
        if _action == "create":
            self.stdout.write("----Creating".format(_user))

            try:
                # update new password
                _queryDB = Users.objects.get(username=_user)
                _randomPasswordGuacamole = ''.join([random.choice(
                    string.ascii_letters + string.digits)
                    for n in range(10)])

                _passSalt = np.random.bytes(32)
                _passhash = _randomPasswordGuacamole + binascii.hexlify(_passSalt).decode("utf-8").upper()

                m = hashlib.sha256()
                m.update(bytearray(_passhash, "UTF-8"))

                _queryDB.password_hash = m.digest()
                _queryDB.password_salt = _passSalt
                _queryDB.save()

                id = _queryDB.user_id

            except Users.DoesNotExist:
                # create Users
                _queryDB = Users()

                _randomPasswordGuacamole = ''.join([random.choice(
                    string.ascii_letters + string.digits)
                    for n in range(10)])

                _passSalt = np.random.bytes(32)
                _passhash = _randomPasswordGuacamole + binascii.hexlify(_passSalt).decode("utf-8").upper()

                m = hashlib.sha256()
                m.update(bytearray(_passhash, "UTF-8"))

                _queryDB.username = _user
                _queryDB.password_hash = m.digest()
                _queryDB.password_salt = _passSalt
                _queryDB.disabled = 0
                _queryDB.expired = 0
                _queryDB.save()
                id = _queryDB.user_id

            self.stdout.write("|_____Username: {}".format(_user))
            self.stdout.write("|_____Password: {}".format(_randomPasswordGuacamole))

        elif _action == "check":
            self.stdout.write("----Checking user: {}".format(_user))
            try:
                _queryDB = Users.objects.get(username=_user)
                self.stdout.write("|____Result: Exists")
            except Users.DoesNotExist:
                self.stdout.write("|____Result: Not Exists")

        elif _action == "changepwd":
            self.stdout.write("----Change password user: {}".format(_user))
            _password = kwargs['password']
            if not _password:
                self.stderr.write("|____Error: Please input new password")
                return

            try:
                _queryDB = Users.objects.get(username=_user)

                _passSalt = np.random.bytes(32)
                _passhash = _password + binascii.hexlify(_passSalt).decode("utf-8").upper()

                m = hashlib.sha256()
                m.update(bytearray(_passhash, "UTF-8"))

                _queryDB.password_hash = m.digest()
                _queryDB.password_salt = _passSalt
                _queryDB.save()

                self.stdout.write("|____Result: Change password for user {} success.".format(_user))
            except Users.DoesNotExist:
                self.stderr.write("|____Error: User Not Exists")
        elif _action == "remove":
            self.stdout.write("----Remove user: {}".format(_user))
            try:
                _queryDB = Users.objects.get(username=_user)

                _queryDB.delete()

                self.stdout.write("|____Result: Remove user {} success.".format(_user))
            except Users.DoesNotExist:
                self.stderr.write("|____Error: User Not Exists")
        elif  _action == "connection":
            self.stdout.write("----Remove user: {}".format(_user))
            try:
                _queryDB = Users.objects.get(username=_user)
                _queryConnectionPermission = Connection_Permission(user_id=_queryDB)

                if _queryConnectionPermission:
                    nameConnection = []
                    for index in _queryConnectionPermission:
                        _connection_id = _queryConnectionPermission[index]['connection_id']
                        nameConnection.append(Connection.objects.get(connection_id = _connection_id).connection_name)
                    self.stdout.write("|____Result: {}".format(",".join(nameConnection)))
                else:
                    self.stdout.write("|____Result: User {} dose not have connection")
            except Users.DoesNotExist:
                self.stderr.write("|____Error: User Not Exists")