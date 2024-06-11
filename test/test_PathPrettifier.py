from pathlib import Path

import pytest
from structlog_pretty.processors import PathPrettifier as uut


BASE_DIR = Path("/tmp")


@pytest.mark.parametrize(
    ["param", "expected"],
    [
        (Path("/tmp/foo.py"), "foo.py"),
        (Path("/tmp/dir/foo.py"), "dir/foo.py"),
        (Path("foo.py"), "foo.py"),
        (Path("/elsewhere/foo.py"), "/elsewhere/foo.py"),
        (1, 1),
        (None, None),
        ("/tmp/dir/foo.py", "/tmp/dir/foo.py"),
    ],
)
def test_run(param, expected):
    processor = uut(BASE_DIR)
    event_dict = processor(None, None, {"param": param})
    assert type(event_dict["param"]) == type(expected)  # pylint: disable=unidiomatic-typecheck
    assert event_dict == {"param": expected}
