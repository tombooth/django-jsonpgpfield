from __future__ import print_function

import os
import sys

from distutils.core import setup
from distutils.core import Command

try:
    from urllib.parse import urlparse  # Python 3
except ImportError:
    from urlparse import urlparse  # Python 2

def load_databases_from_url(url):
    # eg postgres://user3123:pass123@database.foo.com:6212/db982398
    DATABASE_URL = urlparse(url)
    return {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DATABASE_URL.path[1:],
            'USER': DATABASE_URL.username,
            'PASSWORD': DATABASE_URL.password,
            'HOST': DATABASE_URL.hostname,
            'PORT': DATABASE_URL.port,
        }
    }

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if not 'DATABASE_URL' in os.environ:
            print('DATABASE_URL environment variable required')
            sys.exit(1)

        from django.conf import settings
        settings.configure(
            DATABASES=load_databases_from_url(os.environ['DATABASE_URL']),
            INSTALLED_APPS=('jsonpgpfield','tests',))

        from django.core.management import call_command
        import django

        django.setup()
        call_command('test', 'tests')

setup(name='jsonpgpfield',
    version='0.1.0',
    packages=['jsonpgpfield'],
    license='MIT',
    include_package_data=True,
    author='Tom Booth',
    author_email='tombooth@gmail.com',
    url='https://github.com/tombooth/django-jsonpgpfield/',
    description='A reusable Django field that allows you to store encrypted and validated JSON in your model.',
    long_description=open("README.rst").read(),
    install_requires=['Django >= 1.8.0'],
    tests_require=[
        'Django >= 1.8.0',
        'psycopg2 >= 2.5.4',
        'six = 1.9.0',
    ],
    cmdclass={'test': TestCommand},
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
    ],
)
