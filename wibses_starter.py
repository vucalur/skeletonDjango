#!/usr/bin/env python

from optparse import OptionParser
from wibses.py_dict.dict_api import DictionaryUtils


parser = OptionParser()
parser.set_defaults(
    port='8123',
    host='127.0.0.1',
    settings='skeletonDjango.settings',
)

parser.add_option('--port', dest='port')
parser.add_option('--host', dest='host')
parser.add_option('--settings', dest='settings')

options, args = parser.parse_args()

import os

os.environ['DJANGO_SETTINGS_MODULE'] = options.settings
DictionaryUtils.initialize_from_environment()

import fapws._evwsgi as evwsgi
from fapws import base
import sys

sys.setcheckinterval = 100000

from fapws.contrib import django_handler

print 'start on', (options.host, options.port)
evwsgi.start(options.host, options.port)
evwsgi.set_base_module(base)


def generic(environ, start_response):
    res = django_handler.handler(environ, start_response)
    return [res]


evwsgi.wsgi_cb(('', generic))
evwsgi.set_debug(0)
evwsgi.run()