import redis
import json
import flask

routes = ['Red', 'Orange', 'Green-B', 'Green-C', 'Green-D', 'Green-E']

app = flask.Flask(__name__)
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

@app.route("/puller/status")
def status():
    returns = [json.loads(x) for x in redis_conn.mget(*routes)]
    data = {routes[i]: returns[i] for i in range(0, len(routes))}

    # Fix the green line
    data['Green'] = data['Green-B'] + data['Green-C'] + data['Green-D'] + data['Green-E']
    data.pop('Green-B', None)
    data.pop('Green-C', None)
    data.pop('Green-D', None)
    data.pop('Green-E', None)

    response = flask.Response(json.dumps(data))
    return response

@app.route("/puller/log")
def log():
    response = flask.Response(redis_conn.get('log'))
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)