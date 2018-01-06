import pytest

from izk.validation import CommandValidator, UnknownCommand


@pytest.mark.parametrize('input_str, expected', [
    ('ls /test', True),
    ('ls /test', True),
    ('ls /test ', True),
    ('ls  /test ', True),
    ('ls  /test/ ', True),
    ('ls  bad ', False),
    ('ls  bad/ ', False),
    ('get /test', True),
    ('get  bad ', False),
    ('get  bad/ ', False),
    ('stat /test', True),
    ('stat  bad', False),
    ('delete /test', True),
    ('delete  bad', False),
    ('rmr /test', True),
    ('rmr /test/test2', True),
    ('rmr  bad/', False),
    ('set /test \'{"key": "value"}\'', True),
    ('help', True),
    ('help ls', True),
    ('help nope', False),
    ('quit', True),
    ('quit nope', False),

])
def test_validate_pattern(input_str, expected):
    validator = CommandValidator(input_str)
    assert validator.command == input_str.split()[0]
    assert validator.validate() is expected


def test_validate_unknown_command():
    with pytest.raises(UnknownCommand):
        CommandValidator('nope')
