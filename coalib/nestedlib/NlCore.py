from coalib.nestedlib.NlInfoExtractor import generate_arg_list
from coalib.parsing.DefaultArgParser import default_arg_parser
from coalib.nestedlib.NlCliParsing import parse_nl_cli
from collections import OrderedDict
from importlib import import_module

from coalib.parsing.DefaultArgParser import default_arg_parser
import logging
import os
from copy import deepcopy
from coalib.settings.Setting import glob_list,Setting
import shutil
from os.path import isfile
from os import remove
from coala_utils.FileUtils import detect_encoding


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
    """
    Print the str repersenation of the
    """
    str_nl_section = ""
    for nl_section in nl_sections:
        # For debugging let's remove the file name
        #str_nl_section.append(str(nl_section))
        str_section = str(nl_section)
        str_nl_section += str_section + "\n"

    return str_nl_section

def get_temp_file_content(nl_file_dicts, temp_file_name):
    """
    Get the temp file dict of temp_file_name from the patched 
    nl_file_dicts.
    
    If you a nested file `test.py` which contains python and jinja as the
    nested language, then the 

    nl_file_dicts looks something like this:

    ```
    {
        'cli_nl_section: test.py_nl_python': 
            {'test.py_nl_python': ['!!! Start Nl Section: 1\n', '\n', '\n', 
                                    'def hello():\n', '\n', '\n', 
                                    '!!! End Nl Section: 1\n', '\n', '\n', 
                                  ]},  

        'cli_nl_section: test.py_nl_jinja2': 
            {'test.py_nl_jinja2': ['\n', 
                                   '!!! Start Nl Section: 2\n', 
                                   '    {{ x }} asdasd {{ Asd }}\n', 
                                   '!!! End Nl Section: 2\n', 
                                   ]},
    }
    ```
    """
    for nl_coala_section, temp_file in nl_file_dicts.items():
        for filename, file_content in temp_file.items():
            if temp_file_name == filename:
                return file_content

def remove_position_markers(temp_file_content):
    """
    Remove the position markers from the line.

    Return a dicitionary where the key is the section index and the value
    is the content of the section index.
    """
    section_index_lines_dict = {}
    section_index = None
    append_lines = False
    line_list = []

    for line in temp_file_content:
        
        if 'Start Nl Section: ' in line:
            section_index = int(line.split(": ")[1])
            append_lines = True
            continue

        elif 'End Nl Section: ' in line:
            section_index_lines_dict[section_index] = deepcopy(line_list)
            append_lines =  False
            section_index = None
            line_list.clear()

        if append_lines:
            line_list.append(line)

    return section_index_lines_dict

def get_orig_file_dict(nl_file_dicts, nl_file_info_dict):
    """
    Generate the file dict for every original file where we have 
    section_index as the key and the content on the line as the value.

    We'll get the file_dict of the temporary files of each original file,
    process the file dict to remove the position markers and then create a
    new file dictionary, where we store the key as the section index and the
    content of that section as it's value.

    Something like:

    {'test.py': {
                    '1': [ 'def hello(): \n' ] ,
                    '2': [  '\n', '\n'],
                    '3': [ '    {{ x }} asdasd {{ Asd }}\n ],
                    '4': [ '{{ x }}\n']
                }
    }
    """

    file_dict = {}

    for orig_file, temp_file_info in nl_file_info_dict.items():
        for lang, temp_filename in temp_file_info.items():
            temp_file_content = get_temp_file_content(nl_file_dicts, 
                                                      temp_filename)

            # PostProcess the lines to remove the position markers
            # Generate a dict which has the key as the section index
            # and the value as the content of the section. This will
            # help in assembling.
            section_index_lines = remove_position_markers(
                                                    temp_file_content)
            if not file_dict.get(orig_file):
                file_dict[orig_file] =  section_index_lines
            else:
                file_dict[orig_file].update(section_index_lines)

    return file_dict

def generate_linted_file_dict(original_file_dict):
    """
    Generate a dict with the orig_filename as the key and the value as the 
    file contents of the file.

    Use the section indexes present in the original_file_dict to assemble
    all the sections and generate the actual linted file.
    """
    linted_file_dict = {}
    for file, section_line_dict in original_file_dict.items():
        if not linted_file_dict.get(file):
            linted_file_dict[file] = []
        for section_index in sorted(section_line_dict):
            section_content = section_line_dict[section_index]
            linted_file_dict[file].extend(section_content)
        
    return linted_file_dict

def write_patches_to_orig_nl_file(linted_file_dict, sections):
    """
    Update the original Nested language file with the patches that the user
    chose to apply.

    We create a backup with the extension of `.orig` similar to how coala
    does when it writes the patches to the file.
    """
    for filename, patched_filecontent in linted_file_dict.items():
        orig_file_path = get_original_file_path(sections, filename)

        # Backup original file
        if isfile(orig_file_path):
            shutil.copy2(orig_file_path,
                         orig_file_path + '.orig')

        with open(orig_file_path, mode='w',
                  encoding=detect_encoding(orig_file_path)) as file:
            file.writelines(patched_filecontent)

    return

def get_original_file_path(sections, filename):
    """
    Get the origin of the filename. 
    Return the path where the file is located.
    """
    for section_name in sections:
        section = sections[section_name]
        if str(section.get('orig_file_name')) == filename:
            
            return glob_list(section.get('orig_file_name', ''))[0]

def apply_patches_to_nl_file(nl_file_dicts, args=None, arg_list=None,
                             nl_info_dict=None, sections=None):
    """
    Write the accepted patches into the original nested language file.

    We assemble the applied patches from all the temporary linted pure 
    language file and preprocess it to remove the `nl section position` 
    markers and then write it to the original file. 

    We can use the generate_arg_list function to get more information about
    the original file and temporary file.
    'nl_file_info': {   'test.py' : { 
                                        'python' : 'test.py_nl_python',
                                        'jinja2' : 'test.py_nl_jinja2'
                                    },

                        'test2.py': {
                                        'python' : 'test2.py_nl_python',
                                        'jinja2' : 'test2.py_nl_jinja2'
                                    }   
                    }    
    """
    if args is None:
        arg_parser = default_arg_parser() if arg_parser is None else arg_parser
        args = arg_parser.parse_args(arg_list)

    if not nl_info_dict:
        arg_list, nl_info_dict = generate_arg_list(args)
    nl_file_info_dict = nl_info_dict['nl_file_info']

    original_file_dict = get_orig_file_dict(nl_file_dicts,
                                            nl_file_info_dict)
    linted_file_dict = generate_linted_file_dict(original_file_dict)
    write_patches_to_orig_nl_file(linted_file_dict, sections)




