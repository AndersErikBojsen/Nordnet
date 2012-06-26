#!/usr/bin/env python

"""
Module for connecting to the REST services of the API
"""

import time
from base64 import b64encode
from M2Crypto import RSA
import httplib
import urllib
from json import loads as jloads

from nordnet.config import NordnetConfig
from nordnet.utils import print_json

config = NordnetConfig()

headers = {
    'Content-type' : 'application/x-www-form-urlencoded',
    'Accept' : 'application/json',
    'Accept-language' : 'en'
    }

__all__ = ['make_hash', 'connect', 'get_status', 'login']

def make_hash():
    """ Makes the key for authentication according to the
    specification on Nordnets page """
    timestamp = str(int(round(time.time()*1000)))
    auth = b64encode(config.username) + ':' \
        + b64encode(config.password) + ':' \
        + b64encode(config.username)
    rsa = RSA.load_pub_key(config.public_key)
    encrypted_auth = rsa.public_encrypt(auth, RSA.pkcs1_padding)
    return b64encode(encrypted_auth)         

def connect():
    """ Establishing a connection """
    return httplib.HTTPSConnection(config.url)

def get_status(connection):
    """ Gets the server status """
    if not connection:
        connection = connect()
    connection.request('GET', 
                       'https://' + config.base_url \
                           + '/' + config.api_version, 
                       '',
                       headers)
    response = jloads(connection.getresponse().read())
    return response

def login(connection, hash):
    """ Logs in to the server """
    parameters = urllib.urlencode({ 'service' : config.service,
                                    'auth' : hash })
    connection.request('POST', 
                       'https://' + config.base_url \
                           + '/' + config.api_version + '/login',
                       parameters,
                       headers)
    response = jloads(connection.getresponse().read())
    return response