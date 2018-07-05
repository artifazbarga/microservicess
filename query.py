from flask import Flask, render_template
import sqlite3
from services import root_dir
app = Flask(__name__)
MOVIES_DB = "C:\\Users\HP\Desktop\db\database.db".format(root_dir())
test = None


def insert(table, record):
    con = sqlite3.connect(MOVIES_DB, isolation_level=None)
    cur = con.cursor()
    cur.execute("INSERT INTO "+table+" values (?,?,?,?)", record)


def Insbooking(table, record):
    con = sqlite3.connect(MOVIES_DB, isolation_level=None)
    cur = con.cursor()
    cur.execute("INSERT INTO "+table+" values (?,?,?)", record)


def find(p):
    con = sqlite3.connect(MOVIES_DB, isolation_level=None)
    cur = con.cursor()
    cur.execute("SELECT * from Users WHERE pass=? and id= ?",p)
    y=cur.fetchall()
    print(len(y))
    return len(y) is not 0


def apdatelastactive(p, record):
    con = sqlite3.connect(MOVIES_DB, isolation_level=None)
    cur = con.cursor()
    print(p)
    print(record)
    cur.execute("UPDATE users SET last_active =? WHERE ID = ?", (p, record))


def delete(table, uid):
    con = sqlite3.connect(MOVIES_DB, isolation_level=None)
    cur = con.cursor()
    cur.execute("DELETE FROM " + table + " WHERE ID = ?", uid)


def exists(table, uid):
    con = sqlite3.connect(MOVIES_DB, isolation_level=None)
    cur = con.cursor()
    cur.execute("SELECT * from "+table+" WHERE ID = ?", uid)
    return len(cur.fetchall())is not 0


def existsfor(table, uid):
    con = sqlite3.connect(MOVIES_DB)
    cur = con.cursor()
    cur.execute("SELECT  id from "+table)
    data = cur.fetchall()
    found = 0
    for item in data:
        if format(item) == format(uid):
            found = 1
    return found


def querydatabase(table, html):
    con = sqlite3.connect(MOVIES_DB)
    cur = con.cursor()
    cur.execute("SELECT *from "+table)
    test = cur.fetchall()
    des = cur.description
    return render_template(html, items=test, des=des)


def querydatabasebyID(table, html, id):
    con = sqlite3.connect(MOVIES_DB)
    cur = con.cursor()
    cur.execute("SELECT * from "+table+" WHERE id_user = "+id)
    test = cur.fetchall()
    des = cur.description
    return render_template(html, items=test, des=des)


def getinbyid(table, id=id):
    con = sqlite3.connect(MOVIES_DB)
    cur = con.cursor()
    id1= format(id)
    cur.execute("SELECT * from "+table+" WHERE id = "+  id1)
    test = cur.fetchall()
    return test


def update(table, record):
    con = sqlite3.connect(MOVIES_DB, isolation_level=None)
    cur = con.cursor()
    cur.execute("UPDATE " + table + " SET RATING = ? WHERE ID = ?", record)


def three_max():
    con = sqlite3.connect(MOVIES_DB)
    cur = con.cursor()
    cur.execute("SELECT rating from MOVIES")
    test = cur.fetchall()
    max3 = sorted(test, reverse=True)[:3]
    print(max3)
    return max3


def getnameuser(table, p):
    con = sqlite3.connect(MOVIES_DB)
    cur = con.cursor()
    cur.execute("SELECT * from " + table + " WHERE id = " + p)
    test = cur.fetchall()
    print(test)
    return test

if __name__ == "__main__":
    app.run()