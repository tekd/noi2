from flask import current_app, make_response

from hashlib import sha256
from base64 import b64encode
import functools

def add_header(response):
    '''
    Add a Content Security Policy (CSP) header to the given response.
    '''

    script_src = [
        "'self'",
        "use.typekit.net"
    ]

    if current_app.debug:
        # https://github.com/mgood/flask-debugtoolbar/issues/88
        m = sha256()
        m.update("var DEBUG_TOOLBAR_STATIC_PATH = '/_debug_toolbar/static/'")
        script_src.append("'sha256-%s'" % b64encode(m.digest()))

    if hasattr(response, '_csp_script_src'):
        script_src += response._csp_script_src

    response.headers.add('Content-Security-Policy-Report-Only',
                         'script-src %s' % ' '.join(script_src))
    return response

def script_src(source_list):
    '''
    Add additional script-src sources to the CSP header.
    '''

    def decorator(func):
        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            response = make_response(func(*args, **kwargs))
            response._csp_script_src = ['*']
            return response
        return func_wrapper
    return decorator
