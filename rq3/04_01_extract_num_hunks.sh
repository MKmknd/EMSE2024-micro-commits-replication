#!/bin/sh

mkdir ./data/
mkdir ./plot/

base_db='./../prepare_dataset/db/all.db'

sqlite3 ${base_db} -cmd '.mode csv' '
SELECT lt.project,lt.linecid,lt.tokencid,lt.hunkslines,mt.hunkstokens
FROM line_commit_summary lt
INNER JOIN micro_commits mt
ON lt.linecid=mt.linecid;
'  > ./data/num_hunks.csv
