


db='./../prepare_dataset/db/all.db'

sqlite3 ${db} -cmd '.mode markdown' '
drop table if exists perp;
'
sqlite3 ${db} -cmd '.mode markdown' '
create table perp as
select project, count(*) as ncommits
        from line_commit_summary
        group by project;
'
sqlite3 ${db} -cmd '.mode markdown' '
select * from perp;        
'
# | project | ncommits |
# |---------|----------|
# | camel   | 38458    |
# | hadoop  | 53796    |
# | linux   | 802726   |
# | zephyr  | 25542    |

# show the proportion and number of One-line commits
sqlite3 ${db} -cmd '.mode markdown' '
with 
    oneline as  (select project, count(*) n 
       from line_commit_summary
       where addlines = 1 and dellines = 1 and fileslines = 1 and hunkslines = 1
       group by project)
select *, n*100.0/ncommits as prop from oneline join perp using (project)
       ;
'
# | project |   n   | ncommits |       prop       |
# |---------|-------|----------|------------------|
# | camel   | 2405  | 38458    | 6.25357532893026 |
# | hadoop  | 2302  | 53796    | 4.27912855974422 |
# | linux   | 65858 | 802726   | 8.2042938686426  |
# | zephyr  | 1979  | 25542    | 7.74802286430193 |

# create the table that has the One-line commits
sqlite3 ${db} -cmd '.mode markdown' '
drop table if exists oneline_commits;
'
sqlite3 ${db} -cmd '.mode markdown' '
create table oneline_commits as
       select *
       from line_commit_summary
       where addlines = 1 and dellines = 1 and fileslines = 1 and hunkslines = 1;
'
sqlite3 ${db} -cmd '.mode markdown' '
select * from oneline_commits limit 5;
'
# | project |                 linecid                  |                 tokencid                 | hunkslines | addlines | dellines | fileslines |
# |---------|------------------------------------------|------------------------------------------|------------|----------|----------|------------|
# | linux   | 000092b0b4793caf831f6016fa69d25abba31e51 | 07af63711ebede3f73e60ff90df8d4640a3e06cd | 1          | 1        | 1        | 1          |
# | linux   | 00010268842bda320d43159324651c330e1e8136 | 3d9324471f3bde1557b66005a8844dcdfb909396 | 1          | 1        | 1        | 1          |
# | linux   | 0006526d78e93c3684c806bf7cf3f67dfa49c3c8 | 9cbd6e57229bf459e69fc5e66eb02b588c24e412 | 1          | 1        | 1        | 1          |
# | linux   | 00074ad33b7bc7aa840bc113ee4cee058c5fed70 | 0ba4fa0b6d55580df5b934c67968fcd29a164154 | 1          | 1        | 1        | 1          |
# | linux   | 00093fab980d0a8950a64bdf9e346d0497b9a7e4 | 51629aef84bdcff559751c634a81a0ec35b14e12 | 1          | 1        | 1        | 1          |


project_name_list=(
    "camel"
    "hadoop"
    "linux"
    "zephyr"
)
for p_name in "${project_name_list[@]}" ; do
   echo ${p_name}
   git -C ./../prepare_dataset/repository/${p_name} log --all --format="%H" | wc
done

# camel
#   60911   60911 2497351
# hadoop
#   69997   69997 2869877
# linux
# 1048688 1048688 42996208
# zephyr
#   40883   40883 1676203