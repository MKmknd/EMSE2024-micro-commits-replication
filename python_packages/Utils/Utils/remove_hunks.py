import sys
import re

re_repoview_remove = re.compile('^[\+-](begin_|comment|end_|DECL).*$')
re_emptyline_remove = re.compile('^[\+-]$')

def replace_comment_viewrepo_show_output(text):
    new_text = []
    for line in text.splitlines():
        if re_repoview_remove.match(line):
            continue
        if re_emptyline_remove.match(line):
            continue
        new_text.append(line)
    return new_text

def remove_nodiff_hunk(diff_block_dict, p_name):

    new_diff_block_dict = {}
    for commit_hash in diff_block_dict.keys():
        for category in diff_block_dict[commit_hash].keys():

            for f_name in diff_block_dict[commit_hash][category].keys():


                if len(diff_block_dict[commit_hash][category][f_name])==0:
                    continue

                temp_list = []
                for _block_list in diff_block_dict[commit_hash][category][f_name]:

                    # MASA: I can replace this to the following
                    _block_list = replace_comment_viewrepo_show_output(_block_list)
                    # this
                    #_block_list = _block_list.splitlines()
                    # HERE

                    #if len(_block_list)==0:
                    #    print("Error happend? I think we should check this point")
                    #    sys.exit()
                    #    #continue

                    # MASA: I can replace this to the following
                    #_new_block_list = []
                    #for line in _block_list:
                    #    if line=="":
                    #        print("Error3")
                    #        sys.exit()
                    #        continue
                    #    if len(line.split("|"))==1:
                    #        print("Error4")
                    #        sys.exit()
                    #        continue

                    #    _new_block_list.append(line)

                    #if len(_new_block_list)==0:
                    #    print("Error5")
                    #    sys.exit()
                    #    continue

                    #temp_list.append("\n".join(_new_block_list))
                    # this
                    temp_list.append("\n".join(_block_list))
                    # HERE
                
                assert len(temp_list)!=0, "temp list empty in remove_hunks: {0}".format(len(temp_list))
                if not commit_hash in new_diff_block_dict:
                    new_diff_block_dict[commit_hash] = {}
                if not category in new_diff_block_dict[commit_hash]:
                    new_diff_block_dict[commit_hash][category] = {}

                #new_diff_block_dict[commit_hash][category][f_name] = diff_block_dict[commit_hash][category]
                new_diff_block_dict[commit_hash][category][f_name] = temp_list

    return new_diff_block_dict


def replace_comment_viewrepo_show_output_for_org(text):
    new_text = []
    for line in text.splitlines():
        if re_emptyline_remove.match(line):
            continue
        new_text.append(line)
    return new_text

def remove_nodiff_hunk_for_org(diff_block_dict, p_name):

    new_diff_block_dict = {}
    for commit_hash in diff_block_dict.keys():
        for category in diff_block_dict[commit_hash].keys():

            for f_name in diff_block_dict[commit_hash][category].keys():

                if len(diff_block_dict[commit_hash][category][f_name])==0:
                    continue

                temp_list = []
                for _block_list in diff_block_dict[commit_hash][category][f_name]:

                    # MASA: I can replace this to the following
                    _block_list = replace_comment_viewrepo_show_output_for_org(_block_list)

                    temp_list.append("\n".join(_block_list))
                
                assert len(temp_list)!=0, "temp list empty in remove_hunks: {0}".format(len(temp_list))
                if not commit_hash in new_diff_block_dict:
                    new_diff_block_dict[commit_hash] = {}
                if not category in new_diff_block_dict[commit_hash]:
                    new_diff_block_dict[commit_hash][category] = {}

                new_diff_block_dict[commit_hash][category][f_name] = temp_list

    return new_diff_block_dict
