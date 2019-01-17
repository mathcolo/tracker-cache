# Define what a new train is
train_is_new_func = {
    'Red': lambda x: int(x) >= 1900,
    'Orange': lambda x: int(x) >= 1400,
    'Green-B': lambda x: int(x) >= 3900 and int(x) <= 3924,
    'Green-C': lambda x: int(x) >= 3900 and int(x) <= 3924,
    'Green-D': lambda x: int(x) >= 3900 and int(x) <= 3924,
    'Green-E': lambda x: int(x) >= 3900 and int(x) <= 3924
}

train_is_new_func_test = {
    'Red': lambda x: int(x) >= 1880,
    'Orange': lambda x: int(x) >= 1300,
    'Green-B': lambda x: int(x) >= 3894,
    'Green-C': lambda x: int(x) >= 3894,
    'Green-D': lambda x: int(x) >= 3894,
    'Green-E': lambda x: int(x) >= 3894
}

def car_is_new(route_name, car):
    return train_is_new_func[route_name](car)

def car_array_is_new(route_name, arr):
    return any(map(train_is_new_func[route_name], arr))
