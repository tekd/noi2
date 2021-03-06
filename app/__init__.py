'''
NoI __init__

Creates globals
'''

from flask_alchemydumps import AlchemyDumps
from flask_assets import Bundle, Environment
from flask_security import Security
from flask_cache import Cache
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_s3 import FlaskS3
from flask_wtf.csrf import CsrfProtect
from flask_oauthlib.client import OAuth

from babel import Locale, UnknownLocaleError
import locale

from .questionnaires import Questionnaires

s3 = FlaskS3()
mail = Mail()
alchemydumps = AlchemyDumps()
security = Security()
csrf = CsrfProtect()
babel = Babel()
bcrypt = Bcrypt()
oauth = OAuth()

assets = Environment()

main_css = Bundle('css/vendor/bootstrap.css',
                  output='gen/main_packed.%(version)s.css')
assets.register('main_css', main_css)

main_js = Bundle('js/main.js',
                 'js/pingdom-rum.js',
                 'js/google-analytics.js',
                 'js/tutorial.js',
                 'vendor/bootstrap/js/alert.js',
                 'vendor/bootstrap/js/modal.js',
                 'vendor/bootstrap/js/tab.js',
                 #filters='jsmin',
                 output='gen/main_packed.%(version)s.js')
assets.register('main_js', main_js)

cache = Cache()

LEVELS = {'LEVEL_I_CAN_EXPLAIN': {'score': 2,
                                  'class': 'm-explain',
                                  'label': 'I can explain it'},
          'LEVEL_I_CAN_DO_IT': {'score': 5,
                                'class': 'm-do',
                                'label': 'I can do it'},
          'LEVEL_I_CAN_REFER': {'score': 1,
                                'class': 'm-connect',
                                'label': 'I can connect others'},
          'LEVEL_I_WANT_TO_LEARN': {'score': -1,
                                    'class': 'm-learn',
                                    'label': 'I want to learn'}}

VALID_SKILL_LEVELS = [v['score'] for k, v in LEVELS.iteritems()]
LEVELS_BY_SCORE = {}

for v in LEVELS.values():
    LEVELS_BY_SCORE[v['score']] = v

NOI_COLORS = '#D44330,#D6DB63,#BFD19F,#83C8E7,#634662,yellow,gray,#a3abd1'.split(',')

LOCALES = []
_LOCALE_CODES = set()
for l in locale.locale_alias.keys():
    if len(l) == 2 and l not in _LOCALE_CODES:
        _LOCALE_CODES.add(l)
for l in sorted(_LOCALE_CODES):
    try:
        LOCALES.append(Locale(l))
    except UnknownLocaleError:
        pass

ORG_TYPES = {'edu': 'Academia',
             'com': 'Private Sector',
             'org': 'Non Profit',
             'gov': 'Government',
             'other': 'Other'}

# Process YAML files
MIN_QUESTIONS_TO_JOIN = 3

QUESTIONNAIRES = Questionnaires()
QUESTIONNAIRES_BY_ID = QUESTIONNAIRES.by_id
QUESTIONS_BY_ID = QUESTIONNAIRES.questions_by_id
