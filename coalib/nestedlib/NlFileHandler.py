from coalib.nestedlib.parsers.PyJinjaParser import PyJinjaParser #remove - only test
from coalib.nestedlib.NlInfoExtractor import generate_arg_list #remove - only test
from coalib.io.File import File

def get_nl_sections(all_nl_sections, lang):
    """
    Get the nl_section of a particular language from all the nl_sections of the
    file. And sort the nl_section according to their index
    """
    # Get nl_section of `lang` language
    nl_sections = []
    for nl_section in all_nl_sections:
        if nl_section.language == lang:
            nl_sections.append(nl_section)

    # Sort the nl_sections according to their indices
    nl_sections = sorted(nl_sections, key = lambda nl_section: nl_section.index)
    return nl_sections

def make_nl_file_dict(orig_file_path, nl_sections, temp_file_name):
    """
    Make a dictionary 

    :param filename_list: A list of file names as strings to build
                          the file dictionary from.
    """
    file = File(orig_file_path)

    # Initialiaze a line_list with `\n`. The lenght of this list will be equal
    # to the number of lines in the actual files. Each element in this list
    # points to the line number
    line_list = []
    line_list = ['' for index in range(0,file.__len__())]
    #print(file.__len__())

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
            line = line_list[line_nr-1]

            # If the section contains only one line. 
            # This case generally happens for mixed lang line
            if (line_nr == start_line and line_nr == end_line):
                # section_content stores the part of the line that belongs to
                # the section.
                section_content = file[line_nr-1][start_column-1:end_column]

                if(start_column-1 > 0) and (end_column<len(orig_line)-1):
                    line_list[line_nr-1] = (line[0:start_column-1] + 
                        section_content + line[end_column:])

                elif(start_column-1 == 0) and (end_column<len(orig_line)-1):
                    line_list[line_nr-1] = section_content + line[end_column:]

                elif(start_column-1 > 0) and (end_column == len(orig_line)-1):
                    line_list[line_nr-1] = (line[0:start_column-1] + 
                                                section_content)
                else:
                    line_list[line_nr-1] = section_content

            elif (line_nr == start_line):
                if(start_column-1 == 0):
                    line_list[line_nr-1] = orig_line
                else:
                    line_list[line_nr-1] = (line[0:start_column-1] + 
                        orig_line[start_column-1:])

            elif (line_nr == end_line):
                if(end_column ==  len(orig_line)-1):
                    line_list[line_nr-1] = orig_line
                else:
                    line_list[line_nr-1] = (orig_line[0:end_column-1] + 
                        line[end_column-1:])

            else:
                line_list[line_nr-1] = orig_line

    print(line_list)


                




def get_nl_file_dict(orig_file_path, temp_file_name, lang, parser):
    """
    Return a dictionary with `temp_file_name` as the key and the lines of the
    `lang` present in the `original_file`
    """
    all_nl_sections = parser.parse(orig_file_path)
    nl_sections = get_nl_sections(all_nl_sections, lang)
    file_dict = make_nl_file_dict(orig_file_path, nl_sections, temp_file_name)

    return file_dict


if __name__ == '__main__':

    parser = PyJinjaParser()
    orig_file_path = 'parsers/test-setup-coala-full.jj2.test'
    temp_file_name = 'test-setup-coala-full.jj2.test_nl_python'
    lang = 'python'

    file_dict = get_nl_file_dict(orig_file_path, temp_file_name, lang, parser)




    
