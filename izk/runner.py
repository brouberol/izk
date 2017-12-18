import re
import datetime

from .lexer import KEYWORDS
from .formatting import colorize

# A zookeeper CLI command
COMMAND = r'(%s)' % ('|'.join(KEYWORDS))

# A znode path
PATH = r'/[^\s]*'

# A string-value, without the quotes
STR = r"((?<=')[^']+(?=')|(?<=\")[^\"]+(?=\"))"

# A CLI user-input token can either be a command, a path or a string
TOKEN = r'(%s)' % '|'.join([COMMAND, PATH, STR])


class ZkCommandRunner:
    """Object in charge of running the zookeeper commands."""

    def __init__(self, zkcli):
        self.zkcli = zkcli

    def _tokenize(self, command_str):
        tokens = re.findall(TOKEN, command_str)
        return [tok[0] for tok in tokens]

    def ls(self, path):
        nodes = self.zkcli.get_children(path)
        return ' '.join(nodes)

    @colorize
    def get(self, path):
        node_data = self.zkcli.get_node(path)
        if node_data is None:
            raise Exception('%s does not exist' % (path))
        else:
            return node_data

    def set(self, path, data):
        if not self.zkcli.exists(path):
            return self.zkcli.create(path, data.encode('utf-8'))
        else:
            self.zkcli.set(path, data.encode('utf-8'))

    def delete(self, path):
        self.zkcli.delete(path)

    def stat(self, path):
        def dtfmt(ts):
            return datetime.datetime.fromtimestamp(ts / 1000).strftime(
                "%a %b %d %H:%M:%S UTC %Y")
        stat = self.zkcli.stat(path)
        lines = [
            'cZxid = {0:x}'.format(stat.czxid),
            'ctime = {}'.format(dtfmt(stat.ctime)),
            'mZxid = {0:x}'.format(stat.mzxid),
            'mtime = {}'.format(dtfmt(stat.mtime)),
            'pZxid = {0:x}'.format(stat.pzxid),
            'cversion = {}'.format(stat.cversion),
            'dataVersion = {}'.format(stat.version),
            'aclVersion = {}'.format(stat.aversion),
            'ephemeralOwner = {0:x}'.format(stat.ephemeralOwner),
            'dataLength = {}'.format(stat.dataLength),
            'numChildren = {}'.format(stat.numChildren),
        ]
        return '\n'.join(lines)

    def run(self, command_str):
        if command_str:
            tokens = self._tokenize(command_str)
            command, args = tokens[0], tokens[1:]
            out = getattr(self, command)(*args)
            return out
