from coalib.nestedlib.NlInfoExtractor import generate_arg_list
from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.parsing.CliParsing import parse_cli
from collections import OrderedDict
from coalib.settings.Section import Section, append_to_sections
from pprint import pprint


def parse_nl_cli(arg_list,nl_info_dict):
    """
    Create a nested language coala section for the args.

    This function decorates the parse_cli method to create the coala nl_section
    """
    nl_section = OrderedDict()
    for args in arg_list:
        sections = parse_cli(args=args)
        # Append the language of the file 
        append_to_sections(sections,
                           'file_lang',
                           arg_value,
                           origin=os.getcwd(),
                           section_name='cli',
                           from_cli=True)

        # Append the original file name
        append_to_sections(sections,
                           'orig_file_name',
                           arg_value,
                           origin=os.getcwd(),
                           section_name='cli',
                           from_cli=True)

        nl_section_name = "cli_nl_section: " + args.__dict__['files']
        nl_section[nl_section_name]=sections['cli']

    print(nl_section['cli_nl_section: test.py_nl_jinja2'])



def get_nl_coala_sections(args):
    """
    Generate the coala sections for all the nested languages.
    """
    arg_list, nl_info_dict = generate_arg_list(args)
    sections = parse_nl_cli(arg_list=arg_list,nl_info_dict)



if __name__ == '__main__':
    args = default_arg_parser().parse_args()
    get_nl_coala_sections(args)
