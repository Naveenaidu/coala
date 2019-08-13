from coalib.io.File import File


def get_nl_sections(all_nl_sections, lang):
    """
    Get the nl_section of a particular language from all the nl_sections of the
    file. And sort the nl_section according to their index.

    When the parser parses the file, it returns a list of nl_section containing
    all the nested language. In order to make a file_dict, only the sections
    belonging to one language is needed.

    :param all_nl_sections: The list of nl_sections the parser ouputs
    :param lang:            The language whose nl_section is needed.
    """
    # Get nl_section of `lang` language
    nl_sections = []
    #print("\n NLFILE HANDLER GET NL SECTION",all_nl_sections)
    #print("\n NLFILE HANDLER GET NL SECTION LANG", lang)
    for nl_section in all_nl_sections:
        #print(type(nl_section.language))
        #print(type(lang))
        #print(nl_section.language == lang)
        if nl_section.language == lang:
            #print("TRUEEEEE")
            nl_sections.append(nl_section)

    #print("\n NLFILE HANDLER GET NL SECTION nl_Section ", nl_sections)
    # Sort the nl_sections according to their indices
    nl_sections = sorted(nl_sections, key=lambda nl_section: nl_section.index)
    return nl_sections


def get_line_list(nl_sections, orig_file_path):
    """
    Create a list of lines that would be present in the temporary file.

    From the nl_sections, get the information of start and end and use this to
    get the content at those positions.

    :param nl_sections:     The nl_sections belonging to one language
    :param orig_file_path:  The absolute path of the original nested file.
    """
    file = File(orig_file_path)

    # Initialiaze a line_list with whitespace. The lenght of this list will
    # be equal to the number of lines in the actual files.
    # The index of the list points to the line number of the original file.
    # The means line_list[3] contains the line at line number 4 of the original
    # file.
    line_list = []
    line_list = [' ' for index in range(0, file.__len__())]

    for nl_section in nl_sections:

        start_line = nl_section.start.line
        start_column = nl_section.start.column
        end_line = nl_section.end.line
        end_column = nl_section.end.column

        for line_nr in range(start_line, end_line+1):

            # Make the length of line equal to the length of original line
            if(line_list[line_nr-1].isspace()):
                line_list[line_nr-1] = ' '*len(file[line_nr-1])

            orig_line = file[line_nr-1]
            end_orig_line = len(orig_line)-1
            line = line_list[line_nr-1]

            # If the section contains only one line.
            # This case generally happens for mixed lang line
            if (line_nr == start_line and line_nr == end_line):
                # section_content stores the part of the line that belongs to
                # the section.
                section_content = file[line_nr-1][start_column-1:end_column]

                if(start_column-1 > 0) and (end_column < end_orig_line):
                    line_list[line_nr-1] = (line[0:start_column-1] +
                                            section_content +
                                            line[end_column:end_orig_line])

                elif(start_column-1 == 0) and (end_column < end_orig_line):
                    line_list[line_nr-1] = (section_content +
                                            line[end_column:end_orig_line])

                elif(start_column-1 > 0) and (end_column == end_orig_line):
                    line_list[line_nr-1] = (line[0:start_column-1] +
                                            section_content)
                else:
                    line_list[line_nr-1] = section_content

            elif (line_nr == start_line):
                    line_list[line_nr-1] = orig_line


            elif (line_nr == end_line):
                if(end_column == len(orig_line)-1):
                    line_list[line_nr-1] = orig_line
                else:
                    line_list[line_nr-1] = (orig_line[0:end_column-1] +
                                            line[end_column-1:end_orig_line])

            else:
                line_list[line_nr-1] = orig_line
    return line_list


def beautify_line_list(line_list):
    """
    Beautify the line list.

    It add a newline character at the end of items if newline character is not
    not present and also adds a newline character if the item is only
    space. Because those line might have been either a pure line or an empty
    line.

    :param line_list: The list containing all the lines of temporary file.
    :return:          The beautified tuple containing all the lines.

    >>> line_list = ['', '\\n','asdas adasd', 'asdasdawq12\\n']
    >>> beautify_line_list(line_list)
    ('\\n', '\\n', 'asdas adasd\\n', 'asdasdawq12\\n')

    """
    for i, line in enumerate(line_list):
        if not line.strip():
            line_list[i] = '\n'
        elif line[-1] == '\n':
            continue
        else:
            line_list[i] += '\n'

    return(tuple(line_list))


def get_nl_file_dict(orig_file_path, temp_file_name, lang, parser):
    """
    Return a dictionary with `temp_file_name` as the key and the value as the
    tuple containing the lines the lines belonging to the param `lang`.

    :param orig_file_path: Path of the original nested file
    :param temp_file_name: Name of the temporary file that acts as the file
                           holder which consists of only the lines of the
                           `lang` language from the originianl nested file.
                           The temporary files  are said to be the pure
                           langauge files i.e the files that contains only one
                           programming language.
    :param lang:           Specifies the language of the line we want to extract
                           from the original file.
    :param parser:         The parser object to make nl_sections.

    Suppose we have the following file contents. And the name of file is
    `test.py`. Thie file contains both `python` and `jinja2` lines.

    >>> file_contents = ("for x in y:\\n",
    ...                  "{% if x is True %}\\n",
    ...                  "\\t{% set var3 = value3 %}\\n",
    ...                  "{% elif %}\\n",
    ...                  "\\t\\t{{ var }} = print('Bye Bye')\\n")


    The file_dict that contains only `jinja2` lines of the original files are:
    {'test.py_nl_jinja2': ('\\n',
                          '{% if x is True %}\\n',
                           '    {% set var3 = value3 %}\\n',
                           '{% elif %}\\n',
                           '        {{ var }}                   \\n')}

    The file_dict that contains only `python` lines of the original file are:
    {'test.py_nl_python': ('"for x in y:\\n',
                           '\\n',
                           '\\n',
                           '\\n',
                           "                  = print('Bye Bye')\\n")}

    """
    all_nl_sections = parser.parse(orig_file_path)
    nl_sections = get_nl_sections(all_nl_sections, lang)
    line_list = get_line_list(nl_sections, orig_file_path)
    line_tuple = beautify_line_list(line_list)
    file_dict = {temp_file_name: line_tuple}
    return file_dict
