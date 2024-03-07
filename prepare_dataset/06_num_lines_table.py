from Utils import util
from Utils import git_reader
from Utils import remove_hunks
import sqlite3
import os
import re
import sys

def count_num_line(diff_block_dict, target, commit_hash, cregit_hash, inserted_data_list):
    re_deletedLine = re.compile('^-')
    re_addedLine = re.compile('^\+')

    for f_path in diff_block_dict.keys():
        if len(diff_block_dict[f_path])==0:
            continue

        for idx, block_list in enumerate(diff_block_dict[f_path]): # for each block list corresponds to a hunk

            new_block_list = remove_hunks.replace_comment_viewrepo_show_output_for_org(block_list)

            tmp_num_add = 0
            tmp_num_del = 0
            for line in new_block_list:

                if target=="add":
                    if re_addedLine.match(line):
                        tmp_num_add += 1
                elif target=="del":
                    if re_deletedLine.match(line):
                        tmp_num_del += 1
                elif target=="both":
                    if re_addedLine.match(line):
                        tmp_num_add += 1
                    else:
                        tmp_num_del += 1
                else:
                    print("target error")
                    sys.exit()


            if target=='both':
                tmp = 'rep'
            else:
                tmp = target
            inserted_data_list.append([commit_hash, cregit_hash, f_path, idx, tmp, tmp_num_add, tmp_num_del])
            
def extract_data(p_name):

    cregit2org_hash_dict = util.load_pickle("./pickle/{0}_cregit2org_hash_dict.pickle".format(p_name))

    # micro commitsのdiffから対象となるコミットのリストを取り出す
    diff_block_dict = util.load_pickle("./pickle/diff_block_{0}.pickle".format(p_name))
    diff_block_dict = remove_hunks.remove_nodiff_hunk(diff_block_dict, p_name)
    cregit_commit_hash_list = list(diff_block_dict.keys())

    diff_block_dict = util.load_pickle("./pickle/org_diff_block_{0}.pickle".format(p_name))

    num_commit_hash = len(cregit_commit_hash_list)
    print("\n===\nstudied project: {0}".format(p_name))
    inserted_data_list = []
    for idx, cregit_commit_hash in enumerate(cregit_commit_hash_list):

        if not cregit_commit_hash in cregit2org_hash_dict:
            continue
            
        commit_hash = cregit2org_hash_dict[cregit_commit_hash]

        if (idx%1000)==0:
            print("{0}/{1:,}".format(idx, num_commit_hash))
        
        add_block_dict = diff_block_dict[commit_hash]['add']
        del_block_dict = diff_block_dict[commit_hash]['del']
        rep_block_dict = diff_block_dict[commit_hash]['rep']

        org_data_size = len(inserted_data_list)

        count_num_line(add_block_dict, "add", commit_hash, cregit_commit_hash, inserted_data_list)
        count_num_line(del_block_dict, "del", commit_hash, cregit_commit_hash, inserted_data_list)
        count_num_line(rep_block_dict, "both", commit_hash, cregit_commit_hash, inserted_data_list)

        if org_data_size==len(inserted_data_list):
            inserted_data_list.append([commit_hash, cregit_commit_hash, None, None, None, None, None])


    conn = sqlite3.connect('./db/{0}.db'.format(p_name))
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS commit_line_sizes;") 
    # [commit_hash, cregit_hash, f_path, target, tmp_num_add, tmp_num_del]
    cur.execute("CREATE TABLE commit_line_sizes(org_commit_hash_id TEXT, cregit_commit_hash_id TEXT, file_path_id TEXT, hunk_index_id INTEGER, hunk_category_id TEXT, added_lines INTEGER, deleted_lines INTEGER, PRIMARY KEY (org_commit_hash_id, file_path_id, hunk_index_id, hunk_category_id));")

    
    cur.executemany('INSERT INTO commit_line_sizes(org_commit_hash_id, cregit_commit_hash_id, file_path_id, hunk_index_id, hunk_category_id, added_lines, deleted_lines) VALUES(?,?,?,?,?,?,?)', inserted_data_list)

    conn.commit()
    conn.close()

def main():

    for p_name in ['camel', 'hadoop', 'linux', 'zephyr']:

        extract_data(p_name)
        #make_table(p_name)

if __name__=="__main__":
    main()
