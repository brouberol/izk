import json
import functools

from pygments import highlight, lexers, formatters
from pygments import styles


STYLE_NAMES = list(styles.get_all_styles())


def colorize(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        """Pretty-print container types and syntax-highlight command results."""
        from .prompt import g
        out = f(*args, **kwargs)
        if out is None:
            return
        printable = repr(out)
        lexer = lexers.PythonLexer()
        try:
            serialized = json.loads(out)
        except ValueError:
            pass
        else:
            if isinstance(serialized, (tuple, list, dict)):
                printable = json.dumps(serialized, indent=2)
                lexer = lexers.JsonLexer()
        printable = highlight(
            printable,
            lexer,
            formatters.Terminal256Formatter(style=g.style))
        return printable
    return wrapper
