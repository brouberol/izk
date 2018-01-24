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
    'toggle_write'
]

# A zookeeper CLI command
COMMAND = r'(%s)' % ('|'.join(KEYWORDS))

# A znode path
PATH = r'/[^\s]*'

# A string-value
QUOTED_STR = r"('[^']*'|\"[^\"]*\")"

# A single 4 letter word
FOUR_LETTER_WORD = r"\s+[a-z]{4}(\s+|$)"


class ZkCliLexer(RegexLexer):

    tokens = {
        'root': [
            (PATH, Text),
            (FOUR_LETTER_WORD, Text),
            (QUOTED_STR, String),
            (words(KEYWORDS, suffix=r'\b'), Keyword),
        ],
    }
