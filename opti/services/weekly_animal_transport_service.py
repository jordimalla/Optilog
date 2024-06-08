from ..models import WeeklyAnimalTransport

def get_transport_cost_per_trip(week_of_year_selected):
    transports = WeeklyAnimalTransport.objects.filter(week_of_year=week_of_year_selected)
    transport_cost_per_trip = {}

    for transport in transports:
        key = (transport.origin_farm.name, transport.destination_slaughterhouse.name)
        transport_cost_per_trip[key] = transport.transport_cost

    return transport_cost_per_trip

def get_all_weekly_animal_transport():
    return WeeklyAnimalTransport.objects.all()