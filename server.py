import redis
import json
import flask

routes = ['Red', 'Orange', 'Green-B', 'Green-C', 'Green-D', 'Green-E']

app = flask.Flask(__name__)
redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0, charset="utf-8", decode_responses=True)

@app.route("/puller/status2")
def status2():
    returns = [json.loads(x) for x in redis_conn.mget(*routes)]
    data = {routes[i]: returns[i] for i in range(0, len(routes))}

    # Fix the green line
    data['Green'] = data['Green-B'] + data['Green-C'] + data['Green-D'] + data['Green-E']
    data.pop('Green-B', None)
    data.pop('Green-C', None)
    data.pop('Green-D', None)
    data.pop('Green-E', None)


    # Past data
    data_log = json.loads(redis_conn.get('log'))

    response_json = {
        'current': data,
        'past': data_log
    }

    response = flask.Response(json.dumps(response_json))
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)