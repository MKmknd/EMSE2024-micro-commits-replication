from Utils import util
import sqlite3
import os

def make_table(p_name):

    if not os.path.exists('./db'): os.makedirs('./db')

    cregit2org_hash_dict = util.load_pickle("./pickle/{0}_cregit2org_hash_dict.pickle".format(p_name))

    conn = sqlite3.connect('./db/{0}.db'.format(p_name))
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS commit_hash_pairs;") 
    cur.execute("CREATE TABLE commit_hash_pairs(org_commit_hash_id TEXT, cregit_commit_hash_id TEXT, PRIMARY KEY (org_commit_hash_id));")

    for cregit_hash in cregit2org_hash_dict.keys():
        cur.execute('INSERT INTO commit_hash_pairs(org_commit_hash_id, cregit_commit_hash_id) VALUES(?,?)', [cregit2org_hash_dict[cregit_hash], cregit_hash])

    conn.commit()
    conn.close()



def main():

    for p_name in ['camel', 'hadoop', 'linux', 'zephyr']:

        make_table(p_name)

if __name__=="__main__":
    main()
