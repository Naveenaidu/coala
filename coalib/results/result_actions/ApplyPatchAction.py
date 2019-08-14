import shutil
from os.path import isfile
from os import remove

from coala_utils.FileUtils import detect_encoding

from coalib.results.result_actions.ShowPatchAction import ShowPatchAction
from coalib.results.result_actions.ResultAction import ResultAction

from coalib.nestedlib.NlResultHandler import update_nl_sections, update_nl_file_dict


class ApplyPatchAction(ResultAction):

    SUCCESS_MESSAGE = 'Patch applied successfully.'

    is_applicable = staticmethod(ShowPatchAction.is_applicable)

    def apply(self,
              result,
              original_file_dict,
              file_diff_dict,
              nl_sections=None,
              all_nl_sections=None,
              nl_file_dict=None,
              no_orig: bool = False):
        """
        (A)pply patch

        :param no_orig: Whether or not to create .orig backup files
        """
        
        for filename in result.diffs:
            pre_patch_filename = filename
            print("\n FILENAME \n", filename)
            if filename in file_diff_dict:
                diff = file_diff_dict[filename]
                pre_patch_filename = (diff.rename
                                      if diff.rename is not False
                                      else filename)
                file_diff_dict[filename] += result.diffs[filename]
            else:
                file_diff_dict[filename] = result.diffs[filename]

                # Backup original file, only if there was no previous patch
                # from this run though!
                if not no_orig and isfile(pre_patch_filename):
                    shutil.copy2(pre_patch_filename,
                                 pre_patch_filename + '.orig')

            diff = file_diff_dict[filename]
            print("\n DIFF \n",diff)

            if not diff.delete:
                new_filename = (diff.rename
                                if diff.rename is not False
                                else filename)

                # Write to the original file only when we run coala in normal 
                # mode
                if not nl_sections:
                  with open(new_filename, mode='w',
                            encoding=detect_encoding(pre_patch_filename)) as file:
                      file.writelines(diff.modified)
                else:
                  print("*"*60)
                  print("\n     UPDATING NL SECTIONS      \n")
                  
                  update_nl_sections(result=result, 
                                     filename=filename, 
                                     orig_file_dict=original_file_dict, 
                                     nl_sections=nl_sections,
                                     all_nl_sections=all_nl_sections)
                  update_nl_file_dict(nl_file_dict[filename], 
                                      original_file_dict[filename], diff.modified)
                  print(nl_file_dict)

            if diff.delete or diff.rename:
                if diff.rename != pre_patch_filename and isfile(
                        pre_patch_filename):
                    remove(pre_patch_filename)
        print(file_diff_dict)
        return file_diff_dict, nl_file_dict
