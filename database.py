# import sqlite3 as sql
import psycopg2 as sql

conn_user = sql.connect(host='ec2-54-243-150-10.compute-1.amazonaws.com',
                        database='dvmjo6pvokn3v',
                        user='icknsevpzbardh',
                        port='5432',
                        password='5c195733c2d92181a25b5e73f8870c9b3788157e90380bcbdef013daa743644d')
conn_entry = sql.connect(host='ec2-54-243-150-10.compute-1.amazonaws.com',
                        database='dvmjo6pvokn3v',
                        user='icknsevpzbardh',
                        port='5432',
                        password='5c195733c2d92181a25b5e73f8870c9b3788157e90380bcbdef013daa743644d')


def user_add(name, passwd, email):
    c = conn_user.cursor()
    c.execute('select * from data where name = %s;', (name,))
    data = c.fetchall()
    if len(data) != 0:
        return 'Name used'
    try:
        c.execute('insert into data values (%s, %s, %s);', (name, passwd, email))
    except Exception as e:
        conn_user.commit()
        c.close()
        return 'Fail, ' + str(e)
    conn_user.commit()
    c.close()
    return 'Success'


def user_del(name, passwd):
    c = conn_user.cursor()
    c.execute('select * from data where name = %s;', (name, ))
    data = c.fetchall()
    if len(data) == 0:
        conn_user.commit()
        c.close()
        return 'No such of user'
    if data[0][1] != passwd:
        conn_user.commit()
        c.close()
        return 'Password error'
    c.execute('delete from data where name = %s;', (name, ))
    conn_user.commit()
    c.close()
    return 'Success'


def user_check(name, passwd):
    c = conn_user.cursor()
    c.execute('select * from data where name = %s;', (name, ))
    data = c.fetchall()
    c.close()
    if len(data) == 0:
        return 'No such of user'
    if data[0][1] != passwd:
        return 'Password error'
    return 'Success'


def user_get_email(name):
    c = conn_user.cursor()
    conn_user.commit()
    c.execute('select email from data where name = %s;', (name, ))
    data = c.fetchall()
    if len(data) == 0:
        return 'Get None'
    c.close()
    return data[0][0]


def user_all_name():
    c = conn_user.cursor()
    c.execute('select name from data')
    data = c.fetchall()
    c.close()
    if len(data) == 0:
        return []
    return data


def user_all():
    c = conn_user.cursor()
    c.execute('select name, email from data')
    data = c.fetchall()
    c.close()
    if len(data) == 0:
        return []
    return data


# 设置每页20条
one_page = 20


def entry_get(page):
    c = conn_entry.cursor()
    c.execute('select * from entries order by id desc limit %s offset %s;', (one_page, one_page * page))
    data = c.fetchall()
    conn_entry.commit()
    c.close()
    return data


def entry_insert(sid, name, time, icon, message):
    c = conn_entry.cursor()
    try:
        c.execute('insert into entries values (%s, %s, %s, %s, %s)', (sid, name, time, icon, message))
    except Exception as e:
        return 'Fail, ' + str(e)
    finally:
        conn_entry.commit()
        c.close()
    return 'Success'


def entry_get_new_id():
    c = conn_entry.cursor()
    c.execute('select nid from sid')
    data = c.fetchall()
    nid = data[0][0]
    c.execute('update sid set nid = %s where s = 0;', (nid + 1, ))
    conn_entry.commit()
    c.close()
    return nid


if __name__ == '__main__':
    for i in range(10):
        print(entry_get_new_id())

