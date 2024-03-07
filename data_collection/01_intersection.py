import sys
import re
import os
import sqlite3
import subprocess
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

db_path = './../prepare_dataset/db/all.db'

disp_p_dict = {'camel': 'Camel', 'hadoop': 'Hadoop', 'linux': 'Linux', 'zephyr': 'Zephyr'}



def make_table():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    command = """
              with 
                  num_intersections as (select project, count(*) n
                  from intersect_commits
                  group by project
                  ),
                  num_onelines as (
                  select project, count(*) n_oneline
                  from oneline_commits
                  group by project
                  ),
                  num_micro as (
                  select project, count(*) n_micro
                  from micro_commits
                  group by project
                  )
              select *
                  from num_intersections
                  natural join num_onelines
                  natural join num_micro
                  ;
            """
    cur.execute(command)

    data_list = []
    for row in cur.fetchall():
        data_list.append(row)

    conn.close()

    TABLE = []
    for row in data_list:
        pro_one = Decimal(str(100*row[1]/row[2])).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        pro_micro = Decimal(str(100*row[1]/row[3])).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        TABLE.append([disp_p_dict[row[0]], '{0:,}'.format(row[1]), '{0:,}'.format(row[2]), '{0:,}'.format(row[3]), '{0}'.format(pro_one), '{0}\\\\'.format(pro_micro)])


    table_column = ['Project', '\\#intersects', '\\#One-line', '\\#Micro', '\\%One-line', '\\%Micro\\\\']
    if not os.path.exists("./tables"): os.makedirs("./tables")
    TABLE = pd.DataFrame(TABLE, columns=table_column)
    TABLE.to_csv(path_or_buf='./tables/intersection.csv', index=False, sep="&")

def main():

    make_table()

if __name__=="__main__":
    main()


