# -*- coding: utf-8

import sqlite3

dbname = 'database.db'

conn = sqlite3.connect(dbname)
c = conn.cursor()

# # executeメソッドでSQL文を実行する
# create_table = '''CREATE TABLE IF NOT EXISTS review (id integer PRIMARY KEY AUTOINCREMENT, app_id integer,
#                                         rate real, date text, title text,
#                                         review text, ad real, article real,
#                                         crash real, design real, fav real, func real,
#                                         traffic real, useful real)'''
#
# c.execute(create_table)
# #
# # SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
# # セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値を
# # タプルで渡す．
#
create_table = '''CREATE TABLE IF NOT EXISTS app(id integer PRIMARY KEY AUTOINCREMENT, name text,
                                        icon text, rate real, num_review int, ad real, num_ad int, article real,
                                        num_article int,crash real, num_crash int, design real, num_design int,
                                        fav real, num_fav int, func real, num_func int,traffic real, num_traffic int,
                                        useful real, num_useful int)'''

c.execute(create_table)
insert_sql = 'insert into app(name , icon, rate, num_review, ad, num_ad, article, num_article, crash, num_crash, ' \
             'design, num_design, fav, num_fav, func, num_func, traffic, num_traffic, useful, num_useful) ' \
             'values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
apps = [
    ("smartnews", "./static/images/smartnews.png", 4.15, 1792, 1.26, 61, 4.24, 213, 1.55, 41, 448, 118, 3.97, 596, 2.09, 70,
     2.22, 9, 3.96, 394),
    ("yahoo", "./static/images/yahoo.png", 3.11, 860, 1.46, 10, 4.26, 31, 1.36, 93, 4.16, 22, 3.60, 237, 1.15, 81, 2.00, 3,
     3.54, 168),
    ("gunosy", "./static/images/gunosy.png", 3.39, 142, 1.50, 2, 3.87, 13, 2.00, 2, 4.00, 4, 3.90, 31, 2.00, 1, 0.00, 0,
     3.71, 14),
    ("newspass", "./static/images/newspass.png", 3.40, 126, 0.00, 0, 3.88, 4, 1.33, 3, 4.83, 6, 3.88, 40, 1.00, 0, 0.00, 0,
     3.76, 19)
]
c.executemany(insert_sql, apps)
conn.commit()
conn.close()