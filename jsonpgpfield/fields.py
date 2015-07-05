from django.db import models


class JSONPGPField(models.Field):

    description = "JSON stored encrypted with asymetric PGP"

    def db_type(self, connection):
        return 'bytea'
