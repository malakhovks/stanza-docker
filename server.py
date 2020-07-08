#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# load tempfile for temporary dir creation
import sys, os, tempfile
# load misc utils
import json
# import uuid
from werkzeug.utils import secure_filename
import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG)
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)

# load libraries for string proccessing
import re, string

# load libraries for API proccessing
from flask import Flask, jsonify, flash, request, Response, redirect, url_for, abort, render_template

# A Flask extension for handling Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
from flask_cors import CORS

ALLOWED_EXTENSIONS = set(['txt', 'xlsx'])

__author__ = "Kyrylo Malakhov <malakhovks@nas.gov.ua>"
__copyright__ = "Copyright (C) 2020 Kyrylo Malakhov <malakhovks@nas.gov.ua>"

app = Flask(__name__)
CORS(app)

"""
Limited the maximum allowed payload to 16 megabytes.
If a larger file is transmitted, Flask will raise an RequestEntityTooLarge exception.
"""
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

"""
Set the secret key to some random bytes. Keep this really secret!
How to generate good secret keys.
A secret key should be as random as possible. Your operating system has ways to generate pretty random data based on a cryptographic random generator. Use the following command to quickly generate a value for Flask.secret_key (or SECRET_KEY):
$ python -c 'import os; print(os.urandom(16))'
b'_5#y2L"F4Q8z\n\xec]/'
"""
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.secret_key = os.urandom(42)

# Init Stanza (load models too)
import stanza

try:
    snlp = stanza.Pipeline(lang="nb", processors='tokenize,mwt,pos,lemma', dir='./deploy/stanza_resources')
except:
    logging.debug('Installing Stance pretrained NLP model for Norwegian Bokmaal.')
    stanza.download('nb', dir='./deploy/stanza_resources')
    logging.debug('Stance pretrained NLP model for Norwegian Bokmaal is ready to use.')
    snlp = stanza.Pipeline(lang="nb", processors='tokenize,mwt,pos,lemma', dir='./deploy/stanza_resources')

@app.route('/')
def index():
    return 'Hello, Stanza in Docker!'

@app.route('/test/message', methods=['POST'])
def get_nlp():
    req_data = request.get_json()
    # get messge from JSON
    # Example of POST JSON data
    # {'message': 'Formuesskatten er en skatt som utlignes på grunnlag av nettoformuen din.'}
    sdoc = snlp(req_data['message'])
    s_arr = [word.lemma_ for word in sdoc]
    doc = {'doc': req_data['message']}
    doc['lemmas'] = s_arr
    return Response(json.dumps(doc), mimetype='application/json')

if __name__ == '__main__':
    # default port = 5000
    app.run(host = '0.0.0.0')