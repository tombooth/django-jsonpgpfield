from django.db import migrations


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.RunSQL(
            'CREATE EXTENSION IF NOT EXISTS pgcrypto;',
            'DROP EXTENSION pgcrypto;',
        ),
    ]
