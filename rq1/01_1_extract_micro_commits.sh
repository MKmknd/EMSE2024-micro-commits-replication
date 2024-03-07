#!/bin/sh

project_name_list=(
    "camel"
    "hadoop"
    "linux"
    "zephyr"
)
base_db='./../prepare_dataset/db/all.db'

mkdir csv
mkdir db

for p_name in "${project_name_list[@]}" ; do
    echo ${p_name}

    rm ./db/${p_name}.db

    sqlite3 ${base_db} -cmd '.mode csv' '
    SELECT
    linecid, tokencid
    FROM micro_commits
    WHERE project="'${p_name}'"' > ./csv/${p_name}_micro_commits.csv

    sqlite3 ./db/${p_name}.db -cmd '.mode csv' '
    CREATE TABLE 
    micro_commits(org_commit_hash_id TEXT, cregit_commit_hash_id TEXT, PRIMARY KEY(org_commit_hash_id))
    '

    sqlite3 ./db/${p_name}.db -cmd '.mode csv' '.import ./csv/'${p_name}'_micro_commits.csv micro_commits'

done
