import os
import unittest
from os.path import abspath
from coalib.io.File import File

from coalib.nestedlib.NlFileHandler import (get_nl_file_dict, get_nl_sections,
    get_line_list, beautify_line_list )
from coalib.nestedlib.parsers.PyJinjaParser import PyJinjaParser
from coalib.nestedlib.NlSection import NlSection


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
            self.abs_test_file1_path + ': 2: jinja2: L2 C1: L5 C10: L2 C1: L5 C10',
            self.abs_test_file1_path + ': 3: jinja2: L6 C1: L6 C13: L6 C1: L6 C13'
        ]

        for nl_section in uut_nl_sections:
            uut_section_list.append(str(nl_section))

        self.assertEqual(uut_section_list, expected_nl_sections)

    def test_get_line_list(self):
        uut_lang = 'jinja2'
        uut_all_nl_sections = self.all_nl_sections
        uut_nl_sections = get_nl_sections(uut_all_nl_sections, uut_lang)
        uut_line_list = get_line_list(uut_nl_sections, self.abs_test_file1_path)

        expected_line_list = [  ' ',
                                '{% if x is True %}\n',
                                '    {% set var3 = value3 %}\n',
                                '    \n',
                                '{% elif %}\n',
                                '    {{ var }}                   '
                              ]

        self.assertEqual(uut_line_list, expected_line_list)

    def test_beautify_line_list(self):

        uut_line_list = [   '',
                            ' ',
                            '\n',
                            '    {% set var3 = value3 %}\n',
                            '{% elif %}',
                            '    {{ var }}                   '
                        ]

        expected_line_tuple = (  '\n',
                                '\n',
                                '\n',
                                '    {% set var3 = value3 %}\n',
                                '{% elif %}\n',
                                '    {{ var }}                   \n'
                             )

        beautified_line_tuple = beautify_line_list(uut_line_list)

        self.assertEqual(beautified_line_tuple, expected_line_tuple)


        





if __name__ == '__main__':
    unittest.main()