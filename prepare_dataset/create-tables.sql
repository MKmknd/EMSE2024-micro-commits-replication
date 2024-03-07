drop table if exists token_commit_summary;

create table token_commit_summary as
select org_commit_hash_id as linecid,
cregit_commit_hash_id as tokencid,
count(hunk_index_id) as hunkstokens,
sum(added_tokens) as addtokens,
sum(deleted_tokens) as deltokens,
count(distinct file_path_id) as filestokens
from commit_token_sizes group by org_commit_hash_id;

drop table if exists line_commit_summary;

create table line_commit_summary as
select org_commit_hash_id as linecid,
  cregit_commit_hash_id as tokencid,
  count(hunk_index_id) as hunkslines,
  sum(added_lines) as addlines,
  sum(deleted_lines) as dellines,
  count(distinct file_path_id) as fileslines
from commit_line_sizes group by org_commit_hash_id;


