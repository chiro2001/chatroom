import sqlite3 as sql
import os

try:
    os.remove('database.db')
    os.remove('entries.db')
except Exception as e:
    print(e)
    print('请手动删除*.db')
    exit(0)

conn = sql.connect('database.db')
c = conn.cursor()
c.execute("create table data (name varchar(512), passwd char(32), email varchar(512))")
conn.commit()
c.close()
conn.close()

conn = sql.connect('entries.db')
c = conn.cursor()
c.execute("create table entries (id int,name varchar(512), time varchar(32), icon varchar(512), message varchar(4096));")
c.execute('create table sid (nid int, s int);')
c.execute('insert into sid values (0, 0);')
c.execute('update sid set nid = 1 where s = 0;')
conn.commit()
c.close()
conn.close()