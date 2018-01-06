from pygments.lexer import RegexLexer, words
from pygments.token import Keyword, Text

KEYWORDS = [
    # 'addauth',
    # 'close',
    # 'connect',
    'create',
    'delete',
    # 'delquota',
    'get',
    # 'getAcl',
    'help',
    # 'history',
    # 'listquota',
    'ls',
    # 'ls2',
    # 'printwatches',
    'quit',
    # 'redo',
    'rmr',
    'set',
    # 'setAcl',
    # 'setquota',
    'stat',
    # 'sync',
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
