import pytest
import imp
import functools

import izk.runner


def mock_colorize_func(f):
    @functools.wraps(f)
    def mock_wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return mock_wrapper


@pytest.fixture(autouse=True)
def mock_colorize(monkeypatch):
    """Deactivate the colorize decorator by replacing it with a dummy.

    We need to relaod the izk.runner module, as decorators are applied
    at import time, and mocking would have no effect without a reload.

    """
    monkeypatch.setattr("izk.formatting.colorize", mock_colorize_func)
    imp.reload(izk.runner)
