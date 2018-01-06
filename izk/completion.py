import kazoo

from prompt_toolkit.completion import Completer, Completion

from .lexer import KEYWORDS


class ZkCompleter(Completer):

    def __init__(self, zkcli, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.zkcli = zkcli
        self.command = None
        self.prev_typed_word = None
        self.cache = {}

    def get_completions(self, document, complete_event):
        """The completions are either commands or paths"""
        word_before_cursor = document.get_word_before_cursor(WORD=True)

        # If command has been typed, store it
        if (
                not self.command and
                self.prev_typed_word in KEYWORDS and
                word_before_cursor == ''
        ):
            self.command = word_before_cursor

        # Find all possible completable commands
        self.prev_typed_word = word_before_cursor
        if self.command is None:
            completions = [cmd for cmd in KEYWORDS if cmd.startswith(word_before_cursor)]
            for completion in completions:
                yield Completion(completion, -len(word_before_cursor))
        else:
            # Autocomplete on the path of available znodes
            path = word_before_cursor
            if path.startswith('/'):
                current_chroot = '/'.join(path.split('/')[:-1]).rstrip('/') or '/'
                current_node = path.replace(current_chroot, '').lstrip('/')

                if current_chroot not in self.cache:
                    try:
                        self.cache[current_chroot] = self.zkcli.get_children(current_chroot)
                    except kazoo.exceptions.NoNodeError:
                        # We may be typing a nonexistent path
                        # (for example with the 'create' command)
                        self.cache[current_chroot] = []

                completions = [
                    '/%s' % (node)
                    for node in self.cache[current_chroot]
                    if node.startswith(current_node)
                ]

                for completion in completions:
                    yield Completion(completion, -(len(current_node) + 1))
