import json
import functools
import shutil

import colored
from pygments import highlight, lexers, formatters
from pygments import styles


STYLE_NAMES = list(styles.get_all_styles())
PARENT_ZNODE_STYLE = angry = colored.fg("blue") + colored.attr("bold")


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def columnize(items, nb_columns):
    """Format the argument items in columns, using the current terminal width"""
    items_lines = chunks(items, nb_columns)
    term_width, _ = shutil.get_terminal_size()
    col_width = int(term_width / nb_columns)
    lines = '\n'.join([
        "".join(item.ljust(col_width) for item in item_line)
        for item_line in items_lines
    ])
    return lines


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
