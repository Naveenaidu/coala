from coalib.nestedlib.NlInfoExtractor import generate_arg_list
from coalib.parsing.DefaultArgParser import default_arg_parser

def get_nl_coala_sections(args=None):
    """
    Generate the coala sections for all the nested languages.
    """
    arg_list, nl_info_dict = generate_arg_list(args)


if __name__ == '__main__':
    args = default_arg_parser().parse_args()
    