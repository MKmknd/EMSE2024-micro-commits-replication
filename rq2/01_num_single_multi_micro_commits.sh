
# write the database path
db='./db/manual.db'


sqlite3 ${db} -cmd '.mode markdown' '
SELECT COUNT(DISTINCT linecid) multi FROM multi_operation
'

# | multi |
# |-------|
# | 57    |

sqlite3 ${db} -cmd '.mode markdown' '
SELECT COUNT(DISTINCT linecid) single FROM single_operation
'

# | single |
# |--------|
# | 343    |