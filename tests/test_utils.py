import pytest

from izk.utils import bool_from_str


@pytest.mark.parametrize('s, expected', [
    ('1', True),
    ('yes', True),
    ('YES', True),
    ('true', True),
    ('True', True),
    ('0', False),
    ('whatever', False)
])
def test_bool_from_str(s, expected):
    assert bool_from_str(s) == expected
