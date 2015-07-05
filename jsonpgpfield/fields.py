from django.db import models


class JSONPGPField(models.Field):

    description = "JSON stored encrypted with asymetric PGP"

    def __init__(self, public_key, private_key, *args, **kwargs):
        self.public_key = public_key
        self.private_key = private_key
        super(JSONPGPField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'bytea'
