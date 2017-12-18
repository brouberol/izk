import json
import collections

from pygments import highlight, lexers, formatters
from pygments.styles.monokai import MonokaiStyle


def colorize(f):
    def wrapper(*args, **kwargs):
        """Pretty-print container types and syntax-highlight command results."""
        out = f(*args, **kwargs)
        printable = repr(out)
        lexer = lexers.PythonLexer()
        try:
            serialized = json.loads(out)
        except ValueError:
            pass
        else:
            if isinstance(serialized, collections.abc.Container):
                printable = json.dumps(serialized, indent=2)
                lexer = lexers.JsonLexer()
        printable = highlight(
            printable,
            lexer,
            formatters.Terminal256Formatter(style=MonokaiStyle))
        return printable
    return wrapper
