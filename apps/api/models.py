from django.db import models
from datetime import datetime

from enum import Enum
class PERMISSION(Enum):
    READ = 'READ'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    ADMINISTER = 'ADMINISTER'

class Users(models.Model):
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
    disabled = models.PositiveSmallIntegerField()
    expired = models.PositiveSmallIntegerField()
    access_window_start = models.DateTimeField()
    access_window_end = models.DateTimeField()
    valid_from = models.DateField()
    valid_until = models.DateField()
    timezone = models.CharField(max_length=64)
    full_name = models.CharField(max_length=256)
    email_address = models.CharField(max_length=256)
    organization = models.CharField(max_length=256)
    organizational_role = models.CharField(max_length=256)

    objects = models.Manager()
    test_abc = models.Manager()

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
    max_connections_per_user = models.IntegerField()
    connection_weight = models.IntegerField()
    failover_only = models.PositiveSmallIntegerField()
    objects = models.Manager()

class Connection_Parameter(models.Model):
    '''
    Table: guacamole_connection_parameter
    '''
    class Meta:
        managed = False
        db_table = "guacamole_connection_parameter"

    connection_id =  models.ForeignKey(
        Connection,
        db_column="connection_id",
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
        managed = False
        db_table = "guacamole_connection_permission"

    user_id = models.ForeignKey(
        Users,
        db_column="user_id",
        on_delete=models.CASCADE,
        blank = False,
        null = False
    )

    connection_id = models.ForeignKey(
        Connection,
        db_column="connection_id",
        on_delete=models.CASCADE,
        blank = False,
        null = False
    )

    permission = models.CharField(
        max_length = 10,
        choices = [(tag, tag.value) for tag in PERMISSION]
    )


class UserOOB(models.Model):
    '''
     Table: tbl_user_info
    '''

    class Meta:
        managed = False
        db_table = "tbl_user_info"

    id = models.AutoField(primary_key=True)
    serial = models.CharField(max_length=100, null=False)
    ip_console = models.CharField(max_length=100, null=False)
    type = models.CharField(max_length=10, null=False)
    version = models.CharField(max_length=20, null=False)
    firmware = models.CharField(max_length=20, null=False)
    domain = models.CharField(max_length=100, null=False)
    site = models.CharField(max_length=50, null=False)
    user_admin = models.CharField(max_length=255, null=False)
    pass_admin = models.CharField(max_length=255, null=False)
    pass_console = models.CharField(max_length=255, null=False)
    user_oob = models.CharField(max_length=255, null=False)
    pass_oob = models.CharField(max_length=255, null = False)