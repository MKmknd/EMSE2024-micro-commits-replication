
# write the database path
db='./../prepare_dataset/db/all.db'

# the proportion of corrective, adaptive, perfective commits in all studied commits
sqlite3 ${db} -cmd '.mode markdown' '
with 
    num_corrective as (
       select project, count(*) n_corrective
       from commit_maintenance
       where corrective_flag=1
       group by project
    ),
    num_adaptive as (
       select project, count(*) n_adaptive
       from commit_maintenance
       where adaptive_flag=1
       group by project
    ),
    num_perfective as (
       select project, count(*) n_perfective
       from commit_maintenance
       where perfective_flag=1
       group by project
    ),
    num_all as (
       select project, count(*) n_all
       from commit_maintenance
       group by project
    )
select *,
       printf("%5.2f", n_corrective*100.0/n_all) as pro_corrective,
       printf("%5.2f", n_adaptive*100.0/n_all) as pro_adaptive,
       printf("%5.2f", n_perfective*100.0/n_all) as pro_perfective
       from num_all
       natural join num_corrective
       natural join num_adaptive
       natural join num_perfective
       ;
'

# | project | n_all  | n_corrective | n_adaptive | n_perfective | pro_corrective | pro_adaptive | pro_perfective |
# |---------|--------|--------------|------------|--------------|----------------|--------------|----------------|
# | camel   | 38458  | 10350        | 5849       | 2353         | 26.91          | 15.21        |  6.12          |
# | hadoop  | 53796  | 9311         | 7991       | 2805         | 17.31          | 14.85        |  5.21          |
# | linux   | 748618 | 256815       | 271608     | 96994        | 34.31          | 36.28        | 12.96          |
# | zephyr  | 22097  | 6879         | 9032       | 2868         | 31.13          | 40.87        | 12.98          |

# with the header files and no file criterion
# | project | n_all  | n_corrective | n_adaptive | n_perfective | pro_corrective | pro_adaptive | pro_perfective |
# |---------|--------|--------------|------------|--------------|----------------|--------------|----------------|
# | camel   | 38458  | 10350        | 5849       | 2353         | 26.91          | 15.21        |  6.12          |
# | hadoop  | 53796  | 9311         | 7991       | 2805         | 17.31          | 14.85        |  5.21          |
# | linux   | 802726 | 271564       | 292173     | 103590       | 33.83          | 36.40        | 12.90          |
# | zephyr  | 25542  | 7595         | 10625      | 3141         | 29.74          | 41.60        | 12.30          |

sqlite3 ${db} -cmd '.mode markdown' '
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
select *,
       printf("%5.2f", n_corrective*100.0/n_all) as pro_corrective,
       printf("%5.2f", n_adaptive*100.0/n_all) as pro_adaptive,
       printf("%5.2f", n_perfective*100.0/n_all) as pro_perfective
       from num_all
       natural join num_corrective
       natural join num_adaptive
       natural join num_perfective
       ;
'

# | project | n_all  | n_corrective | n_adaptive | n_perfective | pro_corrective | pro_adaptive | pro_perfective |
# |---------|--------|--------------|------------|--------------|----------------|--------------|----------------|
# | camel   | 3735   | 1680         | 218        | 246          | 44.98          |  5.84        |  6.59          |
# | hadoop  | 3631   | 901          | 122        | 141          | 24.81          |  3.36        |  3.88          |
# | linux   | 119567 | 55859        | 24816      | 11075        | 46.72          | 20.75        |  9.26          |
# | zephyr  | 3645   | 1628         | 638        | 395          | 44.66          | 17.50        | 10.84          |

# with the header files and no file criterion
# | project | n_all  | n_corrective | n_adaptive | n_perfective | pro_corrective | pro_adaptive | pro_perfective |
# |---------|--------|--------------|------------|--------------|----------------|--------------|----------------|
# | camel   | 4230   | 1865         | 251        | 294          | 44.09          |  5.93        |  6.95          |
# | hadoop  | 4010   | 1015         | 136        | 155          | 25.31          |  3.39        |  3.87          |
# | linux   | 138142 | 63710        | 28894      | 13474        | 46.12          | 20.92        |  9.75          |
# | zephyr  | 4585   | 2015         | 853        | 460          | 43.95          | 18.60        | 10.03          |