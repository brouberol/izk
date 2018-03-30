import pytest

from izk.validation import CommandValidator, UnknownCommand


@pytest.mark.parametrize('input_str, expected', [
    ('delete  bad', False),
    ('delete /test', True),
    ('edit', False),
    ('edit /test', True),
    ('get  bad ', False),
    ('get  bad/ ', False),
    ('get /test', True),
    ('help ls', True),
    ('help nope', False),
    ('help', True),
    ('ls  /test ', True),
    ('ls  /test/ ', True),
    ('ls  bad ', False),
    ('ls  bad/ ', False),
    ('ls /test ', True),
    ('ls /test', True),
    ('ls /test', True),
    ('quit nope', False),
    ('quit', True),
    ('raw', False),
    ('raw srvr', True),
    ('rmr  bad/', False),
    ('rmr /test', True),
    ('rmr /test/test2', True),
    ('set /test \'{"key": "value"}\'', True),
    ('set /test', True),
    ('set', False),
    ('stat  bad', False),
    ('stat /test', True),
])
def test_validate_pattern(input_str, expected):
    validator = CommandValidator(input_str)
    assert validator.command == input_str.split()[0]
    assert validator.validate() is expected


def test_validate_unknown_command():
    with pytest.raises(UnknownCommand):
        CommandValidator('nope')
