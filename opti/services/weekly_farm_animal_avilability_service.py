from collections import defaultdict

from ..models import WeeklyFarmAnimalAvailability

def get_animals_available(week_of_year_selected):
    farmAnimalsAvailable = WeeklyFarmAnimalAvailability.objects.filter(week_of_year=week_of_year_selected)
    animals_available = defaultdict(int)

    for farmAnimalAvailable in farmAnimalsAvailable:
        farm_name = farmAnimalAvailable.farm.name
        animals_available[farm_name] += farmAnimalAvailable.animal_count

    return dict(animals_available)

def get_average_weight(week_of_year_selected):
    availabilities = WeeklyFarmAnimalAvailability.objects.filter(week_of_year=week_of_year_selected)
    average_weight = {}

    for availability in availabilities:
        farm_name = availability.farm.name
        average_weight[farm_name] = availability.average_weight

    return average_weight

def get_all_weekly_farm_animal_availability():
    return WeeklyFarmAnimalAvailability.objects.all()