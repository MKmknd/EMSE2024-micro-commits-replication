D=./db

mkdir ${D}

sqlite3 ${D}/linux.db < create-tables.sql
sqlite3 ${D}/zephyr.db < create-tables.sql
sqlite3 ${D}/hadoop.db < create-tables.sql
sqlite3 ${D}/camel.db < create-tables.sql

sqlite3 ${D}/all.db < ./consolidate.sql