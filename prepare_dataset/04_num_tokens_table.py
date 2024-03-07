from Utils import util
from Utils import remove_hunks
import sqlite3
import re
import sys

def compute_statistics(diff_block_dict, target, commit_hash, cregit_hash, inserted_data_list):
    #print(diff_block_dict)
    re_deletedLine = re.compile('^-')
    re_addedLine = re.compile('^\+')

    for f_path in diff_block_dict.keys():

        if len(diff_block_dict[f_path])==0:
            continue

        idx = 0
        for block_list in diff_block_dict[f_path]:

            new_block_list = remove_hunks.replace_comment_viewrepo_show_output(block_list)
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

            if len(new_block_list)>0:
                if target=='both':
                    tmp = 'rep'
                else:
                    tmp = target
                inserted_data_list.append([commit_hash, cregit_hash, f_path, idx, tmp, tmp_num_add, tmp_num_del])
                idx += 1



def check_others(others_block_dict, commit_hash):

    if len(others_block_dict)>0:
        tmp_cnt = 0
        for f_path in others_block_dict.keys():
            tmp_cnt += len(others_block_dict[f_path])

        if tmp_cnt > 0:
            print("commit hash: {0}".format(commit_hash))
            print(others_block_dict)
            print("others block exists")
            sys.exit()

def extract_data(p_name):

    diff_block_dict = util.load_pickle("./pickle/diff_block_{0}.pickle".format(p_name))
    diff_block_dict = remove_hunks.remove_nodiff_hunk(diff_block_dict, p_name)

    cregit2org_hash_dict = util.load_pickle("./pickle/{0}_cregit2org_hash_dict.pickle".format(p_name))


    print("\n===\nstudied project: {0}".format(p_name))
    inserted_data_list = []
    num_commit_hash = len(diff_block_dict.keys())
    for idx, commit_hash in enumerate(diff_block_dict.keys()):

        if (idx%10000)==0:
            print("{0:,}/{1:,}".format(idx, num_commit_hash))

        if not commit_hash in cregit2org_hash_dict:
            print(p_name)
            print(commit_hash)
            print('the commit does not exist')
            sys.exit()

        if 'add' in diff_block_dict[commit_hash]:
            compute_statistics(diff_block_dict[commit_hash]['add'], "add", cregit2org_hash_dict[commit_hash], commit_hash, inserted_data_list)

        if 'del' in diff_block_dict[commit_hash]:
            compute_statistics(diff_block_dict[commit_hash]['del'], "del", cregit2org_hash_dict[commit_hash], commit_hash, inserted_data_list)

        if 'rep' in diff_block_dict[commit_hash]:
            compute_statistics(diff_block_dict[commit_hash]['rep'], "both", cregit2org_hash_dict[commit_hash], commit_hash, inserted_data_list)

        if 'others' in diff_block_dict[commit_hash]:
            check_others(diff_block_dict[commit_hash]['others'], commit_hash)


    conn = sqlite3.connect('./db/{0}.db'.format(p_name))
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS commit_token_sizes;") 
    # [commit_hash, cregit_hash, f_path, target, tmp_num_add, tmp_num_del]
    cur.execute("CREATE TABLE commit_token_sizes(org_commit_hash_id TEXT, cregit_commit_hash_id TEXT, file_path_id TEXT, hunk_index_id INTEGER, hunk_category_id TEXT, added_tokens INTEGER, deleted_tokens INTEGER, PRIMARY KEY (org_commit_hash_id, file_path_id, hunk_index_id, hunk_category_id));")

    
    cur.executemany('INSERT INTO commit_token_sizes(org_commit_hash_id, cregit_commit_hash_id, file_path_id, hunk_index_id, hunk_category_id, added_tokens, deleted_tokens) VALUES(?,?,?,?,?,?,?)', inserted_data_list)

    conn.commit()
    conn.close()


def main():

    for p_name in ['camel', 'hadoop', 'linux', 'zephyr']:

        extract_data(p_name)
        #make_table(p_name)

if __name__=="__main__":
    main()
