import re
import functools

from .lexer import COMMAND, PATH, FOUR_LETTER_WORD, QUOTED_STR


def ask_for_confirmation(message):
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


class Either:
    def __init__(self, *options):
        self.options = options

    def __iter__(self):
        for option in self.options:
            yield option

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.options)


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
        'ls': PATH,
        'get': PATH,
        'stat': PATH,
        'delete': PATH,
        'create': PATH,
        'rmr': PATH,
        'set': [PATH, QUOTED_STR],
        'help': Either(None, COMMAND),
        'quit': None,
        'raw': FOUR_LETTER_WORD,
        'toggle_write': None,
    }

    def __init__(self, input_str):
        self.input_str = input_str
        self.command = self._parse_command_name()
        self.patterns = self._make_patterns()

    def _parse_command_name(self):
        command_pattern = r'(%s)\s*' % (COMMAND)
        m = re.match(command_pattern, self.input_str)
        if not m:
            raise UnknownCommand('Command %r not found' % (self.input_str))
        return m.group(1).strip()

    def _make_pattern(self, tokens):
        if tokens is None:
            tokens = []
        elif isinstance(tokens, str):
            tokens = [tokens] if tokens else []

        # the first token will be preceeded by the command
        tokens = [self.command] + tokens

        # Each token pattern must be taken in isolation, without taking any preceeding
        # \s into account
        tokens = [
            token.replace('\s+', '') if token.startswith('\s+') else token
            for token in tokens]
        pattern = r'\s+'.join(tokens)
        return r'^\s*%s\s*$' % (pattern)

    def _make_patterns(self):
        patterns = []
        tokens = self.patterns[self.command]
        if isinstance(tokens, Either):
            for token in tokens:
                patterns.append(self._make_pattern(token))
        else:
            patterns.append(self._make_pattern(tokens))
        return patterns

    def validate(self):
        for pattern in self.patterns:
            if re.match(pattern, self.input_str):
                return True
        return False


def validate_command_input(f):
    """Validate the input command and execute it, if valid"""

    @functools.wraps(f)
    def wrapper(runner, input_str):
        validator = CommandValidator(input_str)
        if not validator.validate():
            validation_error_msg = 'Command %r is invalid' % (input_str)
            raise CommandValidationError(validator.command, validation_error_msg)
        return f(runner, input_str)
    return wrapper
