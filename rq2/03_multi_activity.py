import sys
import re
import os
import sqlite3
import subprocess
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

db_path = './db/manual.db'

def compute1():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    command = """
              select linecid,  operation || '-' || category fullope
              from multi_operation
              """
    cur.execute(command)
    data_dict = {}
    for row in cur.fetchall():
        if not row[0] in data_dict:
            data_dict[row[0]] = set()
        data_dict[row[0]].add(row[1])
    conn.close()


    idx_dict = {}
    ans_dict = {}
    idx = 0
    for key in data_dict.keys():
        ope_set = data_dict[key]

        flag = True
        for tmp_idx in idx_dict.keys():
            if len(ope_set - idx_dict[tmp_idx])==0:
                ans_dict[tmp_idx] += 1
                flag = False
                break
        
        if flag:
            idx_dict[idx] = ope_set
            ans_dict[idx] = 1
            idx += 1
    
    show_dict = {}
    ncommits = 0
    for idx in idx_dict.keys():
        show_dict[','.join(list(idx_dict[idx]))] = ans_dict[idx]
        ncommits += ans_dict[idx]

    print(ncommits)
    TABLE = []
    for idx, row in enumerate(sorted(show_dict.items(), key=lambda x:-x[1])):
        print('{0}, {1}'.format(idx+1, row))
        ope1, tar1 = row[0].split(',')[0].split('-')
        ope2, tar2 = row[0].split(',')[1].split('-')
        if len(row[0].split(','))==3:
            ope3, tar3 = row[0].split(',')[2].split('-')
        else:
            ope3 = tar3 = '-'

        pro = Decimal(str(100*row[1]/ncommits)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        num_pro = Decimal(str(row[1]/ncommits)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        TABLE.append([ope1, tar1, ope2, tar2, ope3, tar3, '{0}'.format(row[1]), '\\Chart{{{0}}}{{{1}}}\\\\'.format(pro, num_pro)])
    

    table_column = ['Operation1', 'Target1', 'Operation2', 'Target2', 'Operation3', 'Target3', 'n', 'Pro\\\\']
    if not os.path.exists("./tables"): os.makedirs("./tables")
    TABLE = pd.DataFrame(TABLE, columns=table_column)
    TABLE.to_csv(path_or_buf='./tables/multi_activity.csv', index=False, sep="&")




    # second count
    show_dict = {}
    ncommits = 0
    for linecid in data_dict.keys():
        for act in data_dict[linecid]:

            if not act in show_dict:
                show_dict[act] = 0
            show_dict[act] += 1
            ncommits += 1
    
    TABLE = []
    for row in sorted(show_dict.items(), key=lambda x:-x[1]):
        pro = Decimal(str(100*row[1]/ncommits)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        num_pro = Decimal(str(row[1]/ncommits)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        #TABLE.append([row[0].split('-')[0], row[0].split('-')[1], '{0}%({1})\\\\'.format(pro, row[1])])
        TABLE.append([row[0].split('-')[0], row[0].split('-')[1], '{0}'.format(row[1]), '\\Chart{{{0}}}{{{1}}}\\\\'.format(pro, num_pro)])
    
    table_column = ['Operation', 'Target', 'n', 'Pro\\\\']
    TABLE = pd.DataFrame(TABLE, columns=table_column)
    TABLE.to_csv(path_or_buf='./tables/multi_unique_activity.csv', index=False, sep="&")


    # third count
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    command = """
              select operation, category, count(*) n
              from multi_operation
              group by operation, category
              order by n DESC
              """
    cur.execute(command)

    data_list = []
    ncommits = 0
    for row in cur.fetchall():
        data_list.append(row)
        ncommits += row[2]

    conn.close()


    TABLE = []
    for row in data_list:
        pro = Decimal(str(100*row[2]/ncommits)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        num_pro = Decimal(str(row[2]/ncommits)).quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
        #TABLE.append([row[0], row[1], '{0}%({1})\\\\'.format(pro, row[2])])
        TABLE.append([row[0], row[1], '{0}'.format(row[2]), '\\Chart{{{0}}}{{{1}}}\\\\'.format(pro, num_pro)])
    

    table_column = ['Operation', 'Target', 'n', 'Pro\\\\']
    if not os.path.exists("./tables"): os.makedirs("./tables")
    TABLE = pd.DataFrame(TABLE, columns=table_column)
    TABLE.to_csv(path_or_buf='./tables/multi_unique_activity2.csv', index=False, sep="&")
    # this file should be the same with multi_unique_activity.csv

def main():

    compute1()

if __name__=="__main__":
    main()


