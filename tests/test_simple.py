import os.path, unittest

import coverage
import mako.template

from coverage.test_helpers import TempDirMixin

class MakoPluginTestCase(TempDirMixin, unittest.TestCase):
    """Base class for tests of the Mako coverage.py plugin."""

    def do_mako_coverage(self, template, context={}):
        """Run a Mako coverage test.

        Args:
            template (str): the text of the template.
            context (dict): data for the template.

        Returns:
            A tuple: (rendered_text, line_data)
            rendered_text: the rendered text.
            line_data: a list of line numbers executed.

        """
        template_dir = self.make_temp_dir("mako_template")
        maktem = mako.template.Template(filename=template, module_directory=template_dir)
        cov = coverage.Coverage(source=["."])
        cov.config["run:plugins"].append("mako_coverage")
        cov.config["mako_coverage:module_directory"] = template_dir
        cov.start()
        text = maktem.render(**context)
        cov.stop()
        cov.save()
        line_data = cov.data.line_data()[os.path.realpath(template)]
        return text, line_data


class TemplateTextTest(MakoPluginTestCase):
    def test_one_line(self):
        self.make_file("template.mako", "Hello\n")
        text, line_data = self.do_mako_coverage("template.mako")
        self.assertEqual(text, "Hello\n")
        self.assertEqual(line_data, [1])

    def test_sequence(self):
        self.make_file("one23.mako", """\
            One
            Two
            Three
            """)
        text, line_data = self.do_mako_coverage("one23.mako")
        self.assertEqual(text, "One\nTwo\nThree\n")
        self.assertEqual(line_data, [1])

    def test_if(self):
        self.make_file("if.mako", """\
            % if 1+1 == 2:
                Two!
            % else:
                Not Two!
            % endif
            """)
        text, line_data = self.do_mako_coverage("if.mako")
        self.assertEqual(text, "    Two!\n")
        self.assertEqual(line_data, [1, 2])

    def test_if_intro_outro(self):
        self.make_file("if.mako", """\
            intro
            % if 1+1 == 2:
                Two!
            % else:
                Not Two!
            % endif
            outro
            """)
        text, line_data = self.do_mako_coverage("if.mako")
        self.assertEqual(text, "intro\n    Two!\noutro\n")
        self.assertEqual(line_data, [1, 2, 3, 7])

    def test_else(self):
        self.make_file("else.mako", """\
            % if 1+1 == 3:
                Three!
            % else:
                Two!
            % endif
            """)
        text, line_data = self.do_mako_coverage("else.mako")
        self.assertEqual(text, "    Two!\n")
        self.assertEqual(line_data, [1, 4])

    def test_else_intro_outro(self):
        self.make_file("else.mako", """\
            intro
            % if 1+1 == 3:
                Three!
            % else:
                Two!
            % endif
            outro
            """)
        text, line_data = self.do_mako_coverage("else.mako")
        self.assertEqual(text, "intro\n    Two!\noutro\n")
        self.assertEqual(line_data, [1, 2, 5, 7])

    def test_elif(self):
        self.make_file("elif.mako", """\
            % if 1+1 == 3:
                Three!
            % elif 1+1 == 2:
                Two!
            % else:
                Not Two!
            % endif
            """)
        text, line_data = self.do_mako_coverage("elif.mako")
        self.assertEqual(text, "    Two!\n")
        self.assertEqual(line_data, [1, 3, 4])

    def test_elif_intro_outro(self):
        self.make_file("elif.mako", """\
            intro
            % if 1+1 == 3:
                Three!
            % elif 1+1 == 2:
                Two!
            % else:
                Not Two!
            % endif
            outro
            """)
        text, line_data = self.do_mako_coverage("elif.mako")
        self.assertEqual(text, "intro\n    Two!\noutro\n")
        self.assertEqual(line_data, [1, 2, 4, 5, 9])


class PythonCodeTest(MakoPluginTestCase):
    def test_if_else(self):
        self.make_file("embedded.mako", """\
            <%
            def foo(x):
                if x:
                    return 10
                else:
                    return 11
            %>
            Hello ${foo(value)}
            """)
        text, line_data = self.do_mako_coverage("embedded.mako", {'value':0})
        self.assertEqual(text.strip(), "Hello 11")
        self.assertEqual(line_data, [2, 3, 6, 8])

        text, line_data = self.do_mako_coverage("embedded.mako", {'value':1})
        self.assertEqual(text.strip(), "Hello 10")
        self.assertEqual(line_data, [2, 3, 4, 8])
