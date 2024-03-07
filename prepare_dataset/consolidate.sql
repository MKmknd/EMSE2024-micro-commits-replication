
attach './db/linux.db' as l;

create table token_commit_summary as
  select
   'linux' as project,
   s.* 
   from l.token_commit_summary as s;

create table line_commit_summary as
  select  'linux' as project,
   s.* 
   from l.line_commit_summary as s;

attach './db/zephyr.db' as z;

insert into token_commit_summary 
  select 'zephyr' as project,
  s.* 
  from z.token_commit_summary as s;

insert into line_commit_summary 
  select 'zephyr' as project,
  s.* 
  from z.line_commit_summary as s;


attach './db/hadoop.db' as h;

insert into token_commit_summary 
select 'hadoop' as project,
s.* 
from h.token_commit_summary as s;

insert into line_commit_summary 
select 'hadoop' as project,
s.* 
from h.line_commit_summary as s;


attach './db/camel.db' as c;

insert into token_commit_summary 
select 'camel' as project,
s.* 
from c.token_commit_summary as s;

insert into line_commit_summary 
select 'camel' as project,
s.* 
from c.line_commit_summary as s;

create table oneline_commits as
select project, linecid, tokencid from line_commit_summary where addlines =1 and dellines =1 and fileslines = 1 and hunkslines = 1;
