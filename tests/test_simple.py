import os.path
import unittest

import coverage
from jinja2 import Environment
from jinja2.loaders import PackageLoader
from jinja2.exceptions import TemplateSyntaxError

class JinjaPluginTestCase(unittest.TestCase):
    """Base class for tests of the Jinja2 coverage.py plugin."""

    def _render(self, template_filename, context={}):
        "Helper method"
        env = Environment(
                loader=PackageLoader('tests', 'templates'),
                extensions=[],
            )
        template = env.get_template(template_filename)
        return template.render(context).strip()


    def do_jinja_coverage(self, template, context={}):
        """Run a Jinja coverage test.

        Args:
            template (str): the filename of the template.
            context (dict): data for the template.

        Returns:
            A tuple: (rendered_text, line_data)
            rendered_text: the rendered text.
            line_data: a list of line numbers executed.

        """
        template_dir = 'tests/templates'
        cov = coverage.Coverage(source=[template_dir])
        cov.config.plugins.append('jinja_coverage')
        cov.config.plugin_options['jinja_coverage'] = {'template_directory': template_dir}
        cov.start()
        text = self._render(template, context)
        cov.stop()
        cov.save()
        abs_path = os.path.abspath(os.path.join(template_dir, template))
        line_data = cov.data.lines(abs_path)
        return text, line_data


class TemplateTextTest(JinjaPluginTestCase):
    def test_one_line(self):
        """
            Depends on https://github.com/pallets/jinja/pull/673
        """
        return
        text, line_data = self.do_jinja_coverage('hello.html')
        self.assertEqual(text, "Hello World")
        self.assertEqual(line_data, [1])

    def test_empty_for_loop(self):
        text, line_data = self.do_jinja_coverage('loop.html', {'users': []})
        self.assertEqual(text, "<ul>\n  \n  </ul>")
        self.assertEqual(line_data, [1, 2, 3, 5, 6, 7])

    def test_non_empty_for_loop(self):
        text, line_data = self.do_jinja_coverage('loop.html', {'users': ['Alex', 'Mr. Senko']})
        self.assertEqual(text, "<ul>\n  \n    <li>Hello Alex</li>\n  \n    <li>Hello Mr. Senko</li>\n  \n  </ul>")
        self.assertEqual(line_data, [1, 2, 3, 4, 5, 6, 7])

    def test_if(self):
        text, line_data = self.do_jinja_coverage('if.html', {'user': 'Alex'})
        self.assertEqual(text, "Hello Alex")
        self.assertEqual(line_data, [1, 2, 3, 5])

    def test_else(self):
        text, line_data = self.do_jinja_coverage('if.html', {'user': ''})
        self.assertEqual(text, "Nobody home")
        self.assertEqual(line_data, [1, 3, 4, 5])
