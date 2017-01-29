"""The Jinja2 coverage plugin."""

import os.path
import coverage.plugin
from jinja2 import Environment
from jinja2.loaders import FileSystemLoader


# For debugging the plugin itself.
SHOW_PARSING = True
SHOW_TRACING = False


class JinjaPlugin(coverage.plugin.CoveragePlugin):
    def __init__(self, options):
        self.template_directory = options.get("template_directory")
        self.environment = Environment(
            loader=FileSystemLoader(self.template_directory),
            extensions=[]
        )

    def file_tracer(self, filename):
        if os.path.samefile(os.path.dirname(filename), self.template_directory):
            return FileTracer(filename)

    def file_reporter(self, filename):
        if os.path.samefile(os.path.dirname(filename), self.template_directory):
            return FileReporter(filename, self.environment)


class FileTracer(coverage.plugin.FileTracer):
    def __init__(self, filename):
        self.metadata = {'filename': filename}

    def source_filename(self):
        return self.metadata["filename"]

    def line_number_range(self, frame):
        lineno = -1
        env = frame.f_locals.get('environment')
        if env:
            template = env.get_template(os.path.basename(frame.f_code.co_filename))
            lineno = template.get_corresponding_lineno(frame.f_lineno)

        if lineno == 0:
            # Zeros should not be tracked, return -1 to skip them.
            lineno = -1
        return lineno, lineno


class FileReporter(coverage.plugin.FileReporter):
    def __init__(self, filename, environment):
        super(FileReporter, self).__init__(filename)
        self._source = None
        self.environment = environment

    def source(self):
        if self._source is None:
            with open(self.filename) as f:
                self._source = f.read()
        return self._source

    def lines(self):
        source_lines = set()

        if SHOW_PARSING:
            print("-------------- {}".format(self.filename))

        tokens = self.environment._tokenize(self.source(), self.filename)

        for token in tokens:
            if SHOW_PARSING:
                print(token)

            source_lines.add(token.lineno)

            if SHOW_PARSING:
                print("\t\t\tNow source_lines is: {!r}".format(source_lines))

        return source_lines

def dump_frame(frame, label=""):
    """Dump interesting information about this frame."""
    locals = dict(frame.f_locals)
    self = locals.get('self', None)
    context = locals.get('context', None)
    if "__builtins__" in locals:
        del locals["__builtins__"]

    if label:
        label = " ( %s ) " % label
    print("-- frame --%s---------------------" % label)
    print("{}:{}:{}".format(
        frame.f_code.co_filename,
        frame.f_lineno,
        type(self),
        ))
    from pprint import pprint
    pprint(locals)
    if self:
        print("self:", self.__dict__)
    if context:
        print("context:", context.__dict__)
    print("\\--")
