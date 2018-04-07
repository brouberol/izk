import argparse
import threading
import os

from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from pygments import styles
from kazoo.exceptions import NoNodeError, NotEmptyError

from .runner import ZkCommandRunner, command_usage, UnauthorizedWrite
from .lexer import ZkCliLexer
from .zk import ExtendedKazooClient
from .completion import ZkCompleter
from .validation import UnknownCommand, CommandValidationError, ask_for_confirmation
from .formatting import STYLE_NAMES
from .utils import bool_from_str
from . import __version__


history = InMemoryHistory()
auto_suggest = AutoSuggestFromHistory()
g = threading.local()

DEFAULT_ZK_URL = 'localhost:2181'
DEFAULT_COLOR_STYLE = 'monokai'
DEFAULT_INPUT_MODE = 'vi'


class EnvDefault(argparse.Action):
    """Action allowing to define a command-line argument via an environment variable.

    The environment variable must be named IZK_<flag name in uppercase>.

    Example: --write can be overriden via the IZK_WRITE environment variable.

    """
    def __init__(self, required=True, default=None, **kwargs):
        # Read value from environment variable, and apply type, if any
        envvar = 'IZK_' + kwargs['dest'].upper()
        if os.environ.get(envvar) and os.environ[envvar] != default:
            if kwargs.get('type'):
                if kwargs['type'] == bool:
                    default = bool_from_str(os.environ[envvar])
                else:
                    default = kwargs['type'](os.environ[envvar])
            else:
                default = os.environ[envvar]

        # If value was required but the envvar was given, cancel the requirement
        if required and default is not None:
            required = False

        # Update the help string with the override environment variable info
        additional_help = 'Override via the %s environment variable.' % (envvar)
        if 'help' in kwargs:
            kwargs['help'] = '%s. %s' % (kwargs['help'].rstrip('.'), additional_help)
        else:
            kwargs['help'] = additional_help
        super().__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def parse_args():
    parser = argparse.ArgumentParser(
        description="CLI for zookeeper with syntax-highlighting and auto-completion.",
        epilog="Version: %s" % (__version__))
    parser.add_argument(
        'zk_url',
        nargs='?',
        action=EnvDefault,
        help='URL of the zookeeper node. Default: %s' % (DEFAULT_ZK_URL),
        default=DEFAULT_ZK_URL)
    parser.add_argument(
        '--write',
        help='Authorize write operations (update/insert/remove)',
        action=EnvDefault,
        type=bool,
        default=False)
    parser.add_argument(
        '--style',
        help="The color style to adopt. Default: %s" % (DEFAULT_COLOR_STYLE),
        action=EnvDefault,
        default=DEFAULT_COLOR_STYLE,
        choices=STYLE_NAMES)
    parser.add_argument(
        '--input-mode',
        help="The input mode to adopt. Default: %s" % (DEFAULT_INPUT_MODE),
        action=EnvDefault,
        default=DEFAULT_INPUT_MODE,
        choices=('vi', 'emacs'))
    parser.add_argument(
        '--version',
        help="Display izk version number and exit",
        action='version',
        version=__version__)
    return parser.parse_args()


def print_headers(zkcli):
    print(zkcli.command(b'srvr'))


def render_prompt(step, read_only):
    mode = 'RO' if read_only else 'RW'
    return '(%s %d) > ' % (mode, step)


def main():  # pragma: no cover
    cmd_index = 0
    args = parse_args()
    g.style = styles.get_style_by_name(args.style)

    with ExtendedKazooClient(
        hosts=args.zk_url,
        timeout=2,
        read_only=not args.write
    ) as zkcli:
        print_headers(zkcli)
        cmdrunner = ZkCommandRunner(zkcli)
        while True:
            # We need a new completer for each command
            completer = ZkCompleter(zkcli)
            try:
                cmd = prompt(
                    render_prompt(cmd_index, zkcli.read_only),
                    history=history,
                    auto_suggest=auto_suggest,
                    completer=completer,
                    lexer=ZkCliLexer,
                    style=g.style,
                    vi_mode=args.mode == 'vi')
                try:
                    out = cmdrunner.run(cmd)
                except CommandValidationError as exc:
                    # The command was invalid. Print command help and usage.
                    print(exc, end='\n\n')
                    print(command_usage(exc.command))
                except (
                    NoNodeError, NotEmptyError, UnknownCommand, UnauthorizedWrite
                ) as exc:
                    print(exc)
                else:
                    if out is not None:
                        print(out)
            except (KeyboardInterrupt, EOFError) as exc:
                if ask_for_confirmation('Quit?', confirm_on_exc=True):
                    break
            except Exception:
                raise
            finally:
                cmd_index += 1


if __name__ == '__main__':
    main()
