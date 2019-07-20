from coalib.nestedlib.NlInfoExtractor import generate_arg_list
from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.nestedlib.NlCliParsing import parse_nl_cli
from collections import OrderedDict
from coalib.settings.Section import Section, append_to_sections
from pprint import pprint
import os
from importlib import import_module

# The supported Parser for the language combination
PARSER_LANG_COMB = [{'PyJinjaParser': {'python', 'jinja2'}}]


def get_parser(lang_comb):
    """
    Return the parser object for the combination of the languages
    """
    lang_comb = set(lang_comb.split(','))
    parser_name = ''

    for parser_lang_comb in PARSER_LANG_COMB:
        for parser, language in parser_lang_comb.items():
            if language == lang_comb:
                parser_name = parser

    parser_module_string = ('coalib.nestedlib.parsers.' + parser_name)
    parser = getattr(import_module(parser_module_string), parser_name)
    return parser()


def get_nl_coala_sections(args):
    """
    Generate the coala sections for all the nested languages.
    """
    arg_list, nl_info_dict = generate_arg_list(args)
    nl_sections = OrderedDict()
    for args in arg_list:
        temp_file_name = args.__dict__['files']
        nl_section_name = 'cli_nl_section: ' + temp_file_name
        sections = parse_nl_cli(args=args, nl_section_name=nl_section_name,
                                nl_info_dict=nl_info_dict)
        nl_sections[nl_section_name] = sections[nl_section_name]

    return nl_sections
