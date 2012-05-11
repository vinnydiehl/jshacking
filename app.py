# JavaScript Hacking - A skill test for finding vulnerabilities in JavaScript.
# Copyright (C) 2012 Vinny Diehl
#
# This application is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This application is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this application.  If not, see <http://www.gnu.org/licenses/>.

import os
from flask import Flask, url_for, render_template, request, \
                  redirect, abort, session
from time import time
from random import random

app = Flask(__name__)

globals()['key'] = int(random() * 1e8 + 1e8) # big random number

def iOSCheck(head):
    ''' Checks if the user is on an iOS device. '''
    return True in [
                    device in head['User-Agent'].lower()
                    for device in 'iphone', 'ipod', 'ipad'
                   ]

# The ordered sequence of tests
sequence = [
    'idiottest', 'math', 'variable', 'escape',
    'extension', 'obfuscation', 'winrar'
]

def generate_answer(test):
    ''' Prototypical attempt at generating unique answers for each session. '''
    key = globals()['key']
    if test == 'idiottest':
        # turn the key into a random string of 8 capital letters
        return ''.join(chr((key % 128 * i) % 26 + 65) for i in range(2, 10))

# Mapping of tests to acceptable password criteria
answers = {
    'idiottest':   generate_answer('idiottest'),
    'math':        8,
    'variable':    'cU8^5-e',
    'escape':      '#j2n*H3',
    'extension':   'narwhal bacons',
    'obfuscation': 'o!aZz4v'
}

def prepare(sender):
    ''' Adjusts input prior to comparison against test criteria. '''
    return len if sender == 'math' else str

@app.route('/')
def index():
    ''' Home page and intro.'''
    return render_template('index.html', iOS=iOSCheck(request.headers),
                                         time='%d' % time())

@app.route('/<test>/')
def test(test):
    ''' The rest of these are the pages with the tests. '''
    if test not in sequence:
        # If the URL is not that of one of the tests, 404
        abort(404)

    if test != sequence[0] and \
       not session.get(sequence[sequence.index(test) - 1], False):
        return 'Page accessed illegally.'

    return render_template(test + '.html', iOS=iOSCheck(request.headers),
                                           time='%d' % time(),
                                           answer=generate_answer(test))

@app.route('/<sender>/verify', methods=['GET', 'POST'])
def verify(sender):
    ''' Verify page for each of the tests to make sure they didn't cheat. '''

    if sender not in sequence[:-1]:
        # Only the senders in the sequence list (except the last one) have
        # verify pages, 404 them if the URL is invalid
        abort(404)

    if request.method == 'POST':
        # The form was submitted, check their password
        if answers[sender] == prepare(sender)(request.form['pass']):
            # The prepared password meets the necessary criteria, STAGE CLEAR!
            session[sender] = True
            return redirect(
                # Advance the index of sender by one, and redirect there
                url_for('test', test=sequence[sequence.index(sender) + 1])
            )
    else:
        # There is no POST, the user tried to enter the URL for this page
        return 'This page has been accessed illegally.'

# Read in the secret_key from key.pvt
# key.pvt is on the server, but not on GitHub.
# Create your own secret_key if you wish to run this application.
app.secret_key = open('key.pvt').read()

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
