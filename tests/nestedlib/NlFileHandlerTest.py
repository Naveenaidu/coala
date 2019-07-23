import os
import unittest
from os.path import abspath

from coalib.nestedlib.NlFileHandler import (get_nl_file_dict, 
                                            get_nl_sections,
                                            get_line_list, 
                                            beautify_line_list, 
                                            get_nl_file_dict)
from coalib.nestedlib.parsers.PyJinjaParser import PyJinjaParser


TEST_FILE_DIR = os.path.join(os.path.split(__file__)[0],
                             'parsers/file_test_files')


class NlFileHandler(unittest.TestCase):

    def setUp(self):
        self.file_test_dir = TEST_FILE_DIR
        self.test_filename1 = 'test-jinja-py.py.jj2.txt'
        self.test_file1_path = os.path.join(self.file_test_dir,
                                            self.test_filename1)
        self.abs_test_file1_path = abspath(self.test_file1_path)

        self.parser = PyJinjaParser()
        self.all_nl_sections = self.parser.parse(self.abs_test_file1_path)

    def test_get_nl_sections(self):
        uut_lang = 'jinja2'
        uut_all_nl_sections = self.all_nl_sections
        uut_nl_sections = get_nl_sections(uut_all_nl_sections, uut_lang)
        uut_section_list = []

        expected_nl_sections = [
            self.abs_test_file1_path + ': 2: jinja2: L2 C1: L5 C10:'+
            ' L2 C1: L5 C10',
            self.abs_test_file1_path + ': 3: jinja2: L6 C1: L6 C13:'+
            ' L6 C1: L6 C13'
        ]

        for nl_section in uut_nl_sections:
            uut_section_list.append(str(nl_section))

        self.assertEqual(uut_section_list, expected_nl_sections)

    def test_get_line_list(self):
        uut_lang = 'jinja2'
        uut_all_nl_sections = self.all_nl_sections
        uut_nl_sections = get_nl_sections(uut_all_nl_sections, uut_lang)
        uut_line_list = get_line_list(
            uut_nl_sections, self.abs_test_file1_path)

        expected_line_list = [' ',
                              '{% if x is True %}\n',
                              '    {% set var3 = value3 %}\n',
                              '    \n',
                              '{% elif %}\n',
                              '    {{ var }}                   '
                              ]

        self.assertEqual(uut_line_list, expected_line_list)

    def test_beautify_line_list(self):

        uut_line_list = ['',
                         ' ',
                         '\n',
                         '  \n',
                         '\n  ',
                         '    {% set var3 = value3 %}\n',
                         '{% elif %}',
                         '    {{ var }}                   '
                         ]

        expected_line_tuple = ('\n',
                               '\n',
                               '\n',
                               '\n',
                               '\n',
                               '    {% set var3 = value3 %}\n',
                               '{% elif %}\n',
                               '    {{ var }}                   \n'
                               )

        beautified_line_tuple = beautify_line_list(uut_line_list)

        self.assertEqual(beautified_line_tuple, expected_line_tuple)

    def test_get_nl_file_dict(self):
        uut_temp_file_name = self.test_filename1 + '_nl_jinja2'
        uut_lang = 'jinja2'
        uut_file_dict = get_nl_file_dict(self.abs_test_file1_path,
                                         uut_temp_file_name, uut_lang, 
                                         self.parser)

        expected_file_dict = {
            'test-jinja-py.py.jj2.txt_nl_jinja2': (
                '\n',
                '{% if x is True %}\n',
                '    {% set var3 = value3 %}\n',
                '\n',
                '{% elif %}\n',
                '    {{ var }}                   \n'
            )
        }

        self.assertEqual(uut_file_dict, expected_file_dict)

    def test_coala_setup_template(self):
        """
        Test the jinja temporary file generated for coala setup template file.
        """
        uut_test_filename = 'test-setup-py.py.jj2.txt'
        uut_test_file_path = os.path.join(
            self.file_test_dir, uut_test_filename)
        uut_abs_test_file_path = abspath(uut_test_file_path)
        uut_temp_file_name = 'test-setup-py.py.jj2.txt_nl_jinja2'

        temp_file_dict = get_nl_file_dict(uut_abs_test_file_path, 
                                          uut_temp_file_name, 
                                          'jinja2',
                                          self.parser)

        """
        # Get the file_dict as a string.
        # It's easier for comparision
        temp_file_output_name = 'coala_setup_jinja2_temp_file.py.jj2.txt'
        temp_file_output_dir = os.path.join(os.path.split(__file__)[0],
                            'test_files_output')
        temp_file_output_path = os.path.join(self.temp_file_output_dir,
                                                temp_file_output_name)
        abs_temp_file_output_path = abspath(temp_file_output_path)
        temp_file_dict_output_file = File(abs_temp_file_output_path)

        expected_output_string =  temp_file_dict_output_file.string
        """

        expected_tuple = ('{% if not scm_host %}\n',
                          "{% set scm_host = 'github.com' %}\n",
                          '{% endif %}\n',
                          '{% block shebang %}\n',
                          '\n',
                          '{% endblock %}\n',
                          "{% set min_python_version = min_python_version|default('2.6') %}\n",
                          "{% set min_python_version = min_python_version.split('.', 2) %}\n",
                          '\n',
                          '{% block header %}\n',
                          '\n',
                          '{% endblock %}\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '{% if external_module_library %}\n',
                          '\n',
                          '{% else %}\n',
                          '\n',
                          '\n',
                          '\n',
                          '{%endif%}\n',
                          '{%block compat_block%}\n',
                          '\n',
                          '\n',
                          '\n',
                          '{%endblock%}\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '{% if PY33 %}\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '{% endif %}\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '        {{name}} \n',
                          '          {{author}} \n',
                          '           {{current_version}} \n',
                          '         {{contact}} \n',
                          '           {{license}} \n',
                          '{% if MAINTAINER %}\n',
                          '              {{maintainer}} \n',
                          '                      {{maintainer_contact}} \n',
                          '{% endif %}\n',
                          '{% if command_line_interface or entry_points %}\n',
                          '\n',
                          "{% if not entry_points or 'console_scripts' not in entry_points %}\n",
                          '\n',
                          '         {{command_line_interface}}   {{ entry_point }} \n',
                          '\n',
                          '{% endif %}\n',
                          '{% if entry_points %}\n',
                          '  {% for group_name, items in entry_points.items() %}\n',
                          '     {{group_name}}    \n',
                          '      {% if group_name == "console_scripts" and command_line_interface %}\n',
                          '         {{command_line_interface}}   {{ entry_point }}  \n',
                          '      {% endif %}\n',
                          '      {% for item in items %}\n',
                          '         {{item}}  \n',
                          '      {% endfor %}\n',
                          '\n',
                          '  {% endfor %}\n',
                          '{% endif %}\n',
                          '\n',
                          '{% endif %}\n',
                          '\n',
                          '{% for line in description | split_length(70) %}\n',
                          '     {{ line }} {{ " +" if not loop.last}}\n',
                          '{% endfor %}\n',
                          '\n',
                          '               {{scm_host}} {{organisation}} {{name}} \n',
                          '                           {{release}}              \n',
                          '                      {%block morefiles %}{%endblock%}                 \n',
                          '{% if self.additional_keywords %}\n',
                          '{% set additional_keywords = self.additional_keywords() %}\n',
                          '{% if additional_keywords and not additional_keywords.rstrip().endswith(",") %}\n',
                          '{% set additional_keywords = additional_keywords.rstrip() + ",\\n" %}\n',
                          '{% endif %}\n',
                          '{% endif %}\n',
                          '\n',
                          '\n',
                          '{% for keyword in keywords %}\n',
                          '     {{keyword}}  \n',
                          '{% endfor %}\n',
                          '    {%block additional_keywords -%}\n',
                          '    {%endblock%}\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '    {% if min_python_version <= ["2", "6"] %}\n',
                          '\n',
                          '    {%- endif %}\n',
                          '\n',
                          '    {% if min_python_version <= ["2", "7"] %}\n',
                          '\n',
                          '    {%- endif %}\n',
                          '\n',
                          '    {%- if min_python_version[0] == "3" %}\n',
                          '\n',
                          '    {%- endif %}\n',
                          '\n',
                          '    {% if min_python_version <= ["3","3"] %}\n',
                          '\n',
                          '    {%- endif %}\n',
                          '\n',
                          '    {% if min_python_version <= ["3","4"] %}\n',
                          '\n',
                          '    {%- endif %}\n',
                          '\n',
                          '    {% if min_python_version <= ["3","5"] %}\n',
                          '\n',
                          '    {%- endif %}\n',
                          '\n',
                          '    {% if min_python_version <= ["3","6"] %}\n',
                          '\n',
                          '    {% endif %}\n',
                          '\n',
                          '    {% if min_python_version <= ["3","7"] %}\n',
                          '\n',
                          '    {% endif %}\n',
                          '\n',
                          '    {% if min_python_version <= ["3","8"] %}\n',
                          '\n',
                          '    {% endif %}\n',
                          '\n',
                          '    {%block additional_classifiers%}\n',
                          '    {%endblock %}\n',
                          '\n',
                          '\n',
                          '{%macro handle_complex_dependency(complex_one) -%}\n',
                          '{%set dependency, condition = complex_one.split(";")%}\n',
                          '{% if condition == \'python_version<"3"\'%}\n',
                          '\n',
                          '{% endif %}\n',
                          '{% if condition == \'python_version>="3"\'%}\n',
                          '\n',
                          '{% endif %}\n',
                          '{% if condition == \'python_version<"2.7"\'%}\n',
                          '\n',
                          '{% endif %}\n',
                          '{% if condition == \'platform_python_implementation=="PyPy"\'%}\n',
                          '\n',
                          '{%endif%}\n',
                          '                             {{dependency}}  \n',
                          '{%- endmacro %}\n',
                          '\n',
                          '{% for dependency in dependencies: %}\n',
                          "  {% if ';' not in dependency and not dependency.startswith('#'): %}\n",
                          "    {% if '#egg=' in dependency: %}\n",
                          "      {% set dependency = dependency.split('#egg=') %}\n",
                          '      {% set repo_link, egg_name = dependency[0], dependency[1] %}\n',
                          '      {% set repo_link = repo_link.strip() %}\n',
                          "      {% if '#' in egg_name: %}\n",
                          "        {% set egg_name = egg_name.split('#')[0].strip() %}\n",
                          '      {% endif %}\n',
                          "     {{[repo_link, egg_name] | join('#egg=')}}  \n",
                          "    {% elif '#' in dependency: %}\n",
                          "      {% set dependency = dependency.split('#')[0].strip() %}\n",
                          '     {{dependency}}  \n',
                          '    {% else %}\n',
                          '     {{dependency}}  \n',
                          '    {% endif %}\n',
                          '  {%   endif %}\n',
                          '{% endfor %}\n',
                          '\n',
                          '{% block additional_setup_commands %}\n',
                          '\n',
                          '{% endblock %}\n',
                          '\n',
                          '{% for dependency in dependencies: %}\n',
                          "  {%  if ';' in dependency: %}\n",
                          '{{handle_complex_dependency(dependency)}}\n',
                          '  {%   endif %}\n',
                          '{% endfor %}\n',
                          '\n',
                          '{% if external_module_library %}\n',
                          '\n',
                          '     {{name}}  \n',
                          '\n',
                          '{% for source in sources: %}\n',
                          '         {{source}}  \n',
                          '{% endfor %}\n',
                          '\n',
                          '\n',
                          '\n',
                          '{% else %}\n',
                          '\n',
                          '{% if extra_dependencies or dependencies: %}\n',
                          '\n',
                          '  {% for dependency in extra_dependencies: %}\n',
                          '     {% for key, value in dependency.items(): %}\n',
                          '     {{key}}   {{value}} \n',
                          '     {% endfor %}\n',
                          '  {% endfor %}\n',
                          '\n',
                          '{% else: %}\n',
                          '\n',
                          '{% endif %}\n',
                          '{% endif %}\n',
                          '\n',
                          '{% if nowheel %}\n',
                          '\n',
                          '{% else %}\n',
                          '\n',
                          '{% endif %}\n',
                          '                  {{name}}  {{release}}    \n',
                          '                    {{release}}                                \n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          "                                       {{name|replace('-', '_')}}            \n",
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '{% if "tests" is exists %}\n',
                          '\n',
                          '{% endif %}\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '{% if MAINTAINER %}\n',
                          '\n',
                          '\n',
                          '{% endif %}\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '{% if external_module_library %}\n',
                          '\n',
                          '{% else %}\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '\n',
                          '{% if command_line_interface or entry_points %}\n',
                          '\n',
                          '{% endif %}\n',
                          '{% endif%}\n',
                          '\n',
                          '\n',
                          '\n')
        self.assertEqual(temp_file_dict[uut_temp_file_name], expected_tuple)
