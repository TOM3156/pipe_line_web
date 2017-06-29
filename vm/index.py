# -*- coding: utf-8 -*-

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

# 各種設定
DATABASE = 'database.db' # <- チュートリアルと異なる
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'Tomohisa'
PASSWORD = 'tomo3156'

# アプリ生成
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# DB接続
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def select_app():
    cur = g.db.execute('select * from app order by id')
    entries = [dict(id=row[0], name=row[1], pic=row[2], rate=row[3], num_review=row[4], ad=row[5], num_ad=row[6],
                    article=row[7], num_article=row[8], crash=row[9], num_crash=row[10], design=row[11],
                    num_design=row[12], fav=row[13], num_fav=row[14], func=row[15], num_func=row[16], traffic=row[17],
                    num_traffic=row[18], useful=row[19], num_useful=row[20]) for row in cur.fetchall()]
    return render_template('index.html', entries=entries)

@app.route('/detail/<id>')
def detail_app(id):
    cur = g.db.execute('select * from app where id='+str(id))
    apps = [dict(id=row[0], name=row[1], pic="."+row[2], rate=row[3], num_review=row[4], ad=row[5], num_ad=row[6],
                    article=row[7], num_article=row[8], crash=row[9], num_crash=row[10], design=row[11],
                    num_design=row[12], fav=row[13], num_fav=row[14], func=row[15], num_func=row[16], traffic=row[17],
                    num_traffic=row[18], useful=row[19], num_useful=row[20]) for row in cur.fetchall()]
    cur = g.db.execute('select * from review where app_id='+str(id)+' order by id desc')
    entries = [dict(id=row[0], app_id=row[1], rate=row[2], date=row[3], title=row[4],
                review=row[5], ad=row[6], article=row[7], crash=row[8], design=row[9],
                fav=row[10], func=row[11], traffic=row[12], useful=row[13]) for row in cur.fetchall()]
    print(apps)
    return render_template('show_detail.html', apps=apps, entries=entries)

@app.route('/select/<app_id>/<eval>')
def select_review(app_id, eval):
    cur = g.db.execute('select * from app where id='+str(app_id))
    apps = [dict(id=row[0], name=row[1], pic="../../."+row[2], rate=row[3], num_review=row[4], ad=row[5], num_ad=row[6],
                    article=row[7], num_article=row[8], crash=row[9], num_crash=row[10], design=row[11],
                    num_design=row[12], fav=row[13], num_fav=row[14], func=row[15], num_func=row[16], traffic=row[17],
                    num_traffic=row[18], useful=row[19], num_useful=row[20]) for row in cur.fetchall()]
    cur = g.db.execute('select * from review where app_id='+str(app_id)+' and '+str(eval)+'>0  order by id desc')
    entries = [dict(id=row[0], app_id=row[1], rate=row[2], date=row[3], title=row[4], review=row[5], ad=row[6],
                    article=row[7], crash=row[8], design=row[9],fav=row[10], func=row[11], traffic=row[12],
                    useful=row[13]) for row in cur.fetchall()]
    print(apps)
    return render_template('target_review.html', apps=apps, entries=entries)

@app.route('/compare/<app_id>/<eval_id>')
def compare_app(app_id, eval_id):
    cur = g.db.execute('select * from app order by id')
    apps = [dict(id=row[0], name=row[1], pic="../../."+row[2], rate=row[3], num_review=row[4], eval=row[int(app_id)],
                 num_eval=row[int(app_id)+1]) for row in cur.fetchall()]
    cur = g.db.execute('select * from review order by id desc')
    entries = [dict(id=row[0], app_id=row[1], rate=row[2], date=row[3], title=row[4], review=row[5],
                    eval=row[int(eval_id)]) for row in cur.fetchall()]
    if int(eval_id) == 6:
        title = '広告'
    elif int(eval_id) == 7:
        title = '記事'
    elif int(eval_id) == 8:
        title = 'クラッシュ'
    elif int(eval_id) == 9:
        title = 'デザイン'
    elif int(eval_id) == 10:
        title = '評価'
    elif int(eval_id) == 11:
        title = '機能'
    elif int(eval_id) == 12:
        title = '通信量'
    elif int(eval_id) == 13:
        title = '便利さ'
    return render_template('compare_app.html', title=title, apps=apps, entries=entries)

if __name__ == '__main__':
    app.run(port=9000, debug=True)
