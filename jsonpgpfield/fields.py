import json
import six

from django.db import models


class NoKeyError(Exception if six.PY3 else StandardError):
    pass


class JSONPGPField(models.Field):

    description = "JSON stored encrypted with asymetric PGP"

    def __init__(self, *args, **kwargs):
        self.public_key = kwargs.pop('public_key', None)
        self.private_key = kwargs.pop('private_key', None)
        super(JSONPGPField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'bytea'

    def get_db_prep_value(self, value, connection, prepared=False):
        if self.null and value is None:
            return None
        return json.dumps(value)

    def get_placeholder(self, value=None, compiler=None, connection=None):
        if not self.public_key:
            raise NoKeyError('No public key to encrypt data')

        return "pgp_pub_encrypt(%s, dearmor('{}'))".format(self.public_key)
