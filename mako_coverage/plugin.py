"""The Mako coverage plugin."""

import os.path

from mako.template import ModuleInfo
import coverage.plugin


class MakoPlugin(coverage.plugin.CoveragePlugin):
    def __init__(self, options):
        self.module_directory = options.get("module_directory")

    def file_tracer(self, filename):
        if os.path.samefile(os.path.dirname(filename), self.module_directory):
            return FileTracer(filename)


class FileTracer(coverage.plugin.FileTracer):
    def __init__(self, filename):
        with open(filename) as f:
            py_source = f.read()
        if 0:
            for i, line in enumerate(py_source.splitlines(), start=1):
                print "%3d: %s" % (i, line)
        self.metadata = ModuleInfo.get_module_source_metadata(py_source)#, full_line_map=True)
        if 0:
            print self.metadata

    def source_filename(self):
        return self.metadata["filename"]

    def line_number_range(self, frame):
        lineno = self.metadata["line_map"].get(frame.f_lineno, -1)
        if 0:
            print "range: %r -> %r" % (frame.f_lineno, lineno)
        if lineno == 0:
            # Zeros should not be tracked, return -1 to skip them.
            lineno = -1
        return lineno, lineno
