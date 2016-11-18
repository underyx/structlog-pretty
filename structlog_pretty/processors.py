from __future__ import absolute_import, print_function

import sys

import json
try:
    import rapidjson
    fast_json_available = True
except ImportError:
    fast_json_available = False

from xml.dom.minidom import parseString as parse_xml_string
try:
    from lxml import etree
    fast_xml_available = True
except ImportError:
    fast_xml_available = False

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import TerminalFormatter


class NumericRounder(object):

    def __init__(self, digits=3, only_fields=None):
        self.digits = digits
        try:
            self.only_fields = set(only_fields)
        except TypeError:
            self.only_fields = None

    def __call__(self, _, __, event_dict):
        for key, value in event_dict.items():
            if self.only_fields is None or key in self.only_fields:
                try:
                    event_dict[key] = round(value, self.digits)
                except TypeError:
                    continue

        return event_dict


class JSONPrettifier(object):

    def __init__(self, json_fields):
        self.fields = json_fields
        self.prettify = self.fast_prettify if fast_json_available else self.slow_prettify

    @staticmethod
    def slow_prettify(code):
        return json.dumps(json.loads(code), indent=2)

    @staticmethod
    def fast_prettify(code):
        return rapidjson.dumps(rapidjson.loads(code), indent=2)

    def __call__(self, _, __, event_dict):
        for field in self.fields:
            try:
                code = event_dict[field]
            except KeyError:
                continue
            event_dict[field] = self.prettify(code)

        return event_dict


class XMLPrettifier(object):

    def __init__(self, xml_fields):
        self.fields = xml_fields
        self.prettify = self.fast_prettify if fast_xml_available else self.slow_prettify

    @staticmethod
    def slow_prettify(code):
        result = parse_xml_string(code).toprettyxml(indent='  ')
        result = result.replace('<?xml version="1.0" ?>\n', '')
        return result.strip()

    @staticmethod
    def fast_prettify(code):
        result = etree.tostring(etree.fromstring(code), pretty_print=True)
        return result.strip().decode()

    def __call__(self, _, __, event_dict):
        for field in self.fields:
            try:
                code = event_dict[field]
            except KeyError:
                continue
            event_dict[field] = self.prettify(code)

        return event_dict


class SyntaxHighlighter(object):

    def __init__(self, field_map):
        self.lexers = {
            field: get_lexer_by_name(language)
            for field, language in field_map.items()
        }

    def __call__(self, _, __, event_dict):
        for field, lexer in self.lexers.items():
            try:
                code = event_dict[field]
            except KeyError:
                continue
            event_dict[field] = highlight(code, lexer, TerminalFormatter())


        return event_dict


class MultilinePrinter(object):

    def __init__(self, fields, target=sys.stdout):
        self.fields = fields
        self.target = target

    def __call__(self, _, __, event_dict):
        for field in self.fields:
            try:
                print(event_dict.pop(field), file=self.target)
            except KeyError:
                continue

        return event_dict
