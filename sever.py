from flask import Flask, session, redirect, url_for, escape, request, render_template
import hashlib
from database import *
from db_init import clear_all
import time
import threading
import os
import pytz
from datetime import datetime


app = Flask(__name__)

entries = []
users = []


def get_icon(email):
    return'https://s.gravatar.com/avatar/' + hashlib.md5(email.encode()).hexdigest() + '?s=144'


@app.route('/', methods=['GET', 'POST'])
def index():
    sever_init()
    if request.method == 'GET':
        if not 'username' in session:
            return redirect(url_for('login'))
        if 'display_mode' in session and session['display_mode'] == 'wap':
            html = 'ChatRoom_wap.html'
        else:
            html = 'ChatRoom.html'
        return render_template(html, username=session['username'],
                               icon=session['icon'],
                               entries=entries,
                               users=users,
                               title='聊天室(迫真)',
                               )
    if request.method == 'POST':
        timedata = time.localtime(time.time())
        cndata = datetime(timedata[0], timedata[1], timedata[2], timedata[3], timedata[4], timedata[5])
        central = pytz.timezone('Asia/Shanghai')
        time_cn = central.localize(cndata)
        data = {
            'username': session['username'],
            'message': request.form['message'],
            'time': str(time_cn.month).zfill(2) + '/' + str(time_cn.day).zfill(2) + ' ' + \
                    str(time_cn.hour).zfill(2) + ':' + str(time_cn.minute).zfill(2),
        }
        entry_insert(entry_get_new_id(), data['username'], data['time'], get_icon(session['email']), data['message'])
        return redirect(url_for('index'))


@app.route('/wap', methods=['GET'])
def wap():
    session['display_mode'] = 'wap'
    return redirect('/')


@app.route('/pc', methods=['GET'])
def pc():
    session['display_mode'] = 'pc'
    return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        redirect(url_for('logout'))
    if request.method == 'POST':
        if request.form['passwd'] != request.form['passwd_']:
            return '两次密码不一致。' + '<a href=%s>返回</a>' % url_for('signup')
        if request.form['username'] == '':
            return '用户名不能为空。' + '<a href=%s>返回</a>' % url_for('signup')
        hl = hashlib.md5(request.form['passwd'].encode()).hexdigest()
        result = user_add(request.form['username'], hl, request.form['email'].lower())
        sever_user_init()
        return result + '<a href=%s>首页</a>' % url_for('index')
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        redirect(url_for('logout'))
    if request.method == 'POST':
        hl = hashlib.md5(request.form['passwd'].encode()).hexdigest()
        result = user_check(request.form['username'], hl)
        if result != 'Success':
            return result
        session['username'] = request.form['username']
        session['passwd'] = hl
        session['email'] = user_get_email(session['username'])
        session['icon'] = get_icon(session['email'])
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/get_email/<username>')
def get_email(username):
    email = user_get_email(username)
    return email + '<br><img src=\"%s\">' % (get_icon(email))


@app.route('/history/<int:page>', methods=['GET', 'POST'])
def get_history(page):
    if not 'username' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        get_entries = entry_get(page)
        return render_template('History.html', entries=get_entries)
    if request.method == 'POST':
        get_page = request.form['page']
        return redirect('/history/' + get_page)


@app.route('/about')
def about():
    return redirect('https://github.com/LanceLiang2018/chatroom')


@app.route('/clear_all')
def clear():
    # clear_all()
    t = threading.Thread(target=clear_all)
    t.setDaemon(True)
    t.start()
    return 'Thread started...'


def sever_user_init():
    global users
    users = user_all_name()


def sever_entry_init():
    global entries
    entries = list(entry_get(0))
    for i in range(len(entries)):
        entries[i] = list(entries[i])
        s = entries[i][4]
        line = s.split('\n')
        sum = 0
        for j in line:
            sum = sum + len(j) // 35
        entries[i].append(entries[i][4].count('\n') + sum)


def sever_init():
    sever_user_init()
    sever_entry_init()


# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    sever_init()
    # app.run(threaded=True, debug=False, host='0.0.0.0', port=10086)
    app.run(threaded=True, debug=False, host='0.0.0.0', port=os.getenv("PORT", "5000"))
    print('Started...')
