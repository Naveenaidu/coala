import difflib
from coalib.results.Diff import diffs_dict

def get_line(nl_file_dict, file_name, line): # might be unnecessary
	return nl_file_dict[file_name][line]

def update_changed_lines(changed_lines, nl_file_dict, nl_section):
	"""Update the changed lines in the nl_section"""
	pass

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
			# then add/subtract the one line from the start and end of all the
			# nl_sections that are below the line to be added/deleted.
			if nl_section.start.line > line_to_update: 
				for nl_section in nl_sections[index:]:
					nl_section.linted_start.line += update_value
					nl_section.linted_end.line += update_value

			# If the line is present inside a section. First update the 
			# linted_end of the line. Then update the linted_start and 
			# linted_end of all the nl_sections below it
			elif (nl_section.start.line < line_to_update and 
										nl_section.end.line > line_to_update):
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
    nl_sections = delete_and_append_lines(deleted_lines, nl_sections, 1)
    nl_sections = delete_and_append_lines(added_lines, nl_sections, -1)
    nl_sections = update_changed_lines(changed_lines, nl_file_dict, nl_sections)  
	pass

if __name__ == '__main__':
	
