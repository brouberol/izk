import re
import datetime
import functools

import colored
from kazoo.exceptions import NoNodeError, NotEmptyError

from .lexer import COMMAND, PATH, QUOTED_STR, KEYWORDS, FOUR_LETTER_WORD
from .formatting import colorize, columnize, PARENT_ZNODE_STYLE
from .validation import validate_command_input, ask_for_confirmation

# A CLI user-input token can either be a command, a path or a string
TOKEN = r'(%s)' % '|'.join([COMMAND, PATH, QUOTED_STR, FOUR_LETTER_WORD])
NODES_PER_LINE = 3


class UnauthorizedWrite(Exception):
    """Exception raised when a write operation is triggered in RO mode."""


def command_usage(command_name):
    """Print the usage of the argument command."""
    doc = getattr(ZkCommandRunner, command_name).__doc__
    lines = doc.split('\n')[1:]  # remove first line
    lines = [line.strip() for line in lines]
    return '\n'.join(lines).strip()


def command_help(command_name, short=False):
    """Display the help (short or not) of the argument command."""
    command = getattr(ZkCommandRunner, command_name, None)
    if not command:
        return ''
    doc = command.__doc__
    if not doc:
        return ''
    lines = doc.split('\n')
    lines = [line.strip() for line in lines]
    if short:
        lines = [lines[0]]
    return '\n'.join(lines).strip()


def commands_help():
    """Display the short help of all available commands."""
    _help = ['Commands:']
    for command_name in KEYWORDS:
        command_short_help = command_help(command_name, short=True)
        _help.append('- %s: %s' % (command_name, command_short_help))
    return '\n'.join(_help)


def write_op(f):
    """Raise an UnauthorizedWrite exception if the client is in read-only mode."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        runner, *_ = args
        if runner.zkcli.read_only:
            raise UnauthorizedWrite('Un-authorized write operation in read-only mode')
        return f(*args, **kwargs)
    return wrapper


class ZkCommandRunner:
    """Object in charge of running the zookeeper commands."""

    def __init__(self, zkcli):
        self.zkcli = zkcli

    def _tokenize(self, command_str):
        tokens = re.findall(TOKEN, command_str)
        return [tok[0].strip() for tok in tokens]

    def close(self):
        """Close the shell"""
        raise KeyboardInterrupt

    def quit(self):
        """Close the shell"""
        raise KeyboardInterrupt

    def help(self, command_name=None):
        """Print the help of a command

        Usage: help [command]
        Examples:
        - help     # shows the list of commands
        - help ls  # shows a command help

        """
        if command_name:
            return command_help(command_name)
        else:
            return commands_help()

    def ls(self, path):
        """Display the children of a ZNode

        Usage: ls <path>
        Example: ls /test

        """
        try:
            nodes = self.zkcli.get_children(path)
        except NoNodeError as exc:
            raise NoNodeError('%s does not exist' % (path))

        nodes = sorted(nodes)
        fmt_nodes = []
        for node in nodes:
            if self.zkcli.get_children('/'.join((path, node))):
                node = colored.stylize(node, PARENT_ZNODE_STYLE)
            fmt_nodes.append(node)

        nodes = columnize(fmt_nodes, NODES_PER_LINE)
        return nodes

    @colorize
    def get(self, path):
        """Display the content of a ZNode

        Usage: get <path>
        Example: get /test

        """
        try:
            node_data, _ = self.zkcli.get(path)
        except NoNodeError:
            raise NoNodeError('%s does not exist' % (path))
        else:
            if node_data is not None:
                node_data = node_data.decode('utf-8')
                return node_data

    @write_op
    def create(self, path):
        """Recursively create a path if it doesn't exist

        Usage: create <path>
        Example: create /a/b/c/d

        """
        return self.zkcli.ensure_path(path)

    @write_op
    def set(self, path, data):
        """Set or update the content of a ZNode

        Usage: set <path> <data>
        Example: set /test '{"key": "value"}'

        """
        data = data.strip("'").strip('"')
        if not self.zkcli.exists(path):
            return self.zkcli.create(path, data.encode('utf-8'))
        else:
            self.zkcli.set(path, data.encode('utf-8'))

    @write_op
    def delete(self, path):
        """Delete a leaf ZNode

        Usage: delete <path>
        Example: delete /test/node

        """
        if ask_for_confirmation("You're about to delete %s. Proceed?" % (path)):
            try:
                self.zkcli.delete(path)
            except NotEmptyError:
                msg = (
                    'Cannot delete %s as it still contains nodes. '
                    'Use the `rmr` command if you really want to proceed.') % (path)
                raise NotEmptyError(msg)
            except NoNodeError:
                raise NoNodeError('%s does not exist' % (path))

    @write_op
    def rmr(self, path):
        """Recursively delete all children ZNodes, along with argument node.

        Usage: rmr <path>
        Example: rmr /test

        """
        if ask_for_confirmation("You're about to recursively delete %s. Proceed?" % (path)):
            self.zkcli.delete(path, recursive=True)

    def stat(self, path):
        """Display a ZNode's metadata

        Usage: stat <path>
        Example: stat /test

        """
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

    def raw(self, _4lcmd):
        """Send the 4-letter-word command to the zookeeper server

        Usage: raw <4-letter-word>
        Example: raw srvr

        """
        _4lcmd = _4lcmd.encode('utf-8')
        return self.zkcli.command(_4lcmd)

    @validate_command_input
    def run(self, command_str):
        if command_str:
            tokens = self._tokenize(command_str)
            command, args = tokens[0].strip(), tokens[1:]
            out = getattr(self, command)(*args)
            return out
