Jinja2 Coverage Plugin
======================

A coverage.py plugin to measure the coverage of Jinja2 templates.

Install
-------

::

    $ pip install jinja_coverage

Configuration
-------------

Edit your ``.coveragerc`` to contain::

    [run]
    plugins =
        jinja_coverage

    [jinja_coverage]
    template_directory = path/to/templates

Known issues
------------

This plugin appears to be collecting and reporting coverage information
correctly. However Jinja2 does not provide enough information to map
the collected data to the appropriate lines in the HTML template. For
more information see
`Jinja #674 <https://github.com/pallets/jinja/pull/674>`_.

Testing
-------

::

    $ pip install -r requirements.txt
    $ python -m unittest discover
