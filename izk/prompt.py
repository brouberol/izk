import argparse
import traceback

from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
from pygments.styles.monokai import MonokaiStyle

from .runner import ZKCommandRunner
from .lexer import ZkCliLexer, KEYWORDS
from .zk import ExtendedKazooClient
from .completion import ZkCompleter


history = InMemoryHistory()
auto_suggest = AutoSuggestFromHistory()
completer = WordCompleter(KEYWORDS)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('zk_url')
    return parser.parse_args()


def main():
    i = 0
    args = parse_args()
    with ExtendedKazooClient(hosts=args.zk_url, timeout=2) as zkcli:
        cmdrunner = ZKCommandRunner(zkcli)
        while True:
            # We need a new completer for each command
            completer = ZkCompleter(zkcli)
            try:
                cmd = prompt(
                    '(%d) > ' % (i),
                    history=history,
                    auto_suggest=auto_suggest,
                    completer=completer,
                    lexer=ZkCliLexer,
                    style=MonokaiStyle)
                try:
                    out = cmdrunner.run(cmd)
                except Exception as exc:
                    print(exc)
                else:
                    if out is not None:
                        print(out)
            except (KeyboardInterrupt, EOFError) as exc:
                break
            except Exception:
                traceback.print_exc()
            finally:
                i += 1


if __name__ == '__main__':
    main()
