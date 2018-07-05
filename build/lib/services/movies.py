import uuid

from services import root_dir, nice_json
from flask import Flask, request
from werkzeug.exceptions import NotFound
import json

app = Flask(__name__)

ROOT_MOVIES = {"uri": "/", "subresource_uris": {"movies": "/movies", "movie": "/movies/<id>"}}
MOVIES_JSON = "{}/database/movies.json".format(root_dir())


def get_movies(movie_id=None):
    with open(MOVIES_JSON, "r") as f:
        movies = json.load(f)
        if movie_id is None:
            return movies
        else:
            return movies[movie_id]


get_movies()


@app.route("/", methods=['GET'])
def root():
    return nice_json(ROOT_MOVIES)


@app.route("/movies/<movieid>", methods=['GET'])
def movie_info(movieid):
    if movieid not in get_movies():
        raise NotFound

    result = get_movies(movieid)
    result["uri"] = "/movies/{}".format(movieid)

    return nice_json(result)


@app.route("/movies", methods=['GET', 'POST'])
def movie_record():
    if request.method == 'POST':
        id = str(uuid.uuid4())
        movie = {'title': request.form['title'],
                 'id': id,
                 'rating': request.form['rating'],
                 'director': request.form['director']}

        data = get_movies()

        data.update({id: movie})

        with open(MOVIES_JSON, 'w') as f:
            json.dump(data, f, sort_keys=True, indent=4)

    return nice_json(get_movies())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
