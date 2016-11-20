import io

import pytest
from structlog_pretty.processors import MultilinePrinter as uut

cases = ['', 'foo', 'foo\n', 'foo\n\n\n', 'foo\nbar']


@pytest.mark.parametrize(['param'], [[case] for case in cases])
def test_run(param):
    buffer = io.StringIO()
    processor = uut(fields=['param'], target=buffer)
    event_dict = processor(None, None, {'param': param})
    assert buffer.getvalue() == param
    assert event_dict == {}


@pytest.mark.parametrize(['param'], [[case] for case in cases])
def test_fields_setting(param):
    buffer = io.StringIO()
    processor = uut(fields=['not_the_param'], target=buffer)
    event_dict = processor(None, None, {'param': param})
    assert buffer.getvalue() == ''
    assert event_dict == {'param': param}
