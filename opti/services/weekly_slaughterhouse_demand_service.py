from collections import defaultdict

from ..models import WeeklySlaughterhouseDemand

def get_demand(week_of_year_selected):
    demands = WeeklySlaughterhouseDemand.objects.filter(week_of_year=week_of_year_selected)
    demand_dict = defaultdict(int)

    for demand in demands:
        slaughterhouse_name = demand.slaughterhouse.name
        demand_dict[slaughterhouse_name] += demand.animal_count

    return dict(demand_dict)

def get_all_weekly_slaughterhouse_demand():
    return WeeklySlaughterhouseDemand.objects.all()

def get_price_per_kg(week_of_year_selected):
    demands = WeeklySlaughterhouseDemand.objects.filter(week_of_year=week_of_year_selected)
    price_per_kg = {}

    for demand in demands:
        slaughterhouse_name = demand.slaughterhouse.name
        price_per_kg[slaughterhouse_name] = demand.live_animal_price_per_kg

    return price_per_kg