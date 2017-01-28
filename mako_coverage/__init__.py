"""Mako template coverage.py plugin."""

from plugin import MakoPlugin

def coverage_init(reg, options):
    reg.add_file_tracer(MakoPlugin(options))
