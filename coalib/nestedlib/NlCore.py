from coalib.nestedlib.NlInfoExtractor import generate_arg_list
from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.nestedlib.NlCliParsing import parse_nl_cli
from collections import OrderedDict
from coalib.settings.Section import Section, append_to_sections
from pprint import pprint
import os


def get_nl_coala_sections(args):
    """
    Generate the coala sections for all the nested languages.
    """
    arg_list, nl_info_dict = generate_arg_list(args)
    nl_sections = OrderedDict()
    for args in arg_list:
        temp_file_name = args.__dict__['files']
        nl_section_name = "cli_nl_section: " + temp_file_name
        sections = parse_nl_cli(args=args, nl_section_name=nl_section_name,
            nl_info_dict=nl_info_dict)
        nl_sections[nl_section_name] = sections[nl_section_name]

    return nl_sections

    #print(nl_sections['cli_nl_section: test.py_nl_python'],"\n")
    #print(nl_sections['cli_nl_section: test2.py_nl_python'],"\n")
    #print(nl_sections['cli_nl_section: test.py_nl_jinja2'],"\n")
    #print(nl_sections['cli_nl_section: test2.py_nl_jinja2'],"\n")



if __name__ == '__main__':
    args = default_arg_parser().parse_args()
    get_nl_coala_sections(args)
