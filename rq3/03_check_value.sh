
# write the database path
base_db='./../prepare_dataset/db/all.db'

# add or remove at most one token
# label exactly_one_token_in_one_line_commits
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


echo "one line"
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