from coalib.nestedlib.NlInfoExtractor import generate_arg_list
from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.nestedlib.NlCliParsing import parse_nl_cli
from collections import OrderedDict
from importlib import import_module
from coalib.settings.Setting import glob_list, typed_list
from coalib.parsing.DefaultArgParser import default_arg_parser
import logging


# The supported Parser for the language combination
PARSER_LANG_COMB = [{'PyJinjaParser': {'python', 'jinja2'}}]

def get_nl_sections_parser(section):
    """
    Get the Nested language section created by the parser
    """
    parser = get_parser(section.get('languages').value)
    orig_file_path = glob_list(section.get('orig_file_name', ''))[0]
    all_nl_sections = parser.parse(orig_file_path)

    return all_nl_sections


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
    try:
        parser = getattr(import_module(parser_module_string), parser_name)
    except:
        logging.error('No Parser found for the languages combination')
        raise SystemExit(2)

    return parser()


def get_nl_coala_sections(args=None, arg_list=None, arg_parser=None):
    """
    Generate the coala sections for all the nested languages.
    """
    assert not (arg_list and args), (
        'Either call parse_cli() with an arg_list of CLI arguments or '
        'with pre-parsed args, but not with both.')

    if args is None:
        arg_parser = default_arg_parser() if arg_parser is None else arg_parser
        args = arg_parser.parse_args(arg_list)

    arg_list, nl_info_dict = generate_arg_list(args)
    nl_sections = OrderedDict()
    for args in arg_list:
        temp_file_name = args.__dict__['files']
        nl_section_name = 'cli_nl_section: ' + temp_file_name
        sections = parse_nl_cli(args=args,
                                nl_section_name=nl_section_name,
                                nl_info_dict=nl_info_dict)
        nl_sections[nl_section_name] = sections[nl_section_name]

    return nl_sections


def nested_language(args=None, arg_list=None, arg_parser=None):
    """
    Check if handle_nested condition is present in arguments
    """
    handle_nested = False
    # If args is None check if arg_list has handle_nested.
    if args is None:
        arg_parser = default_arg_parser() if arg_parser is None else arg_parser
        nested_args = arg_parser.parse_args(arg_list)
        if nested_args.handle_nested:
            handle_nested = True
    else:
        if args.handle_nested:
            handle_nested = True

    return handle_nested

def print_nl_sections(nl_sections):
    str_nl_section = []
    for nl_section in nl_sections:
        # For debugging let's remove the file name
        #str_nl_section.append(str(nl_section))
        str_section = str(nl_section).split(':')
        str_nl_section.append(str_section[1:])

    return str_nl_section
