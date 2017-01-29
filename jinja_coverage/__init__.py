"""Jinja2 template coverage.py plugin."""

from .plugin import JinjaPlugin

def coverage_init(reg, options):
    reg.add_file_tracer(JinjaPlugin(options))
