import hmac
import base64
import urlparse
import urllib
from hashlib import sha256

from .config import config

if hasattr(hmac, 'compare_digest'):
    compare_digest = hmac.compare_digest
else:
    # Slightly modified from http://stackoverflow.com/a/18173992.
    def compare_digest(x, y):
        if not (isinstance(x, bytes) and isinstance(y, bytes)):
            raise TypeError("both inputs should be instances of bytes")
        if len(x) != len(y):
            return False
        result = 0
        for a, b in zip(x, y):
            result |= ord(a) ^ ord(b)
        return result == 0

def hmac_sign(payload, secret=None):
    if secret is None: secret = config.sso_secret
    return hmac.new(secret, payload, sha256)

def unpack_and_verify_payload(query_dict):
    # One really annoying thing about the `sso` parameter is that it
    # includes linefeeds. When included as a `next` hidden field in
    # login redirects, this can be output as a literal linefeed in the
    # HTML output, e.g. instead of:
    #
    #   <input type="hidden" name="next" value"?sso=foo%0Abar">
    #
    # It gets output as:
    #
    #   <input type="hidden" name="next" value"?sso=foo
    #   bar">
    #
    # This causes the browser to convert the linefeed into a
    # linefeed + carriage return when submitting the form.
    #
    # Ideally we'd fix this by simply having the linefeeds in the value
    # stay percent-encoded rather than being rendered as actual linefeeds,
    # but this functionality appears to be buried under layers of
    # third-party code, so instead we'll just "undo" the corruption here
    # by removing any occurrence of carriage returns.
    payload = query_dict['sso'].replace('\r', '')

    their_sig = query_dict['sig'].decode('hex')
    our_sig = hmac_sign(payload).digest()

    if not compare_digest(our_sig, their_sig):
        raise InvalidSignatureError('invalid signature')

    return dict(urlparse.parse_qsl(base64.b64decode(payload)))

def pack_and_sign_payload(payload_dict, secret=None):
    payload = base64.b64encode(urllib.urlencode(payload_dict))
    return {
        'sso': payload,
        'sig': hmac_sign(payload, secret).hexdigest()
    }

def user_info_qs(user, nonce):
    # TODO: Include avatar_url.

    return urllib.urlencode(pack_and_sign_payload({
        'nonce': nonce,
        'email': str(user.email),
        'external_id': str(user.id),
        'username': str(user.username),
        'name': user.full_name.encode('utf8')
    }))

class InvalidSignatureError(Exception):
    pass
