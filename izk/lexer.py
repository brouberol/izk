from pygments.lexer import RegexLexer, words
from pygments.token import Keyword, Text, String

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
    'raw',
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

# A single word
FOUR_LETTER_WORD = r"[a-z]{4}"


class ZkCliLexer(RegexLexer):

    tokens = {
        'root': [
            (r'/[^\s]+', Text),
            (FOUR_LETTER_WORD, Text),
            (words(KEYWORDS, suffix=r'\b'), Keyword),
        ],
    }
