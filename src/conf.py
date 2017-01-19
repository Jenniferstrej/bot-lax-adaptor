import os, json, logging
from os.path import join
from pythonjsonlogger import jsonlogger

ROOTLOG = logging.getLogger("")

_supported_keys = [
    'asctime', # formatted 'created' date in ymdhms format
    'created', # unixtime, can't hurt
    #'filename', # disabled in preference to 'pathname'
    'funcName', # combined with 'lineno' and 'pathname', we can unambiguously know origin
    'levelname',
    #'levelno', # numeric version of 'levelname'
    'lineno',
    #'module', # essentially duplicates 'pathname'
    #'msecs', # millisecond component
    'message',
    #'name', # logger name, probably duplicates 'filename'
    'pathname',
    #'process',
    #'processName',
    #'relativeCreated',
    #'thread',
    #'threadName'
]
# optional json logging if you need it
_log_format = ['%({0:s})'.format(i) for i in _supported_keys]
_log_format = ' '.join(_log_format)
_formatter = jsonlogger.JsonFormatter(_log_format)

# output to stderr
_handler = logging.StreamHandler()
_handler.setLevel(logging.INFO)
_handler.setFormatter(logging.Formatter('%(levelname)s - %(asctime)s - %(message)s'))

ROOTLOG.addHandler(_handler)
ROOTLOG.setLevel(logging.DEBUG)

def multiprocess_log(filename, name=__name__):
    """Creates a shared log for name and the current process, writing to filename
    with the append flag.

    On Linux this should ensure that no log entries are lost, thanks to kernel-specific behavior"""
    log = logging.getLogger("%s.%d" % (__name__, os.getpid()))
    if not log.handlers:
        _handler = logging.FileHandler(filename)
        _handler.setLevel(logging.INFO)
        _handler.setFormatter(logging.Formatter('%(levelname)s - %(asctime)s - %(message)s'))
        log.addHandler(_handler)
    return log

DEBUG = False
PATHS_TO_LAX = map(os.path.expanduser, [
    '/srv/lax/',
    '~/dev/python/lax/'
])

SEND_LAX_PATCHED_AJSON = True

PROJECT_DIR = os.getcwdu() # ll: /path/to/adaptor/
INGEST, PUBLISH, INGEST_PUBLISH = 'ingest', 'publish', 'ingest+publish'
INGESTED, PUBLISHED, INVALID, ERROR = 'ingested', 'published', 'invalid', 'error'

XML_DIR = join(PROJECT_DIR, 'article-xml', 'articles')
JSON_DIR = join(PROJECT_DIR, 'article-json')
VALID_JSON_DIR = join(JSON_DIR, 'valid')
INVALID_JSON_DIR = join(JSON_DIR, 'invalid')
VALID_PATCHED_JSON_DIR = join(JSON_DIR, 'patched') # only valid json is output to the patched dir

def json_load(path):
    path = join(PROJECT_DIR, 'schema', path)
    return json.load(open(path, 'r'))

POA_SCHEMA = json_load('api-raml/dist/model/article-poa.v1.json')
VOR_SCHEMA = json_load('api-raml/dist/model/article-vor.v1.json')

REQUEST_SCHEMA = json_load('request-schema.json')
RESPONSE_SCHEMA = json_load('response-schema.json')

CDN1 = 'cdn.elifesciences.org/articles/%(padded-msid)s/%(fname)s'
CDN2 = 'publishing-cdn.elifesciences.org/%(padded-msid)s/%(fname)s'

DEFAULT_CDN = CDN1 if False else CDN2
CDNS_BY_ENV = {
    'end2end': 'end2end-' + CDN2,
}

def cdn(env=None):
    return 'https://' + CDNS_BY_ENV.get(env, DEFAULT_CDN)

GLENCOE_CACHE = '/tmp/glencoe-cache'

KITCHEN_SINK_MSID = 666

XML_REV = open(join(PROJECT_DIR, 'elife-article-xml.sha1'), 'r').read()

JOURNAL_INCEPTION = 2012 # used to calculate volumes
