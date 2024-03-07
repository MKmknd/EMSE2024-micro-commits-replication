from Utils import util
from Utils import remove_hunks
import sqlite3
import re
import sys

# changed_tokens(org_commit_hash_id TEXT, hunk_id INTEGER, token_id INTEGER, operation TEXT, token TEXT, token_type TEXT, PRIMARY KEY (org_commit_hash_id, hunk_id, token_id)) 
def compute_statistics(diff_block_dict, hunk_idx, commit_hash, target, inserted_data_list, inserted_data_list_hunk):
    #print(diff_block_dict)
    re_deletedLine = re.compile('^-')
    re_addedLine = re.compile('^\+')

    for f_path in diff_block_dict.keys():

        if len(diff_block_dict[f_path])==0:
            continue

        for block_list in diff_block_dict[f_path]:

            new_block_list = remove_hunks.replace_comment_viewrepo_show_output(block_list)
            for token_idx, line in enumerate(new_block_list):

                if re_addedLine.match(line):
                    operation = '+'
                    token_type = re.sub("^\+", "", line.split("|")[0])
                    token = "|".join(line.split("|")[1:])
                elif re_deletedLine.match(line):
                    operation = '-'
                    token_type = re.sub("^-", "", line.split("|")[0])
                    token = "|".join(line.split("|")[1:])
                else:
                    print("target error")
                    sys.exit()

                inserted_data_list.append([commit_hash, hunk_idx, token_idx, operation, token, token_type])

            inserted_data_list_hunk.append([commit_hash, hunk_idx, target])
            hunk_idx += 1

    return hunk_idx


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

def extract_micro_commit_hashes(p_name):
    conn = sqlite3.connect('./db/{0}.db'.format(p_name))
    cur = conn.cursor()
    # [commit_hash, cregit_hash, f_path, target, tmp_num_add, tmp_num_del]
    cur.execute("SELECT org_commit_hash_id, cregit_commit_hash_id FROM micro_commits;")

    commit_hash_list = []
    for row in cur.fetchall():
        commit_hash_list.append(row)
    
    conn.commit()
    conn.close()

    return commit_hash_list

def extract_data(p_name):

    diff_block_dict = util.load_pickle("./../prepare_dataset/pickle/diff_block_{0}.pickle".format(p_name))
    diff_block_dict = remove_hunks.remove_nodiff_hunk(diff_block_dict, p_name)

    micro_commit_hash_list = extract_micro_commit_hashes(p_name)

    print("\n===\nstudied project: {0}".format(p_name))
    inserted_data_list = []
    inserted_data_list_hunk = []
    num_commit_hash = len(micro_commit_hash_list)
    for idx, commit_hash_pair in enumerate(micro_commit_hash_list):
        commit_hash = commit_hash_pair[1] # extract cregit hash
        hunk_idx = 0

        if (idx%10000)==0:
            print("{0:,}/{1:,}".format(idx, num_commit_hash))

        if 'add' in diff_block_dict[commit_hash]:
            hunk_idx = compute_statistics(diff_block_dict[commit_hash]['add'], hunk_idx, commit_hash_pair[0], 'add', inserted_data_list, inserted_data_list_hunk)

        if 'del' in diff_block_dict[commit_hash]:
            hunk_idx = compute_statistics(diff_block_dict[commit_hash]['del'], hunk_idx, commit_hash_pair[0], 'del', inserted_data_list, inserted_data_list_hunk)

        if 'rep' in diff_block_dict[commit_hash]:
            hunk_idx = compute_statistics(diff_block_dict[commit_hash]['rep'], hunk_idx, commit_hash_pair[0], 'rep', inserted_data_list, inserted_data_list_hunk)

        if 'others' in diff_block_dict[commit_hash]:
            check_others(diff_block_dict[commit_hash]['others'], commit_hash)
    

    conn = sqlite3.connect('./db/{0}.db'.format(p_name))
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS changed_tokens;") 
    cur.execute("DROP TABLE IF EXISTS changed_hunk_types;") 

    cur.execute("CREATE TABLE changed_tokens(org_commit_hash_id TEXT, hunk_id INTEGER, token_id INTEGER, operation TEXT, token TEXT, token_type TEXT, PRIMARY KEY (org_commit_hash_id, hunk_id, token_id));")
    cur.execute("CREATE TABLE changed_hunk_types(org_commit_hash_id TEXT, hunk_id INTEGER, hunk_type TEXT, PRIMARY KEY (org_commit_hash_id, hunk_id));")

    cur.executemany('INSERT INTO changed_tokens(org_commit_hash_id, hunk_id, token_id, operation, token, token_type) VALUES(?,?,?,?,?,?)', inserted_data_list)
    cur.executemany('INSERT INTO changed_hunk_types(org_commit_hash_id, hunk_id, hunk_type) VALUES(?,?,?)', inserted_data_list_hunk)

    conn.commit()
    conn.close()


def main():

    for p_name in ['camel', 'hadoop', 'linux', 'zephyr']:

        extract_data(p_name)

if __name__=="__main__":
    main()
