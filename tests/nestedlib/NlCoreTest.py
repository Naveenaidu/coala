import os
import unittest
import logging

from coalib.parsing.DefaultArgParser import default_arg_parser

from coalib.nestedlib.NlCore import (get_parser,
                                     get_nl_coala_sections,
                                     nested_language)
from coalib.nestedlib.parsers.PyJinjaParser import PyJinjaParser


class NlCoreTest(unittest.TestCase):

    def setUp(self):
        self.arg_parser = default_arg_parser()
        self.test_dir_path = os.path.abspath(__file__ + "/../..")
        self.test_bear_path = os.path.join(self.test_dir_path, "test_bears")
        self.arg_list = ['--no-config', '--handle-nested',
                         '--bears=PEP8TestBear,Jinja2TestBear',
                         '--languages=python,jinja2', '--files=test.py',
                         '--bear-dirs='+self.test_bear_path
                         ]
        self.args = self.arg_parser.parse_args(self.arg_list)

    def test_get_parser_PyJinjaParser(self):
        uut_lang_comb = 'python,jinja2'
        parser = get_parser(uut_lang_comb)
        assert isinstance(parser, PyJinjaParser)

        # Test for parser not found
        uut_lang_comb = 'python,cpp'
        logger = logging.getLogger()
        with self.assertLogs(logger, 'ERROR') as cm:
            with self.assertRaises(SystemExit):
                parser = get_parser(uut_lang_comb)
                self.assertRegex(
                    cm.output[0],
                    "No Parser found for the languages combination")

    def test_get_nl_coala_sections(self):

        uut_nl_sections = get_nl_coala_sections(args=self.args)
        self.assertEqual(
            str(uut_nl_sections['cli_nl_section: test.py_nl_python']),
            "cli_nl_section: test.py_nl_python {targets : '', " +
            "bear_dirs : '/home/theprophet/git/coala-repos/coala/tests/test_bears', "+
            "bears : 'PEP8TestBear', files : 'test.py_nl_python', " +
            "handle_nested : 'True', languages : 'python,jinja2', " +
            "no_config : 'True', file_lang : 'python', " +
            "orig_file_name : 'test.py'}")

        # When arg_list is passed
        uut_nl_sections = get_nl_coala_sections(arg_list=self.arg_list)
        self.assertEqual(
            str(uut_nl_sections['cli_nl_section: test.py_nl_python']),
            "cli_nl_section: test.py_nl_python {targets : '', " +
            "bear_dirs : '/home/theprophet/git/coala-repos/coala/tests/test_bears', "+
            "bears : 'PEP8TestBear', files : 'test.py_nl_python', " +
            "handle_nested : 'True', languages : 'python,jinja2', " +
            "no_config : 'True', file_lang : 'python', " +
            "orig_file_name : 'test.py'}")

    def test_nested_language(self):
        # When --handle-nested is present
        handle_nested = nested_language(args=self.args)
        self.assertTrue(handle_nested)

        # When --handle-nested is passed via arg_list
        handle_nested = nested_language(arg_list=self.arg_list)
        self.assertTrue(handle_nested)

        # When --handle-nested is not present
        handle_nested = nested_language(arg_list=[])
        self.assertFalse(handle_nested)
