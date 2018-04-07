import os
import pytest

from izk.prompt import EnvDefault, render_prompt


def test_env_default():
    env_default = EnvDefault(
        required=True, default=None, help='Test command line flag',
        dest='test', option_strings='')
    assert env_default.default is None
    assert env_default.help == (
        'Test command line flag. Override via the IZK_TEST environment variable.')
    assert env_default.required is True


def test_env_default_with_env(monkeypatch):
    monkeypatch.setitem(os.environ, 'IZK_TEST', 'test_value')
    env_default = EnvDefault(
        required=True, default=None, help='Test command line flag',
        dest='test', option_strings='')
    assert env_default.default == 'test_value'
    assert env_default.help == (
        'Test command line flag. Override via the IZK_TEST environment variable.')
    assert env_default.required is False


def test_env_default_no_help():
    env_default = EnvDefault(
        required=True, default=None,
        dest='test', option_strings='')
    assert env_default.help == (
        'Override via the IZK_TEST environment variable.')


def test_env_default_bool_type(monkeypatch):
    monkeypatch.setitem(os.environ, 'IZK_TEST', 'yes')
    env_default = EnvDefault(
        required=True, default=None, help='Test command line flag',
        dest='test', type=bool, option_strings='')
    assert env_default.default is True


def test_env_default_int_type(monkeypatch):
    monkeypatch.setitem(os.environ, 'IZK_TEST', '1')
    env_default = EnvDefault(
        required=True, default=None, help='Test command line flag',
        dest='test', type=int, option_strings='')
    assert env_default.default == 1


@pytest.mark.parametrize('step, read_only, expected', [
    (0, True, '(RO 0) > '),
    (0, False, '(RW 0) > ')
])
def test_render_prompt(step, read_only, expected):
    assert render_prompt(step, read_only) == expected
