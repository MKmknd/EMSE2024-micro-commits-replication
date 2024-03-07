import sys
import re
import os
import sqlite3
import subprocess
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

db_path = './../prepare_dataset/db/all.db'
disp_p_dict = {'camel': 'Camel', 'hadoop': 'Hadoop', 'linux': 'Linux', 'zephyr': 'Zephyr'}

def compute1():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    command = """
    with 
    num_all as (
       select project, count(*) n_all
       from line_commit_summary
       group by project
    ),
    num_onetoken as (
	   select project, count(*) n_onetoken
		from micro_commits
		where addtokens=1 and deltokens=1 and hunkstokens=1
		group by project
    ),
	 num_micro as (
       select project, count(*) n_micro
       from micro_commits
       group by project
    )
    select *,
        printf("%5.2f", n_micro*100.0/n_all) as pro_micro,
        printf("%5.2f", n_onetoken*100.0/n_all) as pro_token
        from num_all
        natural join num_onetoken
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
        pro_onetoken = Decimal(str(100*row[2]/row[1])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        pro_micro = Decimal(str(100*row[3]/row[1])).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        TABLE.append([disp_p_dict[row[0]], '{0:,}'.format(row[3]), pro_micro, '{0:,}'.format(row[2]), '{0}\\\\'.format(pro_onetoken)])
    

    table_column = ['Project', 'Micro commits', 'Prop(\\%)', 'One-token commits', 'Pro(\\%)\\\\']
    if not os.path.exists("./tables"): os.makedirs("./tables")
    TABLE = pd.DataFrame(TABLE, columns=table_column)
    TABLE.to_csv(path_or_buf='./tables/onetoken_commit_prop.csv', index=False, sep="&")

def main():

    compute1()

if __name__=="__main__":
    main()


