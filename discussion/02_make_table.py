import sys
import re
import os
import sqlite3
import subprocess
import pandas as pd
from decimal import Decimal, ROUND_HALF_UP

db_path = './../prepare_dataset/db/all.db'

disp_p_dict = {'camel': 'Camel', 'hadoop': 'Hadoop', 'linux': 'Linux', 'zephyr': 'Zephyr'}

def non_micro_commits(corrective_list, adaptive_list, perfective_list):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    command = """
        with 
            num_corrective as (
            SELECT a.project, COUNT(*) n_corrective
            FROM commit_maintenance AS a
            LEFT JOIN micro_commits AS m ON a.linecid=m.linecid
            WHERE m.linecid IS NULL AND a.corrective_flag=1
            GROUP BY a.project
            ),
            num_adaptive as (
            SELECT a.project, COUNT(*) n_adaptive
            FROM commit_maintenance AS a
            LEFT JOIN micro_commits AS m ON a.linecid=m.linecid
            WHERE m.linecid IS NULL AND a.adaptive_flag=1
            GROUP BY a.project
            ),
            num_perfective as (
            SELECT a.project, COUNT(*) n_perfective
            FROM commit_maintenance AS a
            LEFT JOIN micro_commits AS m ON a.linecid=m.linecid
            WHERE m.linecid IS NULL AND a.perfective_flag=1
            GROUP BY a.project
            ),
            num_non_micro as (
            SELECT a.project, COUNT(*) n_non_micro
            FROM commit_maintenance AS a
            LEFT JOIN micro_commits AS m ON a.linecid=m.linecid
            WHERE m.linecid IS NULL
            GROUP BY a.project
            )
        select *
            from num_non_micro
            natural join num_corrective
            natural join num_adaptive
            natural join num_perfective
       ;
              """
    cur.execute(command)

    data_list = []
    for row in cur.fetchall():
        data_list.append(row)

    conn.close()

    TABLE = []
    for row in data_list:
        pro_c = Decimal(str(100*row[2]/row[1])).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        pro_a = Decimal(str(100*row[3]/row[1])).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        pro_p = Decimal(str(100*row[4]/row[1])).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        TABLE.append([disp_p_dict[row[0]], '{0:,}'.format(row[1]), '{0}({1:,})'.format(pro_c, row[2]), '{0}({1:,})'.format(pro_a, row[3]), '{0}({1:,})\\\\'.format(pro_p, row[4])])

        corrective_list.append([disp_p_dict[row[0]], 'Non-Micro', pro_c, '{0}%XXX({1})'.format(pro_c, row[2])])
        adaptive_list.append([disp_p_dict[row[0]], 'Non-Micro', pro_a, '{0}%XXX({1})'.format(pro_a, row[3])])
        perfective_list.append([disp_p_dict[row[0]], 'Non-Micro', pro_p, '{0}%XXX({1})'.format(pro_p, row[4])])
    

    table_column = ['Project', 'All', 'Corrective', 'Adaptive', 'Perfective\\\\']
    if not os.path.exists("./tables"): os.makedirs("./tables")
    TABLE = pd.DataFrame(TABLE, columns=table_column)
    TABLE.to_csv(path_or_buf='./tables/non_micro_commits.csv', index=False, sep="&")


def micro_commits(corrective_list, adaptive_list, perfective_list):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    command = """
            with 
                num_corrective as (
                select project, count(*) n_corrective
                from commit_maintenance
                natural join micro_commits
                where corrective_flag=1
                group by project
                ),
                num_adaptive as (
                select project, count(*) n_adaptive
                from commit_maintenance
                natural join micro_commits
                where adaptive_flag=1
                group by project
                ),
                num_perfective as (
                select project, count(*) n_perfective
                from commit_maintenance
                natural join micro_commits
                where perfective_flag=1
                group by project
                ),
                num_all as (
                select project, count(*) n_all
                from commit_maintenance
                natural join micro_commits
                group by project
                )
            select *
                from num_all
                natural join num_corrective
                natural join num_adaptive
                natural join num_perfective
       ;
              """
    cur.execute(command)

    data_list = []
    for row in cur.fetchall():
        data_list.append(row)

    conn.close()

    TABLE = []
    for row in data_list:
        pro_c = Decimal(str(100*row[2]/row[1])).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        pro_a = Decimal(str(100*row[3]/row[1])).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        pro_p = Decimal(str(100*row[4]/row[1])).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        TABLE.append([disp_p_dict[row[0]], '{0:,}'.format(row[1]), '{0}({1:,})'.format(pro_c, row[2]), '{0}({1:,})'.format(pro_a, row[3]), '{0}({1:,})\\\\'.format(pro_p, row[4])])


        corrective_list.append([disp_p_dict[row[0]], 'Micro', pro_c, '{0}%XXX({1})'.format(pro_c, row[2])])
        adaptive_list.append([disp_p_dict[row[0]], 'Micro', pro_a, '{0}%XXX({1})'.format(pro_a, row[3])])
        perfective_list.append([disp_p_dict[row[0]], 'Micro', pro_p, '{0}%XXX({1})'.format(pro_p, row[4])])
    

    table_column = ['Project', 'All', 'Corrective', 'Adaptive', 'Perfective\\\\']
    if not os.path.exists("./tables"): os.makedirs("./tables")
    TABLE = pd.DataFrame(TABLE, columns=table_column)
    TABLE.to_csv(path_or_buf='./tables/micro_commits.csv', index=False, sep="&")

def main():

    corrective_list = []
    adaptive_list = []
    perfective_list = []


    non_micro_commits(corrective_list, adaptive_list, perfective_list)
    micro_commits(corrective_list, adaptive_list, perfective_list)

    table_column = ['Project', 'Target', 'Value', 'Label']
    for n, TABLE in zip(['corrective', 'adaptive', 'perfective'], [corrective_list, adaptive_list, perfective_list]):
        TABLE = pd.DataFrame(TABLE, columns=table_column)
        TABLE.to_csv(path_or_buf='./tables/{0}.csv'.format(n), index=False)

if __name__=="__main__":
    main()


