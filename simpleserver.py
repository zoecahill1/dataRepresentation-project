#!flask/bin/python
from flask import Flask, jsonify, request, abort, make_response
from functools import wraps
from movieDAO import movieDAO

app = Flask(__name__,
            static_url_path='',
            static_folder='.')

# Only users with correct usersname and password can access admin features
# such as creating or deleting entries


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth = request.authorization
        # Username and password set here
        if auth and auth.username == "admin" and auth.password == "1234":
            return f(*args, **kwargs)

        return make_response('Could not verify your login', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated

# Gets the top 100 movies
@app.route('/top')
def get_top():
    results = movieDAO.gettop()
    return jsonify(results)

# Get all movies
@app.route('/movies')
@auth_required
def get_movies():
    results = movieDAO.getAll()
    return jsonify(results)

# Get movie by name
@app.route('/movies/<string:name>')
@auth_required
def get_movie(name):
    foundmovies = movieDAO.get_movie(name)

    return jsonify(foundmovies)


# Get movie by ID
@app.route('/movies/<int:id>')
@auth_required
def findById(id):
    foundmovies = movieDAO.findByID(id)

    return jsonify(foundmovies)


# Create movie
@app.route('/movies', methods=['POST'])
@auth_required
def create():

    if not request.json:
        abort(400)
    # other checking
    movie = {
        "name":  request.json['name'],
        "genre": request.json['genre'],
        "description": request.json['description'],
        "totalVotes": 0
    }

    values = (movie['name'], movie['genre'],
              movie['description'], movie['totalVotes'])
    newId = movieDAO.create(values)
    movie['id'] = newId
    return jsonify(movie)


# Update movie by name
@app.route('/movies/<string:name>', methods=['PUT'])
@auth_required
def update_movie(name):
    foundmovie = movieDAO.get_movie(name)
    if not foundmovie:
        abort(404)
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'totalVotes' in reqJson and type(reqJson['totalVotes']) is not int:
        abort(400)
    if 'name' in reqJson:
        foundmovie['name'] = reqJson['name']
    if 'genre' in reqJson:
        foundmovie['genre'] = reqJson['genre']
    if 'description' in reqJson:
        foundmovie['description'] = reqJson['description']
    if 'totalVotes' in reqJson:
        foundmovie['totalVotes'] = reqJson['totalVotes']
    values = (foundmovie['name'], foundmovie['genre'],
              foundmovie['description'], foundmovie['totalVotes'], foundmovie['id'])
    movieDAO.update_movie(values)
    return jsonify(foundmovie)


# Add votes by ID
@app.route('/votes/<int:id>', methods=['PUT'])
@auth_required
def addVote(id):
    foundmovie = movieDAO.findID(id)
    if not foundmovie:
        abort(404)
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'id' in reqJson:
        foundmovie['id'] = reqJson['id']

    Newvote = request.json['votes']

    values = (Newvote, int(foundmovie[0]))
    movieDAO.addVote(values)
    return jsonify(foundmovie)

# Get leaderboard
@app.route('/votes/leaderboard')
def getleaderBoard():
    results = movieDAO.getAll()
    # Sort votes highest to lowest
    results.sort(key=lambda x: x['totalVotes'], reverse=True)
    return jsonify(results)

# Delete movies by name
@app.route('/movies/<string:name>', methods=['DELETE'])
@auth_required
def delete(name):
    movieDAO.delete(name)
    return jsonify({"done": True})


@app.errorhandler(404)
def not_found404(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def not_found400(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.run(debug=True)
