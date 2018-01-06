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

# A zookeeper CLI command
COMMAND = r'(%s)' % ('|'.join(KEYWORDS))

# A znode path
PATH = r'/[^\s]*'

# A string-value, without the quotes
STR = r"((?<=')[^']+(?=')|(?<=\")[^\"]+(?=\"))"


class ZkCliLexer(RegexLexer):

    tokens = {
        'root': [
            (r'/[^\s]+', Text),
            (words(KEYWORDS, suffix=r'\b'), Keyword),
        ],
    }
