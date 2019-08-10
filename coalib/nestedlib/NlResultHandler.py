import difflib
from coalib.results.Diff import diffs_dict

def get_line(nl_file_dict, file_name, line): # might be unnecessary
	return nl_file_dict[file_name][line]

def update_changed_lines(changed_lines, nl_file_dict, nl_section):
	"""Update the changed lines in the nl_section"""
	pass

def remove_deleted_lines(deleted_lines, nl_file_dict, nl_section):
	"""Remove the deleted lines from nl_section"""
	pass

def add_new_lines(added_lines, nl_file_dict, nl_section):
	"""Add new lines in nl_section"""
	pass


def update_nl_section(result, nl_file_dict, nl_section):
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
	diff_dict = result.diffs_dict()
    diff = diff_dict[filename]
    modified_diff = diff.modified()
    changed_lines, deleted_lines, added_lines = diff.get_diff_info()
    update_changed_lines(changed_lines, nl_file_dict, nl_section)
    remove_deleted_lines(deleted_lines, nl_file_dict, nl_section)
    add_new_lines(added_lines, nl_file_dict, nl_section)  
	pass

if __name__ == '__main__':
	
