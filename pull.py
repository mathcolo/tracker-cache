import redis
import API
import datetime
import json as JSON
from Fleet import car_array_is_new

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
routes = ['Red', 'Orange', 'Green-B', 'Green-C', 'Green-D', 'Green-E']

json = API.getV3('vehicles', 'route', ','.join(routes), suffix='&include=stop')

# Create a data structure that maps station ids to station names, which are included in the API payload
stop_ids_to_names = {x['id'] : x['attributes']['name'] for x in json['included']}


# Transform all of the current vehicles into easy-to-use form
all_vehicles = {x: [] for x in routes}

seen_trip_ids = []
for vehicle in json['data']:
    route_name = vehicle['relationships']['route']['data']['id']
    if vehicle['relationships']['trip']['data']['id'] not in seen_trip_ids:
        # Dedup trip ids
        seen_trip_ids.append(vehicle['relationships']['trip']['data']['id'])
        # try:
        all_vehicles[route_name].append({
            'trip_id': vehicle['relationships']['trip']['data']['id'],
            'cars': vehicle['attributes']['label'].split('-'),
            # 'cars': ['3800', '3801', '3802'],
            'cars_new_flag': car_array_is_new(route_name, vehicle['attributes']['label'].split('-')),
            'status': vehicle['attributes']['current_status'],
            'stop_id': vehicle['relationships']['stop']['data']['id'],
            'stop_name': stop_ids_to_names[vehicle['relationships']['stop']['data']['id']],
            'direction': vehicle['attributes']['direction_id']
        })
        # except TypeError:
        #     print('vehicle error: {}'.format(vehicle))

for route_name in routes:
    new_trains_on_route = list(all_vehicles[route_name])
    redis_conn.set(route_name, JSON.dumps(new_trains_on_route))
    redis_conn.expireat(route_name, datetime.datetime.combine(datetime.datetime.today() + datetime.timedelta(1), datetime.time.min))
