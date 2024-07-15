import re
from structlog_pretty.processors import SyntaxHighlighter as uut


def test_json():
    processor = uut(field_map={"body": "json"})
    event_dict = processor(None, None, {"body": '{"ping": true}'})
    assert "\x1b[" in event_dict["body"], "should have at least one ANSI escape code"
    assert not event_dict["body"].endswith(
        "\n"
    ), "should not have trailing newline added"


def test_retain_whitespace():
    processor = uut(field_map={"body": "json"})
    event_dict = processor(None, None, {"body": '{"ping": true}\n\n'})
    match = re.search(r"\s*$", event_dict["body"])
    assert match is not None
    assert match.group() == "\n\n"


def test_missing_json():
    processor = uut(field_map={"body": "json"})
    event_dict = processor(None, None, {"not_body": '{"ping": true}'})
    assert event_dict["not_body"] == '{"ping": true}'


def test_multiple_fields():
    processor = uut(field_map={"body": "json", "body_2": "json"})
    event_dict = processor(None, None, {"body": "null", "body_2": "null"})
    assert "\x1b[" in event_dict["body"], "should have at least one ANSI escape code"
    assert "\x1b[" in event_dict["body_2"], "should have at least one ANSI escape code"


def test_multiple_languages():
    processor = uut(field_map={"body": "json", "body_2": "xml"})
    event_dict = processor(None, None, {"body": "null", "body_2": "<null/>"})
    assert "\x1b[" in event_dict["body"], "should have at least one ANSI escape code"
    assert "\x1b[" in event_dict["body_2"], "should have at least one ANSI escape code"
