from __future__ import absolute_import, print_function

from pathlib import Path
import re
import sys
import json

try:
    import orjson

    fast_json_available = True
except ImportError:
    fast_json_available = False

from typing import Optional
from xml.dom.minidom import parseString as parse_xml_string

try:
    from lxml import etree

    fast_xml_available = True
except ImportError:
    fast_xml_available = False

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter

from . import utils


class NumericRounder(object):
    """A processor for rounding numbers in the event values

    For instance, ``1.162537216`` will be changed to ``1.163``.
    """

    def __init__(self, digits=3, only_fields=None):
        """Create a processor that rounds numbers in the event values

        :param digits: The number of digits to round to
        :param only_fields: An iterable specifying the fields to round
        """
        self.digits = digits
        try:
            self.only_fields = set(only_fields)
        except TypeError:
            self.only_fields = None

    def __call__(self, _, __, event_dict):
        for key, value in event_dict.items():
            if self.only_fields is not None and key not in self.only_fields:
                continue
            if isinstance(value, bool):
                continue  # don't convert True to 1.0

            try:
                event_dict[key] = round(value, self.digits)
            except TypeError:
                continue

        return event_dict


class JSONPrettifier(object):
    """A processor for prettifying JSON strings

    For instance, ``{"numbers":[1,2]}`` will be changed to this::

        {
          "numbers": [
            1,
            2
          ]
        }
    """

    def __init__(self, json_fields):
        """Create a processor that prettifies JSON strings in the event values

        :param json_fields: An iterable specifying the fields to prettify
        """
        self.fields = json_fields
        self.prettify = (
            self.fast_prettify if fast_json_available else self.slow_prettify
        )

    @staticmethod
    def slow_prettify(code):
        return json.dumps(json.loads(code), indent=2)

    @staticmethod
    def fast_prettify(code):
        return orjson.dumps(orjson.loads(code), option=orjson.OPT_INDENT_2).decode()

    def __call__(self, _, __, event_dict):
        for field in self.fields:
            try:
                code = event_dict[field]
            except KeyError:
                continue
            if not code:
                continue
            event_dict[field] = self.prettify(code)

        return event_dict


class XMLPrettifier(object):
    """A processor for prettifying XML strings

    For instance, ``<body><elem/><elem /></body>`` will be changed to this::

        <body>
          <elem/>
          <elem/>
        </body>
    """

    def __init__(self, xml_fields):
        """Create a processor that prettifies XML strings in the event values

        :param xml_fields: An iterable specifying the fields to prettify
        """
        self.fields = xml_fields
        if fast_xml_available:
            self.prettify = self.fast_prettify
            self.lxml_parser = etree.XMLParser(remove_blank_text=True)
        else:
            self.prettify = self.slow_prettify
            self.lxml_parser = None

    @staticmethod
    def slow_prettify(code):
        xml = parse_xml_string(code)
        utils.strip_minidom_whitespace(xml)
        xml.normalize()
        result = xml.toprettyxml(indent="  ")
        result = result.replace('<?xml version="1.0" ?>\n', "")
        return result.strip()

    def fast_prettify(self, code):
        result = etree.tostring(
            etree.fromstring(code.encode(), parser=self.lxml_parser), pretty_print=True
        )
        return result.strip().decode()

    def __call__(self, _, __, event_dict):
        for field in self.fields:
            try:
                code = event_dict[field]
            except KeyError:
                continue
            if not code:
                continue
            event_dict[field] = self.prettify(code)

        return event_dict


class SyntaxHighlighter(object):
    """A processor for syntax highlighting code"""

    def __init__(self, field_map):
        """Create a processor that syntax highlights code in the event values

        The syntax highlighting will use with ANSI terminal color codes.

        :param field_map: A mapping with field names mapped to languages, e.g.
                          ``{'body': 'json': 'soap_response': 'xml'}``
        """
        self.lexers = {
            field: get_lexer_by_name(language) for field, language in field_map.items()
        }

    def __call__(self, _, __, event_dict):
        for field, lexer in self.lexers.items():
            try:
                code = event_dict[field]
            except KeyError:
                continue

            if not code:
                continue

            trailing_whitespace_match = re.search(r"\s*$", code)
            trailing_whitespace = (
                trailing_whitespace_match.group(0) if trailing_whitespace_match else ""
            )

            event_dict[field] = (
                highlight(code, lexer, TerminalFormatter()).rstrip()
                + trailing_whitespace
            )

        return event_dict


class MultilinePrinter(object):
    """A processor for printing multiline strings"""

    def __init__(self, fields, target=sys.stdout):
        """Create a processor that prints the requested fields' values

        This is useful for strings with newlines in them. Keep in mind that the
        fields will be popped from the event dictionary, so they will not be
        visible to anything (other processors and the logger itself) after this
        processor has printed them.

        :param fields: An iterable specifying the fields to print
        :param target: A file-like object to print to
        """
        self.fields = fields
        self.target = target

    def __call__(self, _, __, event_dict):
        for field in self.fields:
            try:
                print(event_dict.pop(field), file=self.target, end="")
            except KeyError:
                continue

        return event_dict


class PathPrettifier:
    """A processor for printing paths.

    Changes all pathlib.Path objects.

    1. Remove PosixPath(...) wrapper by calling str() on the path.
    2. If path is relative to current working directory,
       print it relative to working directory.

    Note that working directory is determined when configuring structlog.
    """

    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = base_dir or Path.cwd()

    def __call__(self, _, __, event_dict):
        for key, path in event_dict.items():
            if not isinstance(path, Path):
                continue
            path = event_dict[key]
            try:
                path = path.relative_to(self.base_dir)
            except ValueError:
                pass  # path is not relative to cwd
            event_dict[key] = str(path)

        return event_dict
