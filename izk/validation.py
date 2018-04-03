import re
import functools

from .lexer import COMMAND, PATH, FOUR_LETTER_WORD, QUOTED_STR


def ask_for_confirmation(message, confirm_on_exc=False):
    try:
        message = '%s [y/n] ' % (message)
        while True:
            answer = input(message)
            if not answer:
                continue
            answer = answer.lower()[0]
            if answer == 'y':
                return True
            elif answer == 'n':
                print('Aborting')
                return False
    except (KeyboardInterrupt, EOFError):
        return confirm_on_exc


class Token(str):
    """A token in a command string"""

    def __init__(self, string):
        self.string = string

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.string)

    def __str__(self):
        return self.string

    def __add__(self, other):
        if isinstance(other, Optional):
            return '%s\s*%s' % (str(self), str(other))
        return '%s\s+%s' % (str(self), str(other))


class Optional(Token):
    """A token that can be ommitted in a command"""

    def __str__(self):
        return r'%s?' % (self.string)


class UnknownCommand(ValueError):
    """Exception raised when an unknown command was passed."""


class CommandValidationError(ValueError):
    """Exception raised when a command received invalid arguments."""

    def __init__(self, command, message):
        self.command = command
        self.message = message

    def __str__(self):
        return self.message


class CommandValidator:
    """Object in charge of validating the user input for a given command."""

    patterns = {
        'create': PATH,
        'delete': PATH,
        'edit': PATH,
        'exit': None,
        'get': PATH,
        'help': Optional(COMMAND),
        'ls': PATH,
        'quit': None,
        'raw': FOUR_LETTER_WORD,
        'rmr': PATH,
        'set': [PATH, Optional(QUOTED_STR)],
        'stat': PATH,
        'toggle_write': None,
    }

    def __init__(self, input_str):
        self.input_str = input_str
        self.command = self._parse_command_name()
        self.pattern = self.make_pattern()

    def _parse_command_name(self):
        command_pattern = r'(%s)\s*' % (COMMAND)
        m = re.match(command_pattern, self.input_str)
        if not m:
            raise UnknownCommand('Command %r not found' % (self.input_str))
        return m.group(1).strip()

    def _make_pattern(self, tokens):
        """Return a regex pattern given the input tokens"""

        # First, transform the input in a list of Tokens, including the command
        if tokens in (None, ''):
            tokens = []
        elif isinstance(tokens, str) and not isinstance(tokens, Token):
            tokens = [Token(tokens)]
        elif isinstance(tokens, list):
            tokens = [tok if isinstance(tok, Token) else Token(tok) for tok in tokens]
        else:
            tokens = [tokens]

        # the first token will be preceeded by the command
        tokens = [Token(self.command)] + tokens

        # Glue the tokens together, and rely on their __add__ method to perform the magic
        pattern = functools.reduce(Token.__add__, tokens)

        return r'^\s*%s\s*$' % (pattern)

    def make_pattern(self):
        tokens = self.patterns[self.command]
        return self._make_pattern(tokens)

    def validate(self):
        return bool(re.match(self.pattern, self.input_str))


def validate_command_input(f):
    """Validate the input command and execute it, if valid"""

    @functools.wraps(f)
    def wrapper(runner, input_str):
        if input_str.strip():
            validator = CommandValidator(input_str.strip())
            if not validator.validate():
                validation_error_msg = 'Command %r is invalid' % (input_str)
                raise CommandValidationError(validator.command, validation_error_msg)
        return f(runner, input_str)
    return wrapper
