
mkdir tmp
mkdir data
mkdir plot
cp ./../prepare_dataset/db/all.db ./tmp/

db='./tmp/all.db'

sqlite3 ${db} -cmd '.mode markdown' '
create table numbers(n int) ;
'

sqlite3 ${db} -cmd '.mode markdown' '
insert into numbers values (0),(1),(2),(3),(4),(5),(6),(7),(8),(9),(10);
'

sqlite3 ${db} -cmd '.mode markdown' '
    create table num_onelines as 
       select project, count(*) nl1commits
       from oneline_commits
       group by project
'

sqlite3 ${db} -cmd '.mode markdown' '
create table rip as
select * from (
       select
       p as project, na.n as "added", nd.n as "deleted", count(project) as n
       from
       (select distinct project as p from perp) as p,
       numbers as na, numbers as nd
       left join token_commit_summary on (p.p = project and na.n = addtokens and nd.n = deltokens)
       group by p, na.n, nd.n) left join perp using (project) left join num_onelines using (project);
'

sqlite3 ${db} -cmd '.mode markdown' '
create table rip1 as
select * from (
       select
       p as project, na.n as 'added', nd.n as 'deleted', count(project) as n1line
       from
       (select distinct project as p from perp) as p,
       numbers as na, numbers as nd
       left join token_commit_summary on (p.p = project and na.n = addtokens and nd.n = deltokens)
       natural join oneline_commits
       group by p, na.n, nd.n);
'

sqlite3 ${db} -cmd '.mode markdown' '
create table bytoken as select * from rip1 join rip using (project, added, deleted);
'

sqlite3 ${db} -cmd '.mode csv' '.headers on' '
select * from bytoken;
'  > ./data/heatmapSizes.csv


sqlite3 ${db} -cmd  '.mode csv' '.headers on' '
select project, itokens as maxtokens,
       nt_commits, nt_commits*1.0/ncommits as propall, 
       n1l_commits, n1l_commits*1.0/nl1commits as prop1l 
       from (
              select project, n as itokens, count(*) as nt_commits from numbers  join token_commit_summary on (deltokens <= n  and addtokens <= n)
              group by project, n
       ) as r
       join (
              select project, n as itokens, count(*) as n1l_commits from numbers  join token_commit_summary on (deltokens <= n  and addtokens <= n)
              natural join oneline_commits
              group by project, n
       ) as r2
       using (project, itokens)
       join perp using (project)
       left join num_onelines using (project)
       ;
' > ./data/maxtokenadded.csv