import sqlite3
import uuid
from services import root_dir
import user
from werkzeug.utils import redirect
from flask import Flask, request, render_template, url_for, flash, session
import os, datetime
import query
app = Flask(__name__)
app.secret_key = os.urandom(24)
ROOT_MOVIES = {"uri": "/", "subresource_uris": {"movies": "/movies", "movie": "/movies/<id>"}}
MOVIES_DB = "C:\\Users\HP\Desktop\db\database.db".format(root_dir())

@app.route('/')
def home():
    if not session.get('logged_in'):
     return redirect(url_for("do_login"))
    else:
        if session['name'] == "88" and session['id'] == "admin":
            return "Hello"+session.get("name") + "\n<a href='/logout'>Logout</a><br><br><a id='user' href='/getmovies'>Update_Delete_Add_list_of_movies</a>" \
            "<br><br><a href='/redirect'>Update_Delete_Add_list of users</a>"
        else:
            query.apdatelastactive(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), session.get('name'))
            return "Hello\n" + session['id']+"<br><br><a href='/logout'>Logout</a><br><br><br><a href='/threemax'>three max movies</a> " \
                                        "<br><a id='user' href='/redirect1'>list_movies</a>"




@app.route('/redirect1', methods=['GET','POST'])
def do_re_m():
 return redirect("http://127.0.0.1:5000/getmoviesuser/" + session.get('name'))


@app.route('/redirect', methods=['GET','POST'])
def do_re():
 return redirect('http://127.0.0.1:5000/user')

@app.route('/login', methods=['GET','POST'])
def do_login():
    if request.method =="POST":
        if query.find((request.form['pass'], request.form['uname'])):
            session['logged_in'] = True
            session['name'] = request.form['uname']
            name = query.getnameuser("users", request.form['uname'])
            session['id'] = name[0][1]
            return redirect(url_for("home"))
        else:
            if (request.form['pass'] == "" and request.form['uname'] == ""):
                return redirect(url_for("home"))
            else:
                return "wrong password!"+"<br><br><a href='/'>go to home</a>"
    if request.method =="GET":
        if session.get('logged_in') is not None:
         if session.get('logged_in'):
            redirect(url_for("home"))
    return render_template("login.html")


@app.route('/signup', methods=['GET','POST'])
def sign_up():
    logout()
    if request.method == "POST":
        signup = (request.form['uname'], request.form['nameuser'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), request.form['pass'])
        query.insert("users", signup)
        return redirect(url_for("home"))
    if request.method == "GET":
        redirect(url_for("home"))
    return render_template("signup.html")


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for("do_login"))


@app.route("/remove/<mid>", methods=['GET'])
def movie_remove(mid):
            query.delete("MOVIES", (mid,))
            return redirect(url_for('movie_list'))


@app.route("/rent/<mid>", methods=['GET'])
def movie_rent(mid):
            query.update("MOVIES", (mid,))
            return redirect(url_for('movie_list'))


# @app.route("/removeusers/<mid>", methods=['GET', 'POST'])
# def user_remove(mid):
#     query.delete("users", (mid,))
#     return redirect(url_for('user_list'))


@app.route("/movierank/<mid>", methods=['GET','POST'])
def movie_rank(mid):
    if request.method == "POST":
        if query.exists("MOVIES", (mid,)):
            record = (request.form['rating'],mid)
            query.update('MOVIES', record)
            return redirect(url_for('movie_list'))
    return render_template("movierank.html")


@app.route("/getmovies/")
def movie_list():
    return query.querydatabase("MOVIES", "movietable.html")+"<br><a href='/addmovie' >Add movie</a><br>"+"<br><a href='/logout'>Logout</a><br>"


@app.route("/getmoviesuser/")
def movie_listuser():
    return query.querydatabase("MOVIES", "listforuser.html")+"<br><br><a href='/logout'>Logout</a><br>"

#
# @app.route("/getusers/")
# def user_list():
#     return query.querydatabase("users", "usertable.html")+"<br><a href='/addmovie' >Add movie</a><br>"+"<a href='/addusers'>Add user</a>" +"<br><a href='/logout'>Logout</a><br>"


@app.route("/addmovie/", methods=['GET', 'POST'])
def movie_add():
    if request.method == "POST":
        record = (str(uuid.uuid4()), request.form['title'], request.form['rating'], request.form['director'])
        query.insert('movies', record)
        return redirect(url_for('movie_list'))
    return render_template("addmovie.html")


@app.route("/moviedit/<mid>", methods=['GET','POST'])
def movie_edit(inf):
    if request.method == "POST":
        get = query.getinbyid("movies", (inf,))
        record = (str(uuid.uuid4()),get[1], request.form['rating'] , get[3])
        query.update('movies', record)
        return redirect(url_for('movie_list'))
    return render_template("editmovie.html", inf=inf)


# @app.route("/addusers/", methods=['GET', 'POST'])
# def user_add():
#     if request.method == "POST":
#         record = (request.form['id'], request.form['name'],  datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), request.form['pass'])
#         query.insert('users', record)
#         return redirect(url_for('user_list'))
#     return render_template("addusers.html")
#

@app.route('/threemax', methods=['GET'])
def maxthree():
    con = sqlite3.connect(MOVIES_DB)
    cur = con.cursor()
    three = query.three_max()
    if len(three) > 2:
        cur.execute("SELECT DISTINCT *from MOVIES WHERE rating in (?,?,?)", (format(three[0][0]), format(three[1][0]), format(three[2][0])))

    else:
        if len(three) > 1 and len(three) < 3:
            cur.execute("SELECT DISTINCT *from MOVIES WHERE rating in (?,?,?)",
                        (format(three[0][0]), format(three[1][0]), "the cinema has just two movies"))
        else:
            if len(three) == 1:
                cur.execute("SELECT DISTINCT *from MOVIES WHERE rating in (?,?,?)",
                            (format(three[0][0]), "", "the cinema has just one movies"))
    des = cur.description
    return render_template("listforuser.html", items=cur.fetchall(), des=des)+"<br><br>"




if __name__ == "__main__":
    app.run(port=5001, debug=True)