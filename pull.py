import redis
import API
import datetime
import json as JSON
# import psycopg2
# import psycopg2.extras
from Fleet import car_array_is_new

redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
routes = ['Red', 'Orange', 'Green-B', 'Green-C', 'Green-D', 'Green-E']

# postgres_conn = psycopg2.connect(host='localhost', dbname="postgres", user="postgres", password="postgres")
# DB_LOG_TABLE_NAME = 'newtrains_history'
json = API.getV3('vehicles', 'route', ','.join(routes), suffix='&include=stop')

# Create a data structure that maps station ids to station names, which are included in the API payload
stop_ids_to_names = {x['id'] : x['attributes']['name'] for x in json['included']}

# Transform all of the current vehicles into easy-to-use form
vehicles_by_route = {x: [] for x in routes}
seen_trip_ids = []
for vehicle in json['data']:
    route_name = vehicle['relationships']['route']['data']['id']
    if vehicle['relationships']['trip']['data']['id'] not in seen_trip_ids:
        # Dedup trip ids
        seen_trip_ids.append(vehicle['relationships']['trip']['data']['id'])
        # try:
        vehicle_output = {
            'trip_id': vehicle['relationships']['trip']['data']['id'],
            'cars': vehicle['attributes']['label'].split('-'),
            'cars_new_flag': car_array_is_new(route_name, vehicle['attributes']['label'].split('-')),
            'status': vehicle['attributes']['current_status'],
            'direction': vehicle['attributes']['direction_id']
        }
        # Sometimes the stop data isn't present, so we (optionally) add it in
        if vehicle['relationships']['stop']['data']:
            vehicle_output['stop_id'] = vehicle['relationships']['stop']['data']['id']
            vehicle_output['stop_name'] = stop_ids_to_names[vehicle['relationships']['stop']['data']['id']]

        vehicles_by_route[route_name].append(vehicle_output)
        # except KeyError:
        #     breakpoint()
        #     print('vehicle error: {}'.format(vehicle))

for route_name in routes:
    new_trains_on_route = list(vehicles_by_route[route_name])
    redis_conn.set(route_name, JSON.dumps(new_trains_on_route))
    redis_conn.expireat(route_name, datetime.datetime.combine(datetime.datetime.today() + datetime.timedelta(1), datetime.time.min))

# Add to PostgreSQL log
# with postgres_conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
#     # This is a little nasty, but we want to maintain independent db rows for each car in a series (for the green line)
#     for route in routes:
#         for vehicle in vehicles_by_route[route]:
#             for car in vehicle['cars']:
#                 cursor.execute("select * from newtrains_history WHERE car = %s ORDER BY seen_start DESC LIMIT 1", [car])
#                 latest = cursor.fetchone()
#                 if latest and (datetime.datetime.now() - latest['seen_end']).seconds < 1200: # Update the current record
#                     cursor.execute("UPDATE newtrains_history SET seen_end = %s WHERE id = %s", [datetime.datetime.now(), latest['id']])
#                 else:
#                     # Make a new record
#                     cursor.execute("insert into newtrains_history (route, car, seen_start, seen_end) values (%s, %s, %s)", [route, car, datetime.datetime.now()])
#     postgres_conn.commit()