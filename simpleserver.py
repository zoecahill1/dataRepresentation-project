#!flask/bin/python
from flask import Flask, jsonify,  request, abort, make_response
from movieDAO import movieDAO

app = Flask(__name__,
            static_url_path='',
            static_folder='.')

# JSON where inital movies are coming from
#movies = [
 #   {
  #      "id": 0,
   #     "name":"Avengers: Endgame",
    #    "genre":"Action & Adventure",
    #    "description":"The grave course of events set in motion by Thanos that wiped out half the universe and fractured the Avengers ranks compels the remaining Avengers to take one final stand in Marvel Studios' grand conclusion to twenty-two films, Avengers: Endgame.",
    #    "totalVotes":9
    #},
    #{
    #    "id": 1,
    #    "name":"The Wizard of Oz",
    #    "genre":"Classics",
    #    "description":"L. Frank Baum's classic tale comes to magisterial Technicolor life! The Wizard of Oz stars legendary Judy Garland as Dorothy, an innocent farm girl whisked out of her mundane earthbound existence into a land of pure imagination. Dorothy's journey in Oz will take her through emerald forests, yellow brick roads, and creepy castles, all with the help of some unusual but earnest song-happy friends",
    #    "totalVotes":2
    #},
    #{
    #    "id": 2,
    #    "name":"Dunkirk",
    #    "genre":"Drama",
    #    "description":"Acclaimed auteur Christopher Nolan directs this World War II thriller about the evacuation of Allied troops from the French city of Dunkirk before Nazi forces can take hold. Tom Hardy, Kenneth Branagh and Mark Rylance co-star, with longtime Nolan collaborator Hans Zimmer providing the score.",
    #    "totalVotes":6
    #}
#]

#nextId=3


#curl "http://127.0.0.1:5000/movies"
@app.route('/movies')
def get_movies():
    #print("in getall")
    results = movieDAO.getAll()
    return jsonify(results)


#@app.route('/movies', methods=['GET'])
#def get_movies():
#    return jsonify( {'movies' : movies})

#curl "http://127.0.0.1:5000/movies/2"
@app.route('/movies/<string:name>')
def get_movie(name):
    foundmovies = movieDAO.get_movie(name)

    return jsonify(foundmovies)

#@app.route('/movies/<string:name>', methods =['GET'])
#def get_movie(name):
#    foundmovies = list(filter(lambda t : t['name'] == name , movies))
#    if len(foundmovies) == 0:
#        return jsonify( { 'movie' : '' }),204
#    return jsonify( { 'movie' : foundmovies[0] })
    
    
#curl "http://127.0.0.1:5000/movies/2"
@app.route('/movies/<int:id>')
def findById(id):
    foundmovies = movieDAO.findByID(id)

    return jsonify(foundmovies)

#@app.route('/movies/<int:id>')
#def findById(id):
#   foundmovies = list(filter(lambda t: t['id'] == id, movies))
#     if len(foundmovies) == 0:
#        return jsonify ({}) , 204

#    return jsonify(foundmovies[0])

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"name\":\"hello\",\"genre\":\"Drama\",\"description\":\"hello\",\"totalVotes\":123}" http://127.0.0.1:5000/movies
@app.route('/movies', methods=['POST'])
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


#@app.route('/movies', methods=['POST'])
#def create_movie():
#    global nextId
#    if not request.json:
#        abort(400)
#    if not 'name' in request.json:
#        abort(400)
#    movie={
#        "id": nextId,
#        "name":  request.json['name'],
#        "genre": request.json['genre'],
#        "description":request.json['description'],
#        "totalVotes":0
#    }
    
#    nextId+=1
#    movies.append(movie)
#    return jsonify({'movie':movie }),201




#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"name\":\"another\",\"genre\":\"Comedy\",\"description\":\"new\",\"totalVotes\":11}" http://127.0.0.1:5000/movies/hello
@app.route('/movies/<string:name>', methods=['PUT'])
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




#@app.route('/movies/<string:name>', methods =['PUT'])
#def update_movie(name):
#    foundmovies=list(filter(lambda t : t['name'] ==name, movies))
#    if len(foundmovies) == 0:
#        abort(404)
#    if not request.json:
#        abort(400)
#    if 'genre' in request.json and type(request.json['genre']) != str:
#        abort(400)
#    if 'description' in request.json and type(request.json['description']) is not str:
#        abort(400)
#    if 'totalVotes' in request.json and type(request.json['totalVotes']) is not int:
#        abort(400)
#    foundmovies[0]['genre']  = request.json.get('genre', foundmovies[0]['genre'])
#    foundmovies[0]['description'] =request.json.get('description', foundmovies[0]['description'])
#    foundmovies[0]['totalVotes'] =request.json.get('totalVotes', foundmovies[0]['totalVotes'])
#    return jsonify( {'movie':foundmovies[0]})

    
@app.route('/votes/<int:movieid>', methods = ['POST'])
def addVote(movieid):
    foundmovies=list(filter(lambda t : t['id']==movieid, movies))
    if len(foundmovies)== 0:
        abort(404)
    if not request.json:
        abort(400)
    if not 'votes' in request.json or type(request.json['votes']) is not int:
        abort(401)
    Newvote = request.json['votes']
    
    foundmovies[0]['totalVotes'] += Newvote
    return jsonify(foundmovies[0])


@app.route('/votes/leaderboard')
def getleaderBoard():
#ut.sort(key=lambda x: x.count, reverse=True)
    movies.sort(key=lambda x: x['totalVotes'], reverse=True)

    return jsonify(movies)



@app.route('/movies/<string:name>', methods =['DELETE'])
def delete_movie(name):
    foundmovies = list(filter (lambda t : t['name'] == name, movies))
    if len(foundmovies) == 0:
        abort(404)
    movies.remove(foundmovies[0])
    return  jsonify( { 'result':True })


@app.errorhandler(404)
def not_found404(error):
    return make_response( jsonify( {'error':'Not found' }), 404)

@app.errorhandler(400)
def not_found400(error):
    return make_response( jsonify( {'error':'Bad Request' }), 400)


if __name__ == '__main__' :
    app.run(debug = True)