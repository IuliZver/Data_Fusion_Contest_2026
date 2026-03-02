import pandas as pd

def load_data():
    # Загрузка данных
    data_heroes = pd.read_csv('data_heroes.csv')
    data_objects = pd.read_csv('data_objects.csv')
    dist_start = pd.read_csv('dist_start.csv')

    # Загрузка матрицы расстояний
    dist_objects = pd.read_csv('dist_objects.csv', header=None)
    dist_objects = dist_objects.apply(pd.to_numeric, errors='coerce')

    return data_heroes, data_objects, dist_start, dist_objects

def improved_greedy_algorithm(data_heroes, data_objects, dist_start, dist_objects, visit_cost=100):
    # Сортировка объектов по дню открытия
    data_objects = data_objects.sort_values(by='day_open')

    # Инициализация списка посещенных объектов
    visited_objects = set()

    # Инициализация списка маршрутов
    routes = {}

    # Проход по героям
    for _, hero in data_heroes.iterrows():
        hero_id = hero['hero_id']
        move_points = hero['move_points']
        current_day = 1
        current_location = 0  # Начинаем с замка
        route = []

        # Пока не кончились дни
        while current_day <= 7:
            daily_points = move_points

            # Пока у героя есть очки хода
            while daily_points > 0:
                # Поиск ближайшей доступной мельницы, открытой в текущий день
                nearest_mill = None
                min_distance = float('inf')

                for _, mill in data_objects.iterrows():
                    mill_id = mill['object_id']
                    day_open = mill['day_open']

                    # Если мельница еще не посещена и открыта в текущий день
                    if mill_id not in visited_objects and day_open == current_day:
                        # Расстояние от текущей локации до мельницы
                        if current_location == 0:
                            distance = dist_start[dist_start['object_id'] == mill_id]['dist_start'].values[0]
                        else:
                            distance = dist_objects.iloc[current_location-1, mill_id-1]

                        # Если это ближайшая мельница
                        if distance < min_distance:
                            min_distance = distance
                            nearest_mill = mill_id

                # Если нашли мельницу
                if nearest_mill is not None:
                    # Проверка, хватит ли очков хода
                    if daily_points >= min_distance + visit_cost:
                        # Посещение мельницы
                        route.append(nearest_mill)
                        visited_objects.add(nearest_mill)
                        daily_points -= (min_distance + visit_cost)
                        current_location = nearest_mill
                    elif 1 <= daily_points < visit_cost:
                        # Правило "последнего шага"
                        route.append(nearest_mill)
                        visited_objects.add(nearest_mill)
                        daily_points = 0
                        current_location = nearest_mill
                    else:
                        # Не хватает очков хода, герой ждет на месте
                        daily_points = 0
                else:
                    # Нет доступных мельниц, открытых в текущий день
                    daily_points = 0

            # Конец дня
            current_day += 1

        # Сохранение маршрута
        routes[hero_id] = route

    return routes

def save_solution(routes):
    # Преобразование маршрутов в формат DataFrame
    route_list = []
    for hero_id, route in routes.items():
        for object_id in route:
            route_list.append({'hero_id': hero_id, 'object_id': object_id})

    # Создание DataFrame
    solution_df = pd.DataFrame(route_list)

    # Сохранение в CSV
    solution_df.to_csv('solution_improved.csv', index=False)
    print("Solution saved to solution_improved.csv")

def main():
    data_heroes, data_objects, dist_start, dist_objects = load_data()
    routes = improved_greedy_algorithm(data_heroes, data_objects, dist_start, dist_objects)
    save_solution(routes)

if __name__ == "__main__":
    main()
