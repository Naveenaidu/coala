import difflib
from coalib.results.Diff import diffs_dict

def get_line(nl_file_dict, file_name, line): # might be unnecessary
    return nl_file_dict[file_name][line]

def decrease_nl_section_columns(section_index, nl_sections, deletion_value):
    """
    Decreases the column number of linted_start and linted_end off all the 
    nl_section from the section_index to the last element in nl_sections. 
    """
    if(any(nl_sections[section_index:])):

                for nl_section in nl_sections[a_index_2:]:
                    nl_section.linted_start.column -= deletion_value
                    nl_section.linted_end.column -= deletion_value
    return nl_sections

def increase_nl_section_columns(section_index, nl_sections, insertion_value):
    """
    Increases the column number of linted_start and linted_end off all the 
    nl_section from the section_index to the last element in nl_sections.
    """
    if any(nl_sections[section_index:]):
        for nl_section in nl_sections[section_index+1:]:
            nl_section.linted_start.column += insertion_value
            nl_section.linted_end.column += insertion_value

def is_delete_section_case_4(nl_sections, a_index_1, a_index_2):
    """
    Case 4: Some part of deletion is inside a nl_section and the remaining
    part is outside.

    a_index_1 is inside a nl_section and a_index_2 is either in between two
    nl_sections or at the very end

    a_index_1_bool tells us if the index of a1 is present inside a section.
    Inside of the section includes the start and the end of the section.

    a_index_2_bool tells if the index of a2 is present in between two sections
    or at the end of sections

    a_index_1_section --> The section in which a_index_1 is present
    a_index_2_section --> The next closest section to a_index_2
    """
    a_index_1_bool = False
    a_index_2_bool = False
    a_index_1_section = None
    a_index_2_section = None

    for index, nl_section in enumerate(nl_sections):
        # Check for a_index_1
        if(nl_section.start.column <= a_index_1 and 
            nl_section.end.column >= a_index_1 and not a_index_1_bool):
            a_index_1_bool = True
            a_index_1_section = index

        # Check for a_index_2
        elif(not a_index_2_bool and 
            (a_index_2 >= nl_section.end.column and  
                a_index_2 <= nl_sections[index+1].start.column) and 
            a_index_2 >= nl_sections[-1].end.column):
            a_index_2_bool = True
            a_index_2_section = index+1

        # Check if the section lie between a_index_1 and a_index_2. If it does
        # mark that section as deleted.
        elif(nl_section.start.column >= a_index_1 and 
                                    nl_section.end.column <= a_index_2):
            nl_sections[index].delete_section = True

    return ((a_index_1_bool and a_index_2_bool), 
            a_index_1_section, 
            a_index_2_section)

def is_delete_section_case_5(nl_sections, a_index_1, a_index_2):
    """
    Case 5: Some part of deletion is inside a nl_section and the remaining
    part is outside.

    a_index_1 is inside a nl_section and a_index_2 is either in between two
    nl_sections or at the very end

    a_index_1_bool tells us if the index of a1 is present inside a section
    a_index_2_bool tells if the index of a2 is present in between two sections
    or at the end of sections.Inside of the section includes the start and the 
    end of the section.

    a_index_1_section --> The section just before a_index_1
    a_index_2_section --> The section in which a_index_2 is present
    """
    a_index_1_bool = False
    a_index_2_bool = False
    a_index_1_section = None
    a_index_2_section = None

    for index, nl_section in enumerate(nl_sections):
        # Check for a_index_2
        if((nl_section.start.column <= a_index_2 and 
            nl_section.end.column >= a_index_2) and not a_index_2_bool):
            a_index_2_bool = True
            a_index_2_section = index

        # Check for a_index_1
        elif(not a_index_1_bool and 
            (a_index_1 >= nl_section.end.column and  
                a_index_1 <= nl_sections[index+1].start.column) and 
            a_index_1 <= nl_sections[0].end.column):
            a_index_1_bool = True
            a_index_1_section = index - 1

        # Check if the section lie between a_index_1 and a_index_2. If it does
        # mark that section as deleted.
        elif(nl_section.start.column >= a_index_1 and 
                                    nl_section.end.column <= a_index_2):
            nl_sections[index].delete_section = True

    return ((a_index_1_bool and a_index_2_bool), 
            a_index_1_section, 
            a_index_2_section)
def is_delete_section_case_6(nl_sections, a_index_1, a_index_2):
    """
    CASE 6: a_index_1 and a_index_2 both are inside nl_sections.

    a_index_1_bool tells if the index of a1 is present in between two sections
    or at the end of sections.Inside of the section includes the start and the 
    end of the section.
    a_index_2_bool tells if the index of a2 is present in between two sections
    or at the end of sections.Inside of the section includes the start and the 
    end of the section.

    a_index_1_section --> The section in which a_index_1 is present
    a_index_2_section --> The section in which a_index_2 is present
    """
    a_index_1_bool = False
    a_index_2_bool = False
    a_index_1_section = None
    a_index_2_section = None

    for index, nl_section in enumerate(nl_sections):

        # Check for a_index_1
        if((nl_section.start.column <= a_index_1 and 
            nl_section.end.column >= a_index_1) and not a_index_1_bool):
            a_index_1_bool = True
            a_index_1_section = index

        # Check for a_index_2
        elif((nl_section.start.column <= a_index_2 and 
            nl_section.end.column >= a_index_2 )and not a_index_2_bool):
            a_index_2_bool = True
            a_index_2_section = index

        elif(nl_section.start.column >= a_index_1 and 
                                    nl_section.end.column <= a_index_2):
            nl_sections[index].delete_section = True

    return ((a_index_1_bool and a_index_2_bool), 
            a_index_1_section, 
            a_index_2_section)

def is_delete_section_case_7(nl_sections, a_index_1, a_index_2):
    """
    CASE 7: a_index_1 and a_index_2 are outside the nl_sections.
    """
    a_index_1_bool = False
    a_index_2_bool = False
    a_index_1_section = None
    a_index_2_section = None

    for index, nl_section in enumerate(nl_sections):
        # Check if a_index_1 is inside a nl_section
        if(nl_sections[index].start.column <= a_index_1 and 
            nl_sections[index+1].end.column >= a_index_1 and not a_index_1_bool):
            a_index_1_bool = True
            a_index_1_section = index

        # Check if a_index_2 is inside a nl_section
        # a_index_2 points to the section that is just after a_index_2
        elif(nl_sections[index].start.column <= a_index_2 and 
            nl_sections[index+1].end.column >= a_index_2 and not a_index_2_bool):
            a_index_2_bool = True
            a_index_2_section = index + 1

        # Check if a section is present between a_index_1 and a_index_2
        elif(nl_section.start.column >= a_index_1 and 
                                    nl_section.end.column <= a_index_2):
            nl_sections[index].delete_section = True

    return ((a_index_1_bool and a_index_2_bool), 
            a_index_1_section, 
            a_index_2_section)

def update_delted_column_changed_line(nl_sections,
                         tag, 
                         a_index_1, 
                         a_index_2, 
                         b_index_1, 
                         b_index2):
    """
    Add/Delete the column numbers of the linted_start and linted_end SourceRange
    objects.
    a_index_1 --> The start of the column num to delete
    a_index_2 --> The end of the column num to delete
    """
    # CASE 1: If the deletion happens before all the nl_sections of the line
    # TODO: CHECK IF THIS IS COVERED BY OTHER CASES
    if all(a_index_2 < nl_section.start.column  for nl_section in nl_sections):
        deletion_value = a_index_2 - a_index_1
        decrease_nl_section_columns(0, nl_sections, deletion_value)

    
    for section_index, nl_section in enumerate(nl_sections):
        delete_value = a_index_2 - a_index_1

        # CASE 2:  Deletion is between two sections
        # TODO: CHECK IF THIS IS COVERED BY OTHER CASES
        if(nl_section.end.column < a_index_1 and 
                nl_sections[section_index+1].start.column > a_index_2 and 
                 len(nl_sections)>1):
            decrease_nl_section_columns(section_index+1, nl_sections, deletion_value)
  

        # Case 3: The deletion lies in between the sections
        # Decrease the end column of the selected section
        # Decrease the start and end of all the corresponding nl_sections
        elif(nl_section.start.column <= a_index_1 and 
                        nl_section.end.column >= a_index_2):
            nl_section.linted_end.column -= delete_value
            decrease_nl_section_columns(section_index+1, nl_sections, deletion_value)

        # CASE 4: Some part of deletion is inside a nl_section and the remaining
        # part is outside.

        # a_index_1 is inside a nl_section and a_index_2 is either in between 
        # two nl_sections or at the very end

        # TODO: Make Graphical representation for better clarity
        # In is_delete_section_case_4, we have already marked the section that
        # are inside the a_index_1 and a_index_2 as deleted. We just have to 
        # change the linted_start.column and linted_end.column values.
        delete_case_4  = is_delete_section_case_4(nl_sections, a_index_1, a_index_2)
        if (delete_case_4[0]):
            a_index_1_section = delete_case_4[1]
            a_index_2_section = delete_case_4[2]

            # Decrease the end column of the section inside which a1 is present
            nl_sections[a_index_1_section].linted_end.column = a_index_1

            # Decrease the start and end of all the sections that comes after 
            # a_index_2, if there are no sections after if then ignore it,
            # because this case happens only when a_index_2 is at the end of 
            # last nl_section
            decrease_nl_section_columns(a_index_2_section, nl_sections, deletion_value)
            
        # CASE 5: Some part of deletion is inside a nl_section and the remaining
        # part is outside. 
        # a_index_1 is outside is either in between  two nl_sections or at the 
        # very beginning of the nl_section and a_index_2 is inside a nl_section
        delete_case_5 = is_delete_section_case_5(nl_sections, a_index_1, a_index_2)
        if(delete_case_5[0]):
            a_index_1_section = delete_case_5[1]
            a_index_2_section = delete_case_5[2]

            # Increase the linted_start of the section where a_index_2 is 
            # present.
            nl_sections[a_index_2_section].linted_start.column = a_index_2

            # Decrease all the nl_sections including the section where 
            # a_index_2 is present by the deletion_value. All the sections
            # before the a_index_1 remains unaffected.
            decrease_nl_section_columns(a_index_2_section, nl_sections, deletion_value)

        # CASE 6: a_index_1 and a_index_2 both are inside nl_sections
        delete_case_6 = is_delete_section_case_6(nl_sections, a_index_1, a_index_2)
        if(delete_case_6[0]):
            a_index_1_section = delete_case_6[1]
            a_index_2_section = delete_case_6[2]

            # Decrease the linted_end of the section in which a_index_1 is 
            # present.
            nl_sections[a_index_1_section].linted_end.column = a_index_1

            # Increase the linted_start of the section in which a_index_2 is 
            # present.
            nl_sections[a_index_2_section].linted_start.column = a_index_2

            # Decrease all the nl_sections including the section where 
            # a_index_2 is present by the deletion_value. All the sections
            # before the a_index_1 remains unaffected
            decrease_nl_section_columns(a_index_2_section, nl_sections, deletion_value)

        # CASE 7: a_index_1 and a_index_2 are outside the nl_sections
        delete_case_7 = is_delete_section_case_7(nl_sections, a_index_1, a_index_2)
        if(delete_case7[0]):
            decrease_nl_section_columns(a_index_2_section, nl_sections, deletion_value)

def update_inserted_column_changed_line(nl_sections,
                                        tag,
                                        a_index_1,
                                        a_index_2,
                                        b_index_1,
                                        b_index_2):
    """
    Update the column of the linted_end and linted_start of the nl_sections when
    a patch is inserted in the line.

    a_index_1 --> Column before which the insertion needs to happen.
    For eg: If a_index_1 is 2, it means that the insertion is happening before
    the column 2 of the original line.

    Note that for `insert`, a_index_1 == a_index_2 
    """

    for section_index, nl_section in enumerate(nl_sections):

        insertion_value = b_index2 - b_index_1

        # CASE 1: Insertion is happening inside a nl_section. 
        # Inside a section include the begging and end column of the section
        if(nl_section.start.column <= a_index_1 and 
                                nl_section.end.column >= a_index_1):

            # Increase the linted_end of that section and increase the 
            # linted_start and linted_end of all the following sections.
            nl_section.linted_end.column += insertion_value
            increase_nl_section_columns(section_index+1, nl_sections, insertion_value)

        # CASE 2: If the insertion is in between two sections
        elif( a_index_1 > nl_section.end.column and 
                    a_index_2 < nl_sections[index+1].start.column ):

            # Increase the end of the section that is right before the a_index_1
            # so as to include that into it's section.
            # Increase the linted_start and linted_end of all the other sections
            # that come after the a_index_1
            nl_section.linted_end.column = b_index_2
            increase_nl_section_columns(section_index+1, nl_sections, insertion_value)

        # CASE 3: The insertion is happening ahead of all the nl_sections
        elif( a_index_1 < nl_sections[0].start.column):

            # Decrease the start of the 1st nl_section to include the inserted
            # elements.
            nl_sections[0].linted_start.column -= insertion_value
            increase_nl_section_columns(1, nl_sections, insertion_value)

def update_replaced_column_changed_line(nl_sections,
                                        tag,
                                        a_index_1,
                                        a_index_2,
                                        b_index_1,
                                        b_index_2):

    """
    Update the column of the linted_end and linted_start of the nl_sections when
    some text is replaced with another.
    """
    replaced_value = (b_index_2 - b_index_1) - (a_index_2 - a_index_1)
    for section_index, nl_section in enumerate(nl_sections):

        # CASE 1: If the characters are being replaced and no other new char
        # is added then do nothing.
        # Else increase the linted_end of that section and increase the 
        # linted_start and linted_end of all other sections after it.
        if(a_index_1 >= nl_section.start.column 
                                and a_index_1 <= nl_section.end.column):
            if ( replaced_value == 0):
                continue

            else:
                nl_section.linted_end.colmun += replaced_value
                increase_nl_section_columns(section_index+1, nl_sections, replaced_value)

        # CASE 2: replacing takes place outside the nl_sections.
        # If this replacing does not insert any new characters, then do not
        # update the linted_start and linted_end of the other nl_sections, else
        # update them

        elif(a_index_1 > nl_section.end.column and 
                        a_index_2 < nl_sections[section_index+1].start.column):

            nl_section.linted_end.column = b_index_2
            if(replaced_value > 0):
                increase_nl_section_columns(section_index+1, nl_sections, replaced_value)


def update_changed_lines(changed_lines, nl_file_dict, nl_section):
    """Update the changed lines in the nl_section"""
    for line in sorted(lines_list):
        # Get all the nl_sections present on the line
        all_nl_sections = [nl_section for nl_section in nl_sections 
                            if nl_section.start.line == line ]
        orig_line = nl_file_dict[filename][line]
        patched_line = modified_diff[line]
        matcher = difflib.SequenceMatcher(None, orig_line, patched_line)
        for change_group in matcher.get_grouped_opcodes(1):
            for (tag,
                a_index_1,
                a_index_2,
                b_index_1,
                b_index_2) in change_group:

                if tag == 'delete':
                    update_delted_column_changed_line(nl_sections,
                                                      tag, 
                                                      a_index_1, 
                                                      a_index_2, 
                                                      b_index_1, 
                                                      b_index_2)

                elif tag == 'insert':
                    update_inserted_column_changed_line(nl_sections,
                                                        tag,
                                                        a_index_1,
                                                        a_index_2,
                                                        b_index_1,
                                                        b_index_2)

                elif tag == 'replace':
                    update_replaced_column_changed_line(nl_sections,
                                                        tag,
                                                        a_index_1,
                                                        a_index_2,
                                                        b_index_1,
                                                        b_index_2)

def delete_and_append_lines(lines_list, nl_sections, update_value):
    """
    Delete the deleted lines and Add the new lines.
    update_value tells us what to do.
    If the update_value is -1 it means the lines will be deleted
    If the update_values is 1 it means the lines will be added

    A particular line can be deleted or added
    """
    # TODO: Look for optimizations
    for line_to_update in sorted(lines_list):
        for index, nl_section in enumerate(nl_sections):
            # If the line to delete/add is above the current nl_section
            # then add/subtract one line from the start and end of all the
            # nl_sections that are below the line to be added/deleted.
            if nl_section.start.line > line_to_update: 
                for nl_section in nl_sections[index:]:
                    nl_section.linted_start.line += update_value
                    nl_section.linted_end.line += update_value

            # If the line is present inside a section. First update the 
            # linted_end of the section. Then update the linted_start and 
            # linted_end of all the nl_sections below it
            elif (nl_section.start.line <= line_to_update and 
                                        nl_section.end.line >= line_to_update):
                nl_section.linted_end.line += update_value
                for nl_section in nl_sections[index+1:]:
                    nl_section.linted_start.line += update_value
                    nl_section.linted_end.line += update_value

    return nl_sections



def update_nl_section(result, nl_file_dict, nl_sections):
    """
    :param nl_section: The nl_section of the language of which the file is made.
    For eg: If the file being linted is a temp_jinja file then nl_sections
    contains the nl_sections of jinja language. 

    Update the NlSection information based on the patches the user chooses to
    apply.

    Get the diff info from the `get_diff_info` from result.diff, use this info
    to find what files are being `changed`, `deleted` and `added` when the 
    patch is going to be applied.

    Fetch those lines from the nl_file_dict, compare them with the patch
    provided by bear. use difflib to compare. And then on the basis of the 
    tags of the difflib, update the start and end of the NlSection.

    Note: The reason we are updating the nl_section is because, it'll help in
    extracting the nl_sections from the nl_section_map from each of the 
    segregated file, when the patches are applied.

    The updated_nl_sections tells us the information about what part of text
    to extract from the temp_file_dict. This information would be useful while
    assembling.
    """
    nl_sections.sort(key = lambda x: x.index)
    diff_dict = result.diffs_dict()
    diff = diff_dict[filename]
    modified_diff = diff.modified()
    changed_lines, deleted_lines, added_lines = diff.get_diff_info()

    # Check if it is necessary to store the value into nl_sections. Or can we
    # only call the function directly.
    nl_sections = delete_and_append_lines(deleted_lines, nl_sections, -1)
    nl_sections = delete_and_append_lines(added_lines, nl_sections, 1)
    nl_sections = update_changed_lines(changed_lines, nl_file_dict, nl_sections)  
    pass

    
