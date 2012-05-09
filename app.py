import os
from flask import Flask, url_for, render_template, request, redirect, abort
from time import time

app = Flask(__name__)

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

# Has lambdas that check their respective tests' passwords
answers = {
    'idiottest': lambda s: s == 'k8h&a6@',
    'math': lambda s: len(s) == 8,
    'variable': lambda s: s == 'cU8^5-e',
    'escape': lambda s: s == '#j2n*H3',
    'extension': lambda s: s == 'narwhal bacons',
    'obfuscation': lambda s: s == 'o!aZz4v'
}

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

    return render_template(test + '.html', iOS=iOSCheck(request.headers),
                                           time='%d' % time())

@app.route('/<sender>/verify', methods=['GET', 'POST'])
def verify(sender):
    ''' Verify page for each of the tests to make sure they didn't cheat. '''

    if sender not in sequence[:-1]:
        # Only the senders in the sequence list (except the last one) have
        # verify pages, 404 them if the URL is invalid
        abort(404)
    
    if request.method == 'POST':
        # The form was submitted, check their password
        if answers[sender](request.form['pass']):
            # The lambda in answers returned True, they got it right
            return redirect(
                # Advance the index of sender by one, and redirect there
                url_for('test', test=sequence[sequence.index(sender) + 1])
            )
    else:
        # There is no POST, the user tried to enter the URL for this page
        return 'This page has been accessed illegally.'

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
