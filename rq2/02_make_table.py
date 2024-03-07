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
              select operation, category, count(*) n
              from single_operation
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
    TABLE.to_csv(path_or_buf='./tables/single_activity.csv', index=False, sep="&")
    TABLE.to_csv(path_or_buf='./tables/single_activity_comma.csv', index=False, sep=",")

def main():

    compute1()

if __name__=="__main__":
    main()


