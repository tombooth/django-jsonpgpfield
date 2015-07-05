from django.db import models
from django.test import TestCase

from jsonpgpfield.fields import JSONPGPField, NoKeyError


PUBLIC_KEY = '''
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG/MacGPG2 v2
Comment: GPGTools - https://gpgtools.org

mQENBFWZj9EBCADIQ8tp3mSNLHln0ICBdspYAfVgvnAmD+hA2wllaucXLUXLHCeK
xTtWVCsU4HSDa0s3o6BpPzb8+0Ko+KWbXeHooUoQZHbtKFF+agbP8T9zllZ2P6LM
6xPt8s0m0hJk9VB8l03stj2PWzuYtk4TQdBN9szm3KI2fz8cW6ndQfCvvjDsqtsM
eJmqzwzNyhQkTsTf1m37A4MOYt41fEsq7Tj55Gpwf6I+sc2SRU/3xmYpoX/vePUs
YJFLHQtEPLfeB9iPS+e4Q7qgk3dgjd2lJBwUa7UtZltCKxeLCDOkZF3LB0reX2xB
kNulfeCzQMObeBVvrrVexzJmQSOQPeHNv0wLABEBAAG0VkpTT05QR1BGaWVsZCB0
ZXN0IChBIHRlc3Qga2V5IHBhaXIgZm9yIEpTT05QR1BGaWVsZCkgPHRvbWJvb3Ro
K2pzb25wZ3BmaWVsZEBnbWFpbC5jb20+iQE3BBMBCgAhBQJVmY/RAhsDBQsJCAcD
BRUKCQgLBRYCAwEAAh4BAheAAAoJELiEoxoCruLn1IsIAMeJFYgpTf49mVlrzBMZ
s3c5o0/9mQIq21REZDPtPtMGmgpLooWRud1KTMAAH6cX79j723SjGkcIE1yEQCl3
0JRw50vg88+oenWKt3eT5zierwAKgNcaa57LvxrxT96UllozcASi2cjaCi0Sii0f
4n+JXH6OR+/8FtYbIzhB/PvEoBSaymdeP4yJ2/RcHxQHORSmt/4JbpXylTb6c8bN
VK+985qclIJhC6ewn0usX03azv4gtkl+g/V3cjpSvhqaWCWCacddiva4ylhGzi64
jPZEPITkxWmePFNkI4iuuIoguW7Y0Ep1SqwAwqUbfqj4G/csZ/n39329zfQO49mu
O1S5AQ0EVZmP0QEIAMSsas8f/GTeNzVFzD5LeImL2dX42ua5R9BWuef+mpQpeFuZ
SGFs1ot2JkzJOIuVr7+685AzsiYLLBLXJAtlrFtUvpVncUQtJ0w8uk4HZSucr90w
L6dOpsAm/sJeso8c1FBB149I1oZZXjr91MAlBzx+5RYCpzuaJhP6MSUgRQGskvtt
h5fU6UCdKjtDv1C/UsF0nT5GLhBPE0pEKsX3hezJOwJhRTJsFiDojn27pnLMJuJP
GI+FC5pARRC7ImKQwH2vIz3fD5aSj/deB5YOevDdFAEHCl5RxRQgNl8a2oDzUH4u
2CrmzlOK0YVcVtYMvBC2uxW/lW0JVnBm1m8hmh0AEQEAAYkBHwQYAQoACQUCVZmP
0QIbDAAKCRC4hKMaAq7i58pYCACxgHYoA815zNUIr1P4SbobRl09onR9jzibqhRI
+AuQ9euGKefNUOz3v77GVkWgRSHinpv0CCQ85Dh4vgZD2J0R8zezaExXCiQ+me4h
a/tzlPY2LYkA5j7zh3K02uAxelao3/FiLxfSF7HiKw9hT6RlB8Z+HvIR9Pwme3J+
s9EGeD9zqULAW9xPujeKO1o3mwDsgl0dYt+u/E921+lUXPhDcT4tofTJafRCZbnc
iNVLdgoi05GTa+rs5bxshfJV+txnv01TKzEuQOpJRYusLnYU8Hhf27ckVBZwZQCD
p/FED08W0fTuz39I7M/bqXkwM5PxNUC87YGnVp3pr0/9qxyU
=Xhb9
-----END PGP PUBLIC KEY BLOCK-----
'''

PRIVATE_KEY = '''
-----BEGIN PGP PRIVATE KEY BLOCK-----
Version: GnuPG/MacGPG2 v2
Comment: GPGTools - https://gpgtools.org

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
=2Igm
-----END PGP PRIVATE KEY BLOCK-----
'''


class TestModel(models.Model):
    secure_json = JSONPGPField(
        public_key=PUBLIC_KEY, private_key=PRIVATE_KEY)


class NoPublicKeyModel(models.Model):
    secure_json = JSONPGPField(private_key=PRIVATE_KEY)


class JSONPGPFieldTest(TestCase):

    def test_keys_stored(self):
        model = TestModel.objects.create()
        field = model._meta.get_field('secure_json')

        self.assertEqual(field.public_key, PUBLIC_KEY)
        self.assertEqual(field.private_key, PRIVATE_KEY)

    def test_storing_value(self):
        model = TestModel()
        model.secure_json = {
            'foo': 'bar',
        }
        model.save()

        self.assertEqual(model.secure_json['foo'], 'bar')

    def test_storing_value_with_no_public_raises(self):
        model = NoPublicKeyModel()
        model.secure_json = {
            'foo': 'bar',
        }

        raised = False
        try:
            model.save()
        except NoKeyError:
            raised = True

        self.assertTrue(raised)
