from pygments.lexer import RegexLexer, words
from pygments.token import Keyword, Text, String

KEYWORDS = [
    # 'addauth',
    # 'close',
    # 'connect',
    'create',
    'delete',
    'edit',
    'exit',
    # 'delquota',
    'get',
    # 'getAcl',
    'help',
    # 'history',
    # 'listquota',
    'ls',
    # 'ls2',
    'tree',
    'ftree',
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
ZK_FOUR_LETTER_WORDS = [
    "conf", "cons", "crst", "dump",
    "envi", "ruok", "srst", "srvr",
    "stat", "wchs", "wchc", "wchp", "mntr"
]
ZK_FOUR_LETTER_WORD = r'(%s)' % ('|'.join(ZK_FOUR_LETTER_WORDS))


class ZkCliLexer(RegexLexer):

    tokens = {
        'root': [
            (PATH, Text),
            (ZK_FOUR_LETTER_WORD, String),
            (QUOTED_STR, String),
            (words(KEYWORDS, suffix=r'\b'), Keyword),
        ],
    }
