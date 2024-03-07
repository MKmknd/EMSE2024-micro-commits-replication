from Utils import git_reader
from Utils import util
import sys
import re


def is_meaningful_file(name, e_list=['java', 'c', 'h']):
    """
    Check whether this file is a source code file

    :param name: a file name
    :param e_list: a list of extensions
    :return: binary (is source code or is not source code)
    """
    for extention in e_list:
        if re.search('\.{}$'.format(extention), name):
            return True
    return False

def find_filehash(module_info):
    for line in module_info.splitlines():
        try:
            if 'index' in line:
                match = re.search('index[\s]([\w]+)\.\.([\w]+)[\s]?', line)
                prev_hash = match.group(1)
                curr_hash = match.group(2)
                return prev_hash, curr_hash
        except Exception:
            print(line)
    exit('Error: index should exist')


def find_moduleName(module):
    """
    Extract file name (after changed)
    """
    re_moduleName = re.compile('^\+\+\+[\s]b?/(.+)$')
    for line in module.splitlines():
        match = re_moduleName.match(line)
        if match:
            return match.group(1)
    raise

def find_moduleName_before(module):
    """
    Extract file name (before changed)
    """
    re_moduleName = re.compile('^\-\-\-[\s]a?/(.+)$')
    for line in module.splitlines():
        match = re_moduleName.match(line)
        if match:
            return match.group(1)
    raise


def split_diff_bymodule(git_show):
    """
    Extract diff information
    """
    modulediff_list = []
    modules = re.split('\ndiff[\s]--git[\s]a/.+\n', git_show) # split a patch (output by git show) into two parts.
    del(modules[0])  # Remove the first part that is a commit message and above
    for module in modules:
        try:
            module_name = find_moduleName(module)
            module_name_before = find_moduleName_before(module)
        except Exception:
            # If the change is only change the modulename, we ignore the change
            # Example: old mode 100755 new mode 100644
            # If we want to remedy this problem, we can use "git config core.filemode false" in git config
            # print('module name is not found.', file=sys.stderr)
            # print("[MODULE]\n" + module + "\n", file=sys.stderr)
            continue
        if not is_meaningful_file(module_name):  # Check extentions
            continue
        module_info, module_diff = re.split('\n\+\+\+[\s]b/.+\n', module)
        prev_hash, curr_hash = find_filehash(module_info)
        modulediff_list.append([module_name, prev_hash, curr_hash, module_diff, module_name_before])

    return modulediff_list


def insert_block_to_list(add_block_list, del_block_list, rep_block_list, others_block_list, type_str, block):
    re_add_block = re.compile('^\++$')
    re_del_block = re.compile('^-+$')
    re_rep_block = re.compile('^-+\++$')

    if re_add_block.match(type_str):
        add_block_list.append(block)
    elif re_del_block.match(type_str):
        del_block_list.append(block)
    elif re_rep_block.match(type_str):
        rep_block_list.append(block)
    else:
        others_block_list.append(block)

def split_diff_blocks(module_diff):
    re_lineInfo = re.compile('^@@[\s]-(\d+).+\+(\d+)')
    re_deletedLine = re.compile('^-')
    re_addedLine = re.compile('^\+')

    re_emptyline_remove = re.compile('^[\+-]$')
    re_repoview_remove = re.compile('^[\+-]\s*$')
    re_comment1_remove = re.compile('//.*')
    re_comment2_remove = re.compile('/\*.*\*/')
    re_comment3_remove = re.compile('/\*.*')
    re_comment4_remove = re.compile('\s*\*.*')
    re_comment5_remove = re.compile('.*\*/')

    add_block_list = []
    del_block_list = []
    rep_block_list = []
    others_block_list = []
    type_str = ""
    block = []

    for line in module_diff.splitlines():

        match = re_lineInfo.match(line)
        if match:
            if len(block)!=0:
                insert_block_to_list(add_block_list, del_block_list,
                                     rep_block_list, others_block_list,
                                     type_str, "\n".join(block))

            type_str = ""
            block = []
            continue
        if '\ No newline at end of file' == line:
            continue  # for no newline

        if re_emptyline_remove.match(line):
            continue
        line = re.sub(re_comment1_remove, "", line)
        line = re.sub(re_comment2_remove, "", line)
        line = re.sub(re_comment3_remove, "", line)
        line = re.sub(re_comment4_remove, "", line)
        line = re.sub(re_comment5_remove, "", line)

        if re_repoview_remove.match(line):
            continue

        if line=="":
            continue
        #if len(line.split("|"))==1:
        #    continue

        if re_deletedLine.match(line):
            type_str = type_str + "-"
        elif re_addedLine.match(line):
            type_str = type_str + "+"
        else:
            print("Error happened")
            continue

        block.append(line)

    if len(block)!=0:
        insert_block_to_list(add_block_list, del_block_list,
                             rep_block_list, others_block_list,
                             type_str, "\n".join(block))

    return add_block_list, del_block_list, rep_block_list, others_block_list


def classify_diff_blocks(repo_dir, commit_hash, p_name):
    """
    Return all diff blocks for each modified type (add, delete, replace, and others)
    Each of the blocks are collected for each modified file

    :param repo_dir: the path of the target reposiotry
    :param commit_hash: the target commit hash
    :return:
    add_block_dict: a dictionary of all diff blocks
    The key is a file name; the value is a list of all added blocks
    deleted_block_dict etc. are the same.
    """

    add_block_dict = {}
    del_block_dict = {}
    rep_block_dict = {}
    others_block_dict = {}
    for module_data in split_diff_bymodule(git_reader.git_show_with_context(repo_dir, commit_hash, 0)):
        module_name, prev_hash, curr_hash, module_diff, module_name_before = module_data

        if module_name in add_block_dict:
            print("Duplicated key error")
            sys.exit()

        extension = module_name.split(".")[-1]
        if p_name in set(['linux', 'zephyr']):
            if not extension in set(["c","h"]):
                continue
        else:
            if extension!="java":
                continue

        add_block_dict[module_name], del_block_dict[module_name],\
        rep_block_dict[module_name], others_block_dict[module_name] = \
            split_diff_blocks(module_diff)

    return add_block_dict, del_block_dict, rep_block_dict, others_block_dict


if __name__=="__main__":

    for p_name in ['camel', 'hadoop', 'linux', 'zephyr']:

        repo_dir = "./repository/{0}"

        print("\n===\nstudied project: {0}".format(p_name))
        data_dict = {}

        for idx, commit_hash in enumerate(git_reader.get_all_hash(repo_dir.format(p_name))):

            if (idx%1000)==0:
                print("{0}, idx: :{1:,}".format(p_name, idx))
            add_block_dict, del_block_dict, rep_block_dict, others_block_dict = \
                classify_diff_blocks(repo_dir.format(p_name), commit_hash, p_name)


            data_dict[commit_hash] = {"add": add_block_dict, "del": del_block_dict,
                                      "rep": rep_block_dict, "others": others_block_dict}


        util.dump_pickle("./pickle/org_diff_block_{0}.pickle".format(p_name), data_dict)
