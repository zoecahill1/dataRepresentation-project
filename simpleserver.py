#!flask/bin/python
from flask import Flask, jsonify,  request, abort, make_response

app = Flask(__name__,
            static_url_path='',
            static_folder='.')

# JSON where inital weathers are coming from
weathers = [
    {
        "town":"Loughrea",
        "country":"Ireland",
        "description":"Mild and cool day",
        "temp":9
    },
    {
        "town":"New York",
        "country":"United States",
        "description":"Frezzing cold, very icy",
        "temp":2
    },
    {
        "town":"Paris",
        "country":"France",
        "description":"Raining Alot",
        "temp":6
    }
]

@app.route('/weathers', methods=['GET'])
def get_weathers():
    return jsonify( {'weathers' : weathers})

@app.route('/weathers/<string:town>', methods =['GET'])
def get_weather(town):
    foundweathers = list(filter(lambda t : t['town'] == town , weathers))
    if len(foundweathers) == 0:
        return jsonify( { 'weather' : '' }),204
    return jsonify( { 'weather' : foundweathers[0] })

@app.route('/weathers', methods=['POST'])
def create_weather():
    if not request.json:
        abort(400)
    if not 'town' in request.json:
        abort(400)
    weather={
        "town":  request.json['town'],
        "country": request.json['country'],
        "description":request.json['description'],
        "temp":request.json['temp']
    }
    weathers.append(weather)
    return jsonify( {'weather':weather }),201


@app.route('/weathers/<string:town>', methods =['PUT'])
def update_weather(town):
    foundweathers=list(filter(lambda t : t['town'] ==town, weathers))
    if len(foundweathers) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'country' in request.json and type(request.json['country']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'temp' in request.json and type(request.json['temp']) is not int:
        abort(400)
    foundweathers[0]['country']  = request.json.get('country', foundweathers[0]['country'])
    foundweathers[0]['description'] =request.json.get('description', foundweathers[0]['description'])
    foundweathers[0]['temp'] =request.json.get('temp', foundweathers[0]['temp'])
    return jsonify( {'weather':foundweathers[0]})



@app.route('/weathers/<string:town>', methods =['DELETE'])
def delete_weather(town):
    foundweathers = list(filter (lambda t : t['town'] == town, weathers))
    if len(foundweathers) == 0:
        abort(404)
    weathers.remove(foundweathers[0])
    return  jsonify( { 'result':True })



@app.errorhandler(404)
def not_found404(error):
    return make_response( jsonify( {'error':'Not found' }), 404)

@app.errorhandler(400)
def not_found400(error):
    return make_response( jsonify( {'error':'Bad Request' }), 400)


if __name__ == '__main__' :
    app.run(debug = True)