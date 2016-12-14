from decimal import Decimal
import itertools

import pytest
from structlog_pretty.processors import NumericRounder as uut


@pytest.mark.parametrize(['param', 'expected'], [
    (0.0, 0.0),
    (1.0, 1.0),
    (1.12345, 1.123),
    (1.2345, 1.234),
    (-1.12345, -1.123),
    (-1.2345, -1.234),
    (Decimal('1.12345'), Decimal('1.123')),
    (Decimal('-1.12345'), Decimal('-1.123')),
    (None, None),
    ('str', 'str'),
    (True, True),
    (False, False),
])
def test_run(param, expected):
    processor = uut()
    event_dict = processor(None, None, {'param': param})
    assert type(event_dict['param']) == type(expected)  # pylint: disable=unidiomatic-typecheck
    assert event_dict == {'param': expected}


@pytest.mark.parametrize(['digits', 'param', 'expected'], [
    (0, 0.0, 0.0),
    (10, 0.0, 0.0),
    (0, 1.12345, 1.0),
    (1, 1.12345, 1.1),
    (10, 1.12345, 1.12345),
    (0, -1.12345, -1.0),
    (1, -1.12345, -1.1),
    (10, -1.12345, -1.12345),
    (0, Decimal('1.12345'), Decimal('1.0')),
    (1, Decimal('1.12345'), Decimal('1.1')),
    (10, Decimal('1.12345'), Decimal('1.12345')),
    (0, Decimal('-1.12345'), Decimal('-1.0')),
    (1, Decimal('-1.12345'), Decimal('-1.1')),
    (10, Decimal('-1.12345'), Decimal('-1.12345')),
    (0, 'str', 'str'),
    (1, 'str', 'str'),
    (10, 'str', 'str'),
])
def test_digits_setting(digits, param, expected):
    processor = uut(digits=digits)
    event_dict = processor(None, None, {'param': param})
    assert event_dict == {'param': expected}


@pytest.mark.parametrize(['only_fields'], [
    [only_fields]
    for i in range(4)
    for only_fields in itertools.combinations(['float', 'decimal', 'str'], i)
])
def test_only_fields_setting(only_fields):
    unrounded = {'float': 1.12345, 'decimal': Decimal('1.12345'), 'str': 'str'}
    rounded = {'float': 1.123, 'decimal': Decimal('1.123'), 'str': 'str'}
    processor = uut(only_fields=only_fields)
    event_dict = processor(None, None, unrounded)
    for field in unrounded:
        should_be_rounded = field in only_fields
        assert event_dict[field] == rounded[field] if should_be_rounded else unrounded[field]
