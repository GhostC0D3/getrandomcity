import json
import random

class CityPicker:
    def __init__(self, file_path):
        self.cities = []
        self.total_population = 0
        self.__load_data(file_path)

    def __load_data(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            for city_info in data:
                name = city_info.get('name')
                population = city_info.get('population')
                self.cities.append((name, population))
                self.total_population += population

    def __pick_random_city(self):
        random_value = random.random()
        cumulative_prob = 0
        for city, population in self.cities:
            city_prob = population / self.total_population
            cumulative_prob += city_prob
            if random_value <= cumulative_prob:
                return city

    def get_random_city(self):
        return self.__pick_random_city()

if __name__ == "__main__":
    file_path = "input.json"
    city_picker = CityPicker(file_path)
    for city in range(10):
        random_city = city_picker.get_random_city()
        print("Randomly picked city:", random_city)
