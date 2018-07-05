import sqlite3
from services import root_dir ,main
from werkzeug.utils import redirect
from flask import Flask, request, render_template, url_for, flash, session
import os, datetime
import query
from werkzeug.exceptions import NotFound, ServiceUnavailable
import json
import query
import requests


app = Flask(__name__)
app.secret_key = os.urandom(24)

# @app.route("/", methods=['GET'])
# def hello():
#     return nice_json({
#         "uri": "/",
#         "subresource_uris": {
#             "users": "/users",
#             "user": "/users/<username>",
#             "bookings": "/users/<username>/bookings",
#             "suggested": "/users/<username>/suggested"
#         }
#     })


@app.route("/user", methods=['GET'])
def users_list():
    return query.querydatabase("users", "usertable.html")


@app.route("/getmoviesuser/<uid>")
def movie_listuser(uid):
    session["uid"] = uid
    return query.querydatabase("MOVIES", "listforuser.html")+"<br><br><a href='http://127.0.0.1:5001/login'>Logout</a><br>"


@app.route("/addusers/", methods=['GET', 'POST'])
def user_add():
    if request.method == "POST":
        record = (request.form['id'], request.form['name'],  datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), request.form['pass'])
        query.insert('users', record)
        return redirect(url_for('user_list'))
    return render_template("addusers.html")


@app.route("/removeusers/<mid>", methods=['GET', 'POST'])
def user_remove(mid):
    query.delete("users", (mid,))
    return redirect(url_for('users_list'))


# @app.route("/users/<username>", methods=['GET'])
# def user_record(username):
#     if username not in users:
#         raise NotFound
#
#     return "list"
#
#
# @app.route("/users/<username>/bookings", methods=['GET'])
# def user_bookings(username):
#     """
#     Gets booking information from the 'Bookings Service' for the user, and
#      movie ratings etc. from the 'Movie Service' and returns a list.
#     :param username:
#     :return: List of Users bookings
#     """
#     if username not in users:
#         raise NotFound("User '{}' not found.".format(username))
#
#     try:
#         users_bookings = requests.get("http://127.0.0.1:5003/bookings/{}".format(username))
#     except requests.exceptions.ConnectionError:
#         raise ServiceUnavailable("The Bookings service is unavailable.")
#
#     if users_bookings.status_code == 404:
#         raise NotFound("No bookings were found for {}".format(username))
#
#     users_bookings = users_bookings.json()
#
#     # For each booking, get the rating and the movie title
#     result = {}
#     for date, movies in users_bookings.iteritems():
#         result[date] = []
#         for movieid in movies:
#             try:
#                 movies_resp = requests.get("http://127.0.0.1:5001/movies/{}".format(movieid))
#             except requests.exceptions.ConnectionError:
#                 raise ServiceUnavailable("The Movie service is unavailable.")
#             movies_resp = movies_resp.json()
#             result[date].append({
#                 "title": movies_resp["title"],
#                 "rating": movies_resp["rating"],
#                 "uri": movies_resp["uri"]
#             })
#
#     return nice_json(result)
#
#
# @app.route("/users/<username>/suggested", methods=['GET'])
# def user_suggested(username):
#     """
#     Returns movie suggestions. The algorithm returns a list of 3 top ranked
#     movies that the user has not yet booked.
#     :param username:
#     :return: Suggested movies
#     """
#     raise NotImplementedError()


if __name__ == "__main__":
    app.run(port=5000, debug=True)
