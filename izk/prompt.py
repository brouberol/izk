import argparse
import threading

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


history = InMemoryHistory()
auto_suggest = AutoSuggestFromHistory()
g = threading.local()

DEFAULT_ZK_URL = 'localhost:2181'
DEFAULT_COLOR_STYLE = 'monokai'


def parse_args():
    parser = argparse.ArgumentParser(
        description='CLI for zookeeper with syntax-highlighting and auto-completion')
    parser.add_argument(
        'zk_url',
        nargs='?',
        help='URL of the zookeeper node. Default: %s' % (DEFAULT_ZK_URL),
        default=DEFAULT_ZK_URL)
    parser.add_argument(
        '--write',
        help='Authorize write operations (update/insert/remove)',
        action='store_true',
        default=False,
    )
    parser.add_argument(
        '--style',
        help="The color style to adopt. Default: %s" % (DEFAULT_COLOR_STYLE),
        default=DEFAULT_COLOR_STYLE,
        choices=STYLE_NAMES,
    )
    return parser.parse_args()


def print_headers(zkcli):
    print(zkcli.command(b'srvr'))


def render_prompt(step, read_only):
    mode = 'RO' if read_only else 'RW'
    return '(%s %d) > ' % (mode, step)


def main():
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
                    style=g.style)
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
                if ask_for_confirmation('Quit?'):
                    break
            except Exception:
                raise
            finally:
                cmd_index += 1


if __name__ == '__main__':
    main()
