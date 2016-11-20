from textwrap import dedent

import pytest
from structlog_pretty.processors import XMLPrettifier as uut

cases = [
    ('<elem/>', '<elem/>'),
    ('<elem />', '<elem/>'),
    ('<wrapper><elem/></wrapper>', dedent('''
        <wrapper>
          <elem/>
        </wrapper>
    ''').strip()),
    ('<wrapper><elem/><elem/></wrapper>', dedent('''
        <wrapper>
          <elem/>
          <elem/>
        </wrapper>
    ''').strip()),
    (
        dedent('''
            <wrapper>
               <elem/>
                <elem/>
             </wrapper>
        ''').strip(),
        dedent('''
            <wrapper>
              <elem/>
              <elem/>
            </wrapper>
        ''').strip(),
    ),
]
modes = ('slow', 'fast')


@pytest.mark.parametrize(['mode', 'param', 'expected'], [
    [mode] + list(case) for mode in modes for case in cases
])
def test_run(mode, param, expected, monkeypatch):
    monkeypatch.setattr('structlog_pretty.processors.fast_xml_available', mode == 'fast')
    processor = uut(xml_fields=['param'])
    event_dict = processor(None, None, {'param': param})
    assert event_dict == {'param': expected}


@pytest.mark.parametrize(['mode', 'param', 'expected'], [
    (mode, case[0], case[0]) for mode in modes for case in cases
])
def test_field_name_setting(mode, param, expected, monkeypatch):
    monkeypatch.setattr('structlog_pretty.processors.fast_xml_available', mode == 'fast')
    processor = uut(xml_fields=['not_the_param'])
    event_dict = processor(None, None, {'param': param})
    assert event_dict == {'param': expected}
