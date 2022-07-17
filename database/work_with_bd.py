import json
import sqlite3 as sq


def sql_start():
    global base, cur
    base = sq.connect('.\\database\\base.db')
    cur = base.cursor()
    base.commit()

def register(user_id):
    dictionary = {'name': '', 'age': '', 'liked_id': [], 'current_id': '', 'teg': ''}
    dictionary = json.dumps(dictionary)
    data = []
    lst = cur.execute(f"SELECT id_user from pro_users")
    for row in lst.fetchall():
        data.append(str(row[0]))
    if str(user_id) not in data:
        cur.execute("INSERT INTO pro_users(id_user, user_info) VALUES(?, ?)", (user_id, dictionary,))
        base.commit()


def set_info(photo, desc, user_id, name, age, teg):
    data = next(cur.execute('SELECT user_info from pro_users where id_user = ?', (user_id,)))[0]
    data = json.loads(data)
    data['name'] = name
    data['age'] = age
    data['teg'] = teg
    data = json.dumps(data)
    cur.execute('UPDATE pro_users SET picture = ?, description = ?, user_info = ? where id_user = ?', (photo, desc, data, user_id,))
    base.commit()

def send_profile(user_id):
    data = next(cur.execute(f"select * from pro_users where id_user = ?", (user_id,)))
    base.commit()
    return data

def all_id():
    data = cur.execute(f"select id_user from pro_users").fetchall()
    base.commit()
    return list(map(lambda x: x[0], data))


def liked_person(user_id, liked_id):
    data = next(cur.execute(f"select user_info from pro_users where id_user = ?", (user_id, )))[0]
    data = json.loads(data)
    data['liked_id'].append(str(liked_id))
    data['liked_id'] = list(set(data['liked_id']))
    data = json.dumps(data)
    cur.execute(f"UPDATE pro_users SET user_info = ? where id_user = ?", (data, user_id,))
    base.commit()


def get_liked(user_id):
    data = next(cur.execute(f"select user_info from pro_users where id_user = ?", (user_id, )))[0]
    base.commit()
    data = json.loads(data)
    data = data['liked_id']
    return data


def set_current_id(like_id, user_id):
    data = next(cur.execute('SELECT user_info from pro_users where id_user = ?', (user_id,)))[0]
    base.commit()
    data = json.loads(data)
    data['current_id'] = str(like_id)
    data = json.dumps(data)
    cur.execute('UPDATE pro_users SET user_info = ? where id_user = ?', (data, user_id,))
    base.commit()


def get_current_id(user_id):
    data = next(cur.execute(f"SELECT user_info from pro_users where id_user = ?", (user_id,)))[0]
    base.commit()
    data = json.loads(data)
    return data['current_id']


def check_register(user_id):
    data = next(cur.execute(f"SELECT user_info from pro_users where id_user = ?", (user_id,)))[0]
    base.commit()
    data = json.loads(data)
    if data['teg'] == '@None':
        return False
    return data['teg']


# sql_start()
# print(cur.execute(f"SELECT description from users where id_user = 748045404"))

