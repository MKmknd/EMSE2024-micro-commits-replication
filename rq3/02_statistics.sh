
db='./../prepare_dataset/db/all.db'

# the proportion of commits that add and remove at most one token in One-line commits
sqlite3 ${db} -cmd '.mode markdown' '
with 
    num_oneline as (
       select project, count(*) n_oneline
       from oneline_commits
       group by project
    ),
    num_onetoken as (
	   select project, count(*) n_onetoken
      from token_commit_summary
		where addtokens=1 and deltokens=1 and hunkstokens=1 and filestokens=1
		group by project
    )
select *,
       printf("%5.2f", n_onetoken*100.0/n_oneline) as pro_onetoken
       from num_oneline
       natural join num_onetoken
;
'

# | project | n_oneline | n_onetoken | pro_onetoken |
# |---------|-----------|------------|--------------|
# | camel   | 2405      | 1319       | 54.84        |
# | hadoop  | 2302      | 1288       | 55.95        |
# | linux   | 65858     | 32973      | 50.07        |
# | zephyr  | 1979      | 1247       | 63.01        |

sqlite3 ${db} -cmd '.mode markdown' '
drop table if exists micro_commits;
'
sqlite3 ${db} -cmd '.mode markdown' '
create table micro_commits as
       select *
       from token_commit_summary
       where addtokens<=5 and deltokens<=5;
'

# intersection
sqlite3 ${db} -cmd '.mode markdown' '
drop table if exists intersect_commits;
'
sqlite3 ${db} -cmd '.mode markdown' '
    create table intersect_commits as
    select project, linecid
       from oneline_commits
       intersect
       select project, linecid
       from micro_commits
'


# the proportion of commits that add or remove at most three tokens in One-line commits
sqlite3 ${db} -cmd '.mode markdown' '
with 
    num_oneline as (
       select project, count(*) n_oneline
       from oneline_commits
       group by project
    ),
    num_threetoken as (
	   select project, count(*) n_threetoken
		from intersect_commits
      natural join micro_commits
		where addtokens<=3 and deltokens<=3
		group by project
    )
select *,
       printf("%5.2f", n_threetoken*100.0/n_oneline) as pro_threetoken
       from num_oneline
       natural join num_threetoken
;
'
# | project | n_oneline | n_threetoken | pro_threetoken |
# |---------|-----------|--------------|----------------|
# | camel   | 2405      | 1824         | 75.84          |
# | hadoop  | 2302      | 1829         | 79.45          |
# | linux   | 65858     | 52542        | 79.78          |
# | zephyr  | 1979      | 1631         | 82.42          |


# the proportion of commits that add or remove at most five tokens in One-line commits
sqlite3 ${db} -cmd '.mode markdown' '
with 
    num_oneline as (
       select project, count(*) n_oneline
       from oneline_commits
       group by project
    ),
    num_fivetoken as (
	   select project, count(*) n_fivetoken
      from intersect_commits
      natural join micro_commits
		where addtokens<=5 and deltokens<=5
		group by project
    )
select *,
       printf("%5.2f", n_fivetoken*100.0/n_oneline) as pro_fivetoken
       from num_oneline
       natural join num_fivetoken
;
'

# | project | n_oneline | n_fivetoken | pro_fivetoken |
# |---------|-----------|-------------|---------------|
# | camel   | 2405      | 2131        | 88.61         |
# | hadoop  | 2302      | 2069        | 89.88         |
# | linux   | 65858     | 59836       | 90.86         |
# | zephyr  | 1979      | 1849        | 93.43         |


# the proportion of One-line commits in micro commits
sqlite3 ${db} -cmd '.mode markdown' '
    with 
    num_oneline as (
       select project, count(*) n_line
       from line_commit_summary
       where hunkslines=1 and addlines=1 and dellines=1 and fileslines=1
       group by project
    ),
    num_micro as (
       select project, count(*) n_micro
       from micro_commits
       group by project
    )
    select *,
       printf("%5.2f", n_line*100.0/n_micro) as pro_line
       from num_micro
       natural join num_oneline
       group by project
    ;
'
# | project | n_micro | n_line | pro_line |
# |---------|---------|--------|----------|
# | camel   | 4230    | 2405   | 56.86    |
# | hadoop  | 4010    | 2302   | 57.41    |
# | linux   | 138142  | 65858  | 47.67    |
# | zephyr  | 4585    | 1979   | 43.16    |

# the proportion of micro commits in One-line commits
sqlite3 ${db} -cmd '.mode markdown' '
    with 
    num_twoline as (
       select project, count(*) n_line
       from line_commit_summary
       where hunkslines<=2 and addlines<=2 and dellines=1 and fileslines=1
       group by project
    ),
    num_micro as (
       select project, count(*) n_micro
       from micro_commits
       group by project
    )
    select *,
       printf("%5.2f", n_line*100.0/n_micro) as pro_line
       from num_micro
       natural join num_twoline
       group by project
    ;
'
# | project | n_micro | n_line | pro_line |
# |---------|---------|--------|----------|
# | camel   | 4230    | 3644   | 86.15    |
# | hadoop  | 4010    | 3356   | 83.69    |
# | linux   | 138142  | 98610  | 71.38    |
# | zephyr  | 4585    | 2685   | 58.56    |

# the proportion of commits that change at most two lines in micro commits
echo "two lines"
sqlite3 ${db} -cmd '.mode markdown' '
    with 
    twoline_commits as (
       select project, linecid
       from line_commit_summary
       where hunkslines=1 and addlines<=2 and dellines<=2 and fileslines=1
    ),
	 micro_num as (
        select project, count(*) n_micro
        from micro_commits
        group by project
	 )
    select *,
	     printf("%5.2f", n_line*100.0/n_micro) as pro_line
	 from(
	     select project, count(*) as n_line
	     from(
            select project, linecid
            from twoline_commits
            intersect
            select project, linecid
            from micro_commits
		  )
		  group by project
	 )
	 natural join micro_num
    ;
'
# | project | n_line | n_micro | pro_line |
# |---------|--------|---------|----------|
# | camel   | 2554   | 4230    | 60.38    |
# | hadoop  | 2706   | 4010    | 67.48    |
# | linux   | 91256  | 138142  | 66.06    |
# | zephyr  | 2731   | 4585    | 59.56    |


# the proportion of commits that change at most one line (not One-line commits) in micro commits
sqlite3 ${db} -cmd '.mode markdown' '
    with 
    oneline_commits as (
       select project, linecid
       from line_commit_summary
       where hunkslines=1 and addlines<=1 and dellines<=1 and fileslines=1
    ),
	 micro_num as (
        select project, count(*) n_micro
        from micro_commits
        group by project
	 )
    select *,
	     printf("%5.2f", n_line*100.0/n_micro) as pro_line
	 from(
	     select project, count(*) as n_line
	     from(
            select project, linecid
            from oneline_commits
            intersect
            select project, linecid
            from micro_commits
		  )
		  group by project
	 )
	 natural join micro_num
    ;
'
# | project | n_line | n_micro | pro_line |
# |---------|--------|---------|----------|
# | camel   | 2365   | 4230    | 55.91    |
# | hadoop  | 2327   | 4010    | 58.03    |
# | linux   | 81086  | 138142  | 58.70    |
# | zephyr  | 2421   | 4585    | 52.80    |
