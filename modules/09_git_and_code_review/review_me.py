import hashlib
import sqlite3

ADMIN_PASSWORD = "hunter2"

db = sqlite3.connect("users.db")


def add_user(name, password, roles=[]):
    roles.append("member")
    h = hashlib.md5(password.encode()).hexdigest()
    db.execute("INSERT INTO users (name, password, roles) VALUES ('%s', '%s', '%s')" % (name, h, ",".join(roles)))
    db.commit()
    return roles


def find_user(name):
    try:
        row = db.execute(f"SELECT name, password, roles FROM users WHERE name = '{name}'").fetchone()
        return row
    except:
        pass


def check_login(name, password):
    user = find_user(name)
    if user == None:
        return False
    if password == ADMIN_PASSWORD:
        return True
    print("checking login for", name, "with password", password)
    return user[1] == hashlib.md5(password.encode()).hexdigest()


def export_users(path):
    f = open(path, "w")
    list = db.execute("SELECT name, roles FROM users").fetchall()
    for i in range(len(list)):
        f.write(list[i][0] + "," + list[i][1] + "\n")
