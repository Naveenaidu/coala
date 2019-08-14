import difflib
#from coalib.results.Result import diffs_dict

def update_nl_file_dict(nl_file_dict, orig_file_dict, diff_modified):
    patched_lines = list(set(orig_file_dict) - set(diff_modified))
    print("\n PATCHED_LINES\n", patched_lines)
    for line in patched_lines:
        index = orig_file_dict.index(line)
        print(index)
        # Check if the line is present in the patched_lines, if yes, replace
        # the original_line in nl_file_dict with it.
        try:
            print("\nReplacing nl_file_dict with patched_line\n")
            nl_file_dict[index] = diff_modified[index]
        except:
            # If it's not present, it means that the line is deleted.
            nl_file_dict.pop(index)

    return nl_file_dict

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
        # If we have only one nl_section then the condition 
        # `a_index_2 >= nl_sections[-1].end.column` checks if the a_index_2 is
        # greater than the last element. This indirectly means that the 
        # a_index_2 is outside. That's also, why this condition needs to be
        # checked before we check if the a_index_2 is between two nl_section.
        # Because if we do so, we get `index_out_of_bounds`
        elif(not a_index_2_bool and (a_index_2 >= nl_sections[-1].end.column or 
            (a_index_2 >= nl_section.end.column and  
                a_index_2 <= nl_sections[index+1].start.column)
            )):
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
        elif(not a_index_1_bool and(a_index_1 <= nl_sections[0].end.column or 
            (a_index_1 >= nl_section.end.column and  
                a_index_1 <= nl_sections[index+1].start.column) 
            )):
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
        if((a_index_1 <= nl_sections[0].end.column or 
            (nl_sections[index].start.column <= a_index_1 and 
            nl_sections[index+1].end.column >= a_index_1)) and 
            not a_index_1_bool):
            a_index_1_bool = True
            a_index_1_section = index

        # Check if a_index_2 is inside a nl_section
        # a_index_2 points to the section that is just after a_index_2
        elif((a_index_2 >= nl_sections[-1].end.column or 
            (a_index_2 >= nl_section.end.column and  
                a_index_2 <= nl_sections[index+1].start.column)) 
            and not a_index_2_bool):
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
                         b_index_2):
    """
    Add/Delete the column numbers of the linted_start and linted_end SourceRange
    objects.
    a_index_1 --> The start of the column num to delete
    a_index_2 --> The end of the column num to delete

    Remember, the nl_sections are sorted by their index.
    """

    # CASE 1: If the deletion happens before all the nl_sections of the line
    # TODO: CHECK IF THIS IS COVERED BY OTHER CASES
    if (a_index_2 < nl_sections[0].start.column):
        print("\nINSIDE DELE COL CHANGED LINE CASE 1\n")
        deletion_value = a_index_2 - a_index_1
        decrease_nl_section_columns(0, nl_sections, deletion_value)

    for section_index, nl_section in enumerate(nl_sections):
        deletion_value = a_index_2 - a_index_1

        # CASE 2:  Deletion is between two sections
        # TODO: CHECK IF THIS IS COVERED BY OTHER CASES
        if((len(nl_sections)>1) and (nl_section.end.column < a_index_1 and 
                 a_index_2 < nl_sections[section_index+1].start.column)):
            print("\nINSIDE DELE COL CHANGED LINE CASE 2\n")
            decrease_nl_section_columns(section_index+1, nl_sections, deletion_value)
  
        # Case 3: The deletion lies inside sections
        # Decrease the end column of the selected section
        # Decrease the start and end of all the corresponding nl_sections
        elif(nl_section.start.column <= a_index_1 and 
                        nl_section.end.column >= a_index_2):
            print("\nINSIDE DELE COL CHANGED LINE CASE 3\n")
            nl_section.linted_end.column -= deletion_value
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
        if(delete_case_4[0]):
            print("\nINSIDE DELE COL CHANGED LINE CASE 4\n")
            a_index_1_section = delete_case_4[1]
            a_index_2_section = delete_case_4[2]

            # Decrease the end column of the section inside which a1 is present
            # Decrease the end column to point to the column before a_index_1
            nl_sections[a_index_1_section].linted_end.column = a_index_1 - 1

            # Decrease the start and end of all the sections that comes after 
            # a_index_2, if there are no sections after if then ignore it,
            # because this case happens only when a_index_2 is at the end of 
            # last nl_section
            decrease_nl_section_columns(a_index_2_section, nl_sections, deletion_value)
            break
            
        # CASE 5: Some part of deletion is inside a nl_section and the remaining
        # part is outside. 
        # a_index_1 is outside is either in between  two nl_sections or at the 
        # very beginning of the nl_section and a_index_2 is inside a nl_section
        delete_case_5 = is_delete_section_case_5(nl_sections, a_index_1, a_index_2)
        if(delete_case_5[0]):
            print("\nINSIDE DELE COL CHANGED LINE CASE 5\n")
            a_index_1_section = delete_case_5[1]
            a_index_2_section = delete_case_5[2]

            # Increase the linted_start of the section where a_index_2 is 
            # present.
            nl_sections[a_index_2_section].linted_start.column = a_index_2

            # Decrease all the nl_sections including the section where 
            # a_index_2 is present by the deletion_value. All the sections
            # before the a_index_1 remains unaffected.
            decrease_nl_section_columns(a_index_2_section, nl_sections, deletion_value)
            break

        # CASE 6: a_index_1 and a_index_2 both are inside nl_sections
        delete_case_6 = is_delete_section_case_6(nl_sections, a_index_1, a_index_2)
        if(delete_case_6[0]):
            print("\nINSIDE DELE COL CHANGED LINE CASE 6\n")
            a_index_1_section = delete_case_6[1]
            a_index_2_section = delete_case_6[2]

            # Decrease the linted_end of the section in which a_index_1 is 
            # present.
            nl_sections[a_index_1_section].linted_end.column = a_index_1 - 1

            # Increase the linted_start of the section in which a_index_2 is 
            # present.
            nl_sections[a_index_2_section].linted_start.column = a_index_2

            # Decrease all the nl_sections including the section where 
            # a_index_2 is present by the deletion_value. All the sections
            # before the a_index_1 remains unaffected
            decrease_nl_section_columns(a_index_2_section, nl_sections, deletion_value)
            break

        # CASE 7: a_index_1 and a_index_2 are outside the nl_sections
        delete_case_7 = is_delete_section_case_7(nl_sections, a_index_1, a_index_2)
        if(delete_case_7[0]):
            print("\nINSIDE DELE COL CHANGED LINE CASE 7\n")
            decrease_nl_section_columns(a_index_2_section, nl_sections, deletion_value)
            break

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

        insertion_value = b_index_2 - b_index_1

        print("\na_index_1 :", a_index_1)
        print("\na_index_2 :", a_index_2)
        print("\nnl_section.start.column: ", nl_section.start.column)
        print("\nnl_section.end.column: ", nl_section.end.column)
        # CASE 1: Insertion is happening inside a nl_section. 
        # Inside a section include the begging and end column of the section
        if(nl_section.start.column <= a_index_1 and 
                                nl_section.end.column >= a_index_2):
            print("\nINSIDE INSERTION COL CHANGED LINE CASE 1\n")
            # Increase the linted_end of that section and increase the 
            # linted_start and linted_end of all the following sections.
            nl_section.linted_end.column += insertion_value
            increase_nl_section_columns(section_index+1, nl_sections, insertion_value)
            break

        # CASE 2: If the insertion is in between two sections
        elif( a_index_1 > nl_section.end.column and 
                    a_index_2 < nl_sections[section_index+1].start.column ):
            print("\nINSIDE INSERTION COL CHANGED LINE CASE 2\n")
            # Increase the end of the section that is right before the a_index_1
            # so as to include that into it's section.
            # Increase the linted_start and linted_end of all the other sections
            # that come after the a_index_1
            nl_section.linted_end.column += insertion_value
            increase_nl_section_columns(section_index+1, nl_sections, insertion_value)
            break

        # CASE 3: The insertion is happening ahead of all the nl_sections
        elif( a_index_1 < nl_sections[0].start.column):
            print("\nINSIDE INSERTION COL CHANGED LINE CASE 3\n")
            # Decrease the start of the 1st nl_section to include the inserted
            # elements.
            nl_sections[0].linted_start.column -= insertion_value
            increase_nl_section_columns(1, nl_sections, insertion_value)
            break

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
            print("\nINSIDE REPLACED COL CHANGED LINE CASE 1\n")
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
            print("\nINSIDE REPLACED COL CHANGED LINE CASE 2\n")
            nl_section.linted_end.column = b_index_2
            if(replaced_value > 0):
                increase_nl_section_columns(section_index+1, nl_sections, replaced_value)


def update_changed_lines(changed_lines, nl_file_dict, nl_sections, filename, 
                        all_nl_sections, modified_diff=None):
    """Update the changed lines in the nl_section"""
    for line in sorted(changed_lines):
        # Get all the nl_sections present on the line
        all_nl_sections_line = [nl_section for nl_section in all_nl_sections 
                            if nl_section.start.line == line ]
        
        # Do not update the columns if the change is happening on one of the 
        # lines of a pure nl_section. Or if we have no all_nl_section, that means
        # the lines belongs to a pure_sections. And it's not necessary to update
        # the column of a nl_section.
        # Because it doesn't matter.
        # Remember the parsing is done in  a way that, a mixed line is kept in
        # a seperate section altogether, it is not mixed with the lines of
        # pure nl_section
        if(len(all_nl_sections_line) == 1):
            return

        # Get the nl_section of the current language present on the line
        nl_sections_line = [nl_section for nl_section in all_nl_sections_line 
                            if nl_section.start.line == line ]

        print("\n NL SECTIONS on the LINE\n", nl_sections_line)
        print("\n NlResultHandler nl_file_dict \n", nl_file_dict)
        print("\n NlResultHandler modified_diff \n", modified_diff)
        orig_line = nl_file_dict[filename][line-1]
        patched_line = modified_diff[line-1]

        print("\nORIG LINE   : ", orig_line)
        print("\nPATCHED LINE: ", patched_line)
        matcher = difflib.SequenceMatcher(None, orig_line, patched_line)

        # PRint the message ---- DELETE IT - DEBUGGING
        for change_group in matcher.get_grouped_opcodes(1):
            for (tag,
                a_index_1,
                a_index_2,
                b_index_1,
                b_index_2) in change_group:
                # The column when showing the difference starts with 0,
                # The column in nl_Sections starts with 1
                a_index_1 += 1
                a_index_2 += 1
                b_index_1 += 1
                b_index_2 += 1
                print ("%7s a[%d:%d] (%s) b[%d:%d] (%s)" %
                        (tag, a_index_1, a_index_2, orig_line[a_index_1-1:a_index_2-1],
                         b_index_1, b_index_2, patched_line[b_index_1-1: b_index_2-1]))
         # PRint the message ---- DELETE IT - DEBUGGING

        for change_group in matcher.get_grouped_opcodes(1):
            for (tag,
                a_index_1,
                a_index_2,
                b_index_1,
                b_index_2) in change_group:

                # The column when showing the difference starts with 0,
                # The column in nl_Sections starts with 1
                a_index_1 += 1
                a_index_2 += 1
                b_index_1 += 1
                b_index_2 += 1
            
                if tag == 'delete':
                    update_delted_column_changed_line(nl_sections_line,
                                                      tag, 
                                                      a_index_1, 
                                                      a_index_2, 
                                                      b_index_1, 
                                                      b_index_2)

                elif tag == 'insert':
                    update_inserted_column_changed_line(nl_sections_line,
                                                        tag,
                                                        a_index_1,
                                                        a_index_2,
                                                        b_index_1,
                                                        b_index_2)

                elif tag == 'replace':
                    update_replaced_column_changed_line(nl_sections_line,
                                                        tag,
                                                        a_index_1,
                                                        a_index_2,
                                                        b_index_1,
                                                        b_index_2)

def delete_or_append_lines(lines_list, nl_sections, update_value):
    """
    Delete the deleted lines and Add the new lines.
    update_value tells us what to do.
    If the update_value is -1 it means the lines will be deleted
    If the update_values is 1 it means the lines will be added

    A particular line can be deleted or added
    """
    # TODO: Look for optimizations
    if not lines_list:
        return nl_sections
    print("\nINSIDE DELETE OR APPEND LINES\n")
    for line_to_update in sorted(lines_list):
        for index, nl_section in enumerate(nl_sections):
            # If the line to delete/add is above the current nl_section
            # then add/subtract one line from the start and end of all the
            # nl_sections that are below the line to be added/deleted.
            if nl_section.start.line > line_to_update: 
                for nl_section in nl_sections[index:]:
                    nl_section.linted_start.line += update_value
                    nl_section.linted_end.line += update_value
                break

            # If the line is present inside a section. First update the 
            # linted_end of the section. Then update the linted_start and 
            # linted_end of all the nl_sections below it
            elif (nl_section.start.line <= line_to_update and 
                                        nl_section.end.line >= line_to_update):
                nl_section.linted_end.line += update_value
                for nl_section in nl_sections[index+1:]:
                    nl_section.linted_start.line += update_value
                    nl_section.linted_end.line += update_value
                break

    return nl_sections



def update_nl_sections(result, orig_file_dict, nl_sections, all_nl_sections, filename):
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
    all_nl_sections.sort(key = lambda x: x.index)

    diff_dict = result.diffs_dict()
    diff = diff_dict[filename]
    modified_diff = diff.modified
    changed_lines, deleted_lines, added_lines = diff.get_diff_info()
    print("\ndeleted_lines: ", deleted_lines)

    # Check if it is necessary to store the value into nl_sections. Or can we
    # only call the function directly.
    nl_sections = delete_or_append_lines(deleted_lines, nl_sections, -1)
    nl_sections = delete_or_append_lines(added_lines, nl_sections, 1)
    nl_sections = update_changed_lines(changed_lines=changed_lines, 
                                       nl_file_dict=orig_file_dict, 
                                       nl_sections=nl_sections,
                                       filename=filename,
                                       modified_diff=modified_diff, 
                                       all_nl_sections=all_nl_sections)