#!/bin/sh

mkdir ./data/
mkdir ./plot/

project_name_list=(
    "camel"
    "hadoop"
    "linux"
    "zephyr"
)
#project_name_list=(
#    "ActionBarSherlock"
#)
base_dir='./db/'

p_avg='./data/average_changed_tokens.csv'
rm ${p_avg}

for p_name in "${project_name_list[@]}" ; do
    echo ${p_name}
    tmp=$(sqlite3 ${base_dir}${p_name}.db -cmd '.mode csv' "SELECT AVG(cnt) FROM (SELECT org_commit_hash_id, COUNT(*) AS cnt FROM changed_tokens GROUP BY org_commit_hash_id);")
    echo "Average changed tokens: "${tmp}
    echo "${p_name},${tmp}" >> ${p_avg}

    echo "Changed token types order"
    sqlite3 ${base_dir}${p_name}.db -cmd '.mode csv' 'SELECT token_type, COUNT(*) FROM changed_tokens GROUP BY token_type ORDER BY COUNT(*) DESC;'  > ./data/changed_token_type_order_${p_name}.csv

    echo "Changed tokens order"
    sqlite3 ${base_dir}${p_name}.db -cmd '.mode csv' 'SELECT token, COUNT(*) FROM changed_tokens GROUP BY token ORDER BY COUNT(*) DESC;'  > ./data/changed_token_order_${p_name}.csv

    echo "Replaced tokens and token types: hunk(rep)"
    sqlite3 ${base_dir}${p_name}.db -cmd '.mode csv' '
    CREATE TABLE replace_hunks AS
    SELECT
    *
    FROM
    changed_hunk_types
    WHERE
    hunk_type="rep";
    '

    sqlite3 ${base_dir}${p_name}.db -cmd '.mode csv' '
    CREATE TABLE replace_tokens AS
    SELECT
    *
    FROM
    changed_tokens
    NATURAL JOIN
    replace_hunks;
    '

    sqlite3 ${base_dir}${p_name}.db -cmd '.mode csv' '
    SELECT token_type, COUNT(*) FROM replace_tokens GROUP BY token_type ORDER BY COUNT(*) DESC;
    ' > ./data/replaced_token_type_order_${p_name}.csv

    sqlite3 ${base_dir}${p_name}.db -cmd '.mode csv' '
    SELECT token, COUNT(*) FROM replace_tokens GROUP BY token ORDER BY COUNT(*) DESC;
    '  > ./data/replaced_token_order_${p_name}.csv

done
