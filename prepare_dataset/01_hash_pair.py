from Utils import util
from Utils.git_reader import get_commit_message
from Utils.git_reader import get_all_hash
import re
import os

cregit_repo_dir = "./cregit_repository/{0}"

def extract_hash_list(cregit_repo_dir):
    return get_all_hash(cregit_repo_dir)


def extract_org_hash_from_cregit_repo(cregit_repo_dir, cregit_hash_list, p_name):

    re_former_commit_id = r"\nFormer-commit-id: ([0-9a-f]+)$"

    org2cregit_hash_dict = {}
    cregit2org_hash_dict = {}
    re_former_commit_id_error = set()
    for idx, commit_hash in enumerate(cregit_hash_list):

        if idx%100==0:
            print("run: {0}/{1}".format(idx, len(cregit_hash_list)))
        log = get_commit_message(cregit_repo_dir, commit_hash)

        match = re.search(re_former_commit_id, log)

        if not match:
            re_former_commit_id_error.add(commit_hash)
            continue
        org2cregit_hash_dict[match.group(1)] = commit_hash
        cregit2org_hash_dict[commit_hash] = match.group(1)

    util.dump_pickle("./pickle/{0}_org2cregit_hash_dict.pickle".format(p_name), org2cregit_hash_dict)
    util.dump_pickle("./pickle/{0}_cregit2org_hash_dict.pickle".format(p_name), cregit2org_hash_dict)
    util.dump_pickle("./pickle/{0}_former_commit_id_error.pickle".format(p_name), re_former_commit_id_error)

    return org2cregit_hash_dict, cregit2org_hash_dict

def main():

    if not os.path.exists('./pickle'): os.makedirs('./pickle')

    for p_name in ['camel', 'hadoop', 'linux', 'zephyr']:

        cregit_hash_list = extract_hash_list(cregit_repo_dir.format(p_name))
        org2cregit_hash_dict, cregit2org_hash_dict = \
            extract_org_hash_from_cregit_repo(cregit_repo_dir.format(p_name), cregit_hash_list, p_name)


if __name__=="__main__":

    main()
