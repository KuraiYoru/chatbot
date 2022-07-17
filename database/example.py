import sqlite3 as sq
import random
import json

def sql_start():
    global base, cur
    base = sq.connect('base.db')
    cur = base.cursor()
    base.commit()


def register(user_id):
    dictionary = {'name': '', 'age': '', 'liked_id': f'{json.dumps([])}', 'current_id': '', 'teg': ''}
    dictionary = json.dumps(dictionary)
    data = []
    lst = cur.execute(f"SELECT id_user from pro_users")
    for row in lst.fetchall():
        data.append(row[0])
    if str(user_id) not in data:
        cur.execute("INSERT INTO pro_users(id_user, user_info) VALUES(?)", (user_id, dictionary,))
        base.commit()



def send_profile(user_id):
    data = next(cur.execute(f"select * from users where id_user = ?", (user_id,)))
    base.commit()
    return data


# def add_user(id):
#     data = next(cur.execute(f"SELECT liked_id from users where id_user = ?", (id,)))
#     cur.execute(f"UPDATE users SET liked_id = ? where id_user = ?", (lst, id,))

sql_start()

def all_id():
    data = cur.execute(f"select id_user from users").fetchall()
    base.commit()
    return data
def liked_person():
    data = next(cur.execute(f"select liked_id from users"))[0]
    print(data)

def get_liked(id):
    data = next(cur.execute(f"select liked_id from users where id_user = ?", (id, )))[0]
    base.commit()
    data = json.loads(data)
    return data

sql_start()
cur.execute('CREATE TABLE pro_users(smth INT)')
base.commit()