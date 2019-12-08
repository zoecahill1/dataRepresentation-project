#!flask/bin/python
from flask import Flask, jsonify, request, abort, make_response
from functools import wraps
from movieDAO import movieDAO

app = Flask(__name__,
            static_url_path='',
            static_folder='.')

def auth_required(f):


    @wraps(f)
    def decorated(*args, **kwargs):
        
        auth = request.authorization

        if auth and auth.username == "admin" and auth.password == "1234":
            return f(*args, **kwargs)

        return make_response('Could not verify your login', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    
    return decorated



#curl "http://127.0.0.1:5000/movies"
@app.route('/movies')
@auth_required
def get_movies():
    #print("in getall")
    results = movieDAO.getAll()
    return jsonify(results)


#curl "http://127.0.0.1:5000/movies/2"
@app.route('/movies/<string:name>')
@auth_required
def get_movie(name):
    foundmovies = movieDAO.get_movie(name)

    return jsonify(foundmovies)

    
    
#curl "http://127.0.0.1:5000/movies/2"
@app.route('/movies/<int:id>')
@auth_required
def findById(id):
    foundmovies = movieDAO.findByID(id)

    return jsonify(foundmovies)


#curl  -i -H "Content-Type:application/json" -X POST -d "{\"name\":\"hello\",\"genre\":\"Drama\",\"description\":\"hello\",\"totalVotes\":123}" http://127.0.0.1:5000/movies
@app.route('/movies', methods=['POST'])
@auth_required
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    movie = {
        "name":  request.json['name'],
        "genre": request.json['genre'],
        "description":request.json['description'],
        "totalVotes":0
    }
    
    values =(movie['name'],movie['genre'],movie['description'],movie['totalVotes'])
    newId = movieDAO.create(values)
    movie['id'] = newId
    return jsonify(movie)



#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"name\":\"another\",\"genre\":\"Comedy\",\"description\":\"new\",\"totalVotes\":11}" http://127.0.0.1:5000/movies/hello
@app.route('/movies/<string:name>', methods=['PUT'])
@auth_required
def update_movie(name):
    foundmovie = movieDAO.get_movie(name)
    print(foundmovie)
    if not foundmovie:
        print(name)
        print('no mmmooovie')
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'totalVotes' in reqJson and type(reqJson['totalVotes']) is not int:
        abort(400)

    #if 'id' in reqJson:
     #   foundmovie['id'] = reqJson['id']
    if 'name' in reqJson:
        foundmovie['name'] = reqJson['name']
    if 'genre' in reqJson:
        foundmovie['genre'] = reqJson['genre']
    if 'description' in reqJson:
        foundmovie['description'] = reqJson['description']
    if 'totalVotes' in reqJson:
        foundmovie['totalVotes'] = reqJson['totalVotes']
    values = (foundmovie['name'],foundmovie['genre'],foundmovie['description'],foundmovie['totalVotes'],foundmovie['id'])
    movieDAO.update_movie(values)
    return jsonify(foundmovie)


    

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"name\":\"another\",\"genre\":\"Comedy\",\"description\":\"new\",\"totalVotes\":11}" http://127.0.0.1:5000/movies/1

@app.route('/votes/<int:id>', methods=['PUT'])
@auth_required
def addVote(id):
    foundmovie = movieDAO.findID(id)

    if not foundmovie:
        print(name)
        print('no mmmooovie')
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json

    if 'id' in reqJson:
        foundmovie['id'] = reqJson['id']

    Newvote = request.json['votes']

    values =(Newvote, int(foundmovie[0]))
    movieDAO.addVote(values)
    return jsonify(foundmovie)


#curl "http://127.0.0.1:5000/votes/leaderboard"

@app.route('/votes/leaderboard')
def getleaderBoard():
    results = movieDAO.getAll()
#ut.sort(key=lambda x: x.count, reverse=True)
    results.sort(key=lambda x: x['totalVotes'], reverse=True)
    #results.sort(key=lambda x: x['totalVotes'], reverse=True)
    return jsonify(results)


@app.route('/movies/<string:name>' , methods=['DELETE'])
@auth_required
def delete(name):
    movieDAO.delete(name)
    return jsonify({"done":True})


@app.errorhandler(404)
def not_found404(error):
    return make_response( jsonify( {'error':'Not found' }), 404)

@app.errorhandler(400)
def not_found400(error):
    return make_response( jsonify( {'error':'Bad Request' }), 400)


if __name__ == '__main__' :
    app.run(debug = True)