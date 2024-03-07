from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
import sqlite3
import sys
import os
import pandas as pd


def extract_data(p_name):
    conn = sqlite3.connect('./db/{0}.db'.format(p_name))
    cur = conn.cursor()
    cur.execute("SELECT org_commit_hash_id, operation, token_type FROM changed_tokens;")

    data_dict = {}
    for row in cur.fetchall():
        if not row[0] in data_dict:
            data_dict[row[0]] = {'+': [], '-': []}
        
        data_dict[row[0]][row[1]].append(row[2])
    
    return_list = []
    for cid in data_dict.keys():
        tmp = ','.join(sorted(data_dict[cid]['+']))

        tmp += '@@Masa@@'
        tmp += ','.join(sorted(data_dict[cid]['-']))

        return_list.append(tmp)
    
    
    conn.commit()
    conn.close()

    return return_list

def extract_most_common_token_type(N, data_list):
    c = Counter(data_list)
    return c.most_common(N)

def my_replacement(t):
    rep_list = [('argument_list', 'arg'), ('expr_stmt', 'expr')]
    for r in rep_list:
        t = t.replace(r[0], r[1])
    
    if t=='':
        t = 'None'
    return t 

def make_table(p_name, common_list, sum_commits, ALL_TABLE):
    p_dict = {'camel': 'Camel', 'hadoop': 'Hadoop', 'linux': 'Linux', 'zephyr': 'Zephyr'}

    TABLE = []
    for idx, row in enumerate(common_list):
        a, d = row[0].split('@@Masa@@')
        data = [my_replacement(a), my_replacement(d)]
        data.append(row[1])
        pro = Decimal(str(100*row[1]/sum_commits)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        num_pro = Decimal(str(row[1]/sum_commits)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        data.append('\\Chart{{{0}}}{{{1}}}\\\\'.format(pro, num_pro))

        TABLE.append(data)

        if idx==2:
            a_data = [p_dict[p_name]]
        else:
            a_data = ['']
        a_data.extend(data)
        ALL_TABLE.append(a_data)

    table_column = ['Add', 'Del', 'n', 'Pro\\\\']
    if not os.path.exists("./tables"): os.makedirs("./tables")
    TABLE = pd.DataFrame(TABLE, columns=table_column)
    TABLE.to_csv(path_or_buf='./tables/{0}_top5_frequently_appered_commits.csv'.format(p_name), index=False, sep="&")

def main():

    ALL_TABLE = []
    for p_name in ['camel', 'hadoop', 'linux', 'zephyr']:
        data_list = extract_data(p_name)
        common_list = extract_most_common_token_type(5, data_list)
        sum_commits = len(data_list)

        make_table(p_name, common_list, sum_commits, ALL_TABLE)

    table_column = ['Project', 'Add', 'Del', 'n', 'Pro\\\\']
    ALL_TABLE = pd.DataFrame(ALL_TABLE, columns=table_column)
    ALL_TABLE.to_csv(path_or_buf='./tables/all_top5_frequently_appered_commits.csv', index=False, sep="&")


if __name__=="__main__":
    main()
