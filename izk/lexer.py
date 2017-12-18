from pygments.lexer import RegexLexer, words
from pygments.token import Keyword, Text

KEYWORDS = [
    'connect',
    'get',
    'ls',
    'set',
    'rmr',
    'delquota',
    'quit',
    'printwatches',
    'create',
    'stat',
    'close',
    'ls2',
    'history',
    'listquota',
    'setAcl',
    'getAcl',
    'sync',
    'redo',
    'addauth',
    'delete',
    'setquota',
]


class ZkCliLexer(RegexLexer):

    tokens = {
        'root': [
            (r'/[^\s]+', Text),
            (words(KEYWORDS, suffix=r'\b'), Keyword),
        ],
    }
