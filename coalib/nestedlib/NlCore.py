from coalib.nestedlib.NlInfoExtractor import (generate_arg_list,get_orig_file,
  get_temp_file_lang)
from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.parsing.CliParsing import parse_cli
from collections import OrderedDict
from coalib.settings.Section import Section, append_to_sections
from pprint import pprint
import os


def parse_nl_cli(arg_list,nl_info_dict):
    """
    Create a nested language coala section for the args.

    This function decorates the parse_cli method to create the coala nl_section
    """
    nl_sections = OrderedDict()
    for args in arg_list:
        sections = parse_cli(args=args)
        file_name = args.__dict__['files']
        # Append the language of the file 
        append_to_sections(sections,
                           'file_lang',
                           get_temp_file_lang(nl_info_dict, file_name),
                           origin=os.getcwd(),
                           section_name='cli',
                           from_cli=True)

        # Append the original file name
        append_to_sections(sections,
                           'orig_file_name',
                           get_orig_file(nl_info_dict, file_name),
                           origin=os.getcwd(),
                           section_name='cli',
                           from_cli=True)

        nl_section_name = "cli_nl_section: " + file_name
        nl_sections[nl_section_name]=sections['cli']

    return nl_sections




def get_nl_coala_sections(args):
    """
    Generate the coala sections for all the nested languages.
    """
    arg_list, nl_info_dict = generate_arg_list(args)
    sections = parse_nl_cli(arg_list,nl_info_dict)



if __name__ == '__main__':
    args = default_arg_parser().parse_args()
    get_nl_coala_sections(args)
