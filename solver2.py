import pandas as pd

def load_data():
    data_heroes = pd.read_csv('data_heroes.csv')
    data_objects = pd.read_csv('data_objects.csv')
    dist_start = pd.read_csv('dist_start.csv')
    dist_objects = pd.read_csv('dist_objects.csv', header=None)
    dist_objects = dist_objects.apply(pd.to_numeric, errors='coerce')

    return data_heroes, data_objects, dist_start, dist_objects

def improved_greedy_algorithm(data_heroes, data_objects, dist_start, dist_objects, visit_cost=100):
    data_objects = data_objects.sort_values(by='day_open')

    visited_objects = set()

    routes = {}

    for _, hero in data_heroes.iterrows():
        hero_id = hero['hero_id']
        move_points = hero['move_points']
        current_day = 1
        current_location = 0  
        route = []

        while current_day <= 7:
            daily_points = move_points

            while daily_points > 0:
                nearest_mill = None
                min_distance = float('inf')

                for _, mill in data_objects.iterrows():
                    mill_id = mill['object_id']
                    day_open = mill['day_open']

                    if mill_id not in visited_objects and day_open == current_day:
                        if current_location == 0:
                            distance = dist_start[dist_start['object_id'] == mill_id]['dist_start'].values[0]
                        else:
                            distance = dist_objects.iloc[current_location-1, mill_id-1]

                        if distance < min_distance:
                            min_distance = distance
                            nearest_mill = mill_id

                if nearest_mill is not None:

                    if daily_points >= min_distance + visit_cost:

                        route.append(nearest_mill)
                        visited_objects.add(nearest_mill)
                        daily_points -= (min_distance + visit_cost)
                        current_location = nearest_mill
                    elif 1 <= daily_points < visit_cost:

                        route.append(nearest_mill)
                        visited_objects.add(nearest_mill)
                        daily_points = 0
                        current_location = nearest_mill
                    else:
      
                        daily_points = 0
                else:

                    daily_points = 0


            current_day += 1


        routes[hero_id] = route

    return routes

def save_solution(routes):

    route_list = []
    for hero_id, route in routes.items():
        for object_id in route:
            route_list.append({'hero_id': hero_id, 'object_id': object_id})


    solution_df = pd.DataFrame(route_list)


    solution_df.to_csv('solution_improved.csv', index=False)
    print("Solution saved to solution_improved.csv")

def main():
    data_heroes, data_objects, dist_start, dist_objects = load_data()
    routes = improved_greedy_algorithm(data_heroes, data_objects, dist_start, dist_objects)
    save_solution(routes)

if __name__ == "__main__":
    main()

