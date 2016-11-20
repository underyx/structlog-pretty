structlog-pretty
================

.. image:: https://circleci.com/gh/underyx/structlog-pretty.svg?style=shield
   :target: https://circleci.com/gh/underyx/structlog-pretty
   :alt: CI Status

.. image:: https://codecov.io/gh/underyx/structlog-pretty/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/underyx/structlog-pretty
   :alt: Code Coverage

A collection of structlog_ processors for prettier output: a code syntax
highlighter, JSON and XML prettifiers, a multiline string printer, and
a numeric value rounder.

Installation
------------

First of all, sorry, grandma, but ``structlog-pretty`` requires Python 3.

You can just install the library with pip::

    pip install structlog-pretty

or, if you want faster prettifying processors::

    pip install structlog-pretty[fast]

The downside of the faster processors is that they will build C extensions and
they need ``libxml`` to be installed.

Usage
-----

Add structlog-pretty processors to your structlog configuration

.. code-block:: python

    import structlog
    import structlog_pretty

    structlog.configure(
        # ...
        processors=[
            structlog.stdlib.add_log_level,
            structlog_pretty.NumericRounder(digits=2, only_fields=['timing'])
            structlog.processors.JSONRenderer(),
        ],
    )

A nice example of a processor pipeline for the *prettiest* logs could be

.. code-block:: python

    processors=[
        # ...
        structlog_pretty.JSONPrettifier(['request', 'response']),
        structlog_pretty.XMLPrettifier(['soap_response']),
        structlog_pretty.SyntaxHighlighter({'request': 'json', 'response': 'json', 'soap_response': 'xml'}),
        structlog_pretty.MultilinePrinter(['request', 'response', 'soap_response']),
        # ...
    ],

.. _structlog: https://github.com/hynek/structlog
