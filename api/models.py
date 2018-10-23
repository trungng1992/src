from django.db import models
from datetime import datetime

from enum import Enum
class PERMISSION(Enum):
    READ = 'READ'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    ADMINISTER = 'ADMINISTER'


class User(models.Model):
    '''
    Table: guacamole_user
    '''
    class Meta:
        db_table = "guacamole_user"
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length = 128, unique=True, null=False)
    password_hash = models.BinaryField(max_length=32, null=False)
    password_salt = models.BinaryField(max_length=32, null=False)
    password_date = models.DateTimeField(auto_now=True)
    disable = models.PositiveSmallIntegerField()
    expired = models.PositiveSmallIntegerField()
    access_window_start = models.DateTimeField()
    access_window_end = models.DateTimeField()
    valid_from = models.DateField()
    valid_util = models.DateField()
    timezone = models.CharField(max_length=64)
    fullname = models.CharField(max_length=256)
    email_address = models.CharField(max_length=256)
    organization = models.CharField(max_length=256)
    organization_role = models.CharField(max_length=256)

class Connection(models.Model):
    '''
    Table: guacamole_connection
    '''
    class Meta:
        db_table = "guacamole_connection"
    connection_id  = models.AutoField(primary_key=True)
    connection_name = models.CharField(max_length = 11, null=False)
    parent_id = models.IntegerField()
    protocol = models.CharField(max_length = 11, null = False)
    proxy_port = models.IntegerField()
    proxy_hostname = models.CharField(max_length=512)
    proxy_encryption_method = models.CharField(max_length=255)
    max_connections = models.IntegerField()
    max_conenctions_per_user = models.IntegerField()
    connection_weight = models.IntegerField()
    failover_only = models.PositiveSmallIntegerField()

class Connection_Parameter(models.Model):
    '''
    Table: guacamole_connection_parameter
    '''
    class Meta:
        db_table = "guacamole_connection_parameter"
    connection_id =  models.ForeignKey(
        Connection,
        on_delete=models.CASCADE,
        blank = False,
        null = False
    )
    parameter_name = models.CharField(max_length=128)
    parameter_value = models.CharField(max_length=4096)

class Connection_Permission(models.Model):
    '''
    Table: guacamole_connection_permission
    '''
    class Meta:
        db_table = "guacamole_connection_permission"
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank = False,
        null = False
    )

    connection_id = models.ForeignKey(
        Connection,
        on_delete=models.CASCADE,
        blank = False,
        null = False
    )

    permission = models.CharField(
        max_length = 10,
        choices = [(tag, tag.value) for tag in PERMISSION]
    )
