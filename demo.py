from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory, FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict
from pygments.lexer import RegexLexer, words
from pygments.token import Keyword

COMMANDS = ('get', 'set', 'exit', 'ls')


class CustomCompleter(Completer):

    def __init__(self, tokens):
        self.tokens = tokens
        self.first_token_completed = False

    def get_completions(self, document, event):
        current_word = document.get_word_before_cursor(WORD=True)
        if not self.first_token_completed and current_word:
            tokens = [tok for tok in self.tokens if tok.startswith(current_word[0])]
            for token in tokens:
                yield Completion(token, -len(current_word))
            self.first_token_completed = True


class MyLexer(RegexLexer):
    tokens = {
        'root': [
            (words(COMMANDS), Keyword),
        ]

    }


def get_bottom_toolbar_tokens(cli):
    global cmd_index
    return [(Token.Toolbar, '[%d]' % (cmd_index))]


style = style_from_dict({
    Token.Toolbar: '#ffffff bg:#ff0000',
    Keyword: '#ff00ff'
})


history = InMemoryHistory()
file_history = FileHistory('.demohist')
auto_suggest = AutoSuggestFromHistory()
completer = WordCompleter(COMMANDS)
lexer = MyLexer
cmd_index = 0

while True:
    try:
        completer = CustomCompleter(COMMANDS)
        cmd = prompt(
            '> ',
            history=file_history,
            auto_suggest=auto_suggest,
            completer=completer,
            vi_mode=True,
            style=style,
            get_bottom_toolbar_tokens=get_bottom_toolbar_tokens,
            lexer=lexer)
        print(cmd)
        cmd_index += 1
    except (KeyboardInterrupt, EOFError):
        print('Byye')
        exit(0)
