from collections import defaultdict
from ortools.linear_solver import pywraplp
from django.shortcuts import get_object_or_404
from django.http import Http404
from ..models import WeeklyTransportCapacity, Slaugherhouse, Farm, WeeklyAnimalTransport, WeeklySlaughterhouseDemand, WeeklyFarmAnimalAvailability

def get_weeks_of_year_availables():
    weeks = ""
    try:
        weeks = WeeklyTransportCapacity.objects.order_by('week_of_year').values_list('week_of_year', flat=True).distinct('week_of_year')
    except:
        raise Http404("Weekly transport capacity doesn't exist")
    
    return weeks

def get_animals_available(week_of_year_selected):
    farmAnimalsAvailable = WeeklyFarmAnimalAvailability.objects.filter(week_of_year=week_of_year_selected)
    animals_available = defaultdict(int)

    for farmAnimalAvailable in farmAnimalsAvailable:
        farm_name = farmAnimalAvailable.farm.name
        animals_available[farm_name] += farmAnimalAvailable.animal_count

    return dict(animals_available)

def get_demand(week_of_year_selected):
    demands = WeeklySlaughterhouseDemand.objects.filter(week_of_year=week_of_year_selected)
    demand_dict = defaultdict(int)

    for demand in demands:
        slaughterhouse_name = demand.slaughterhouse.name
        demand_dict[slaughterhouse_name] += demand.animal_count

    return dict(demand_dict)

def get_transport_cost_per_trip(week_of_year_selected):
    transports = WeeklyAnimalTransport.objects.filter(week_of_year=week_of_year_selected)
    transport_cost_per_trip = {}

    for transport in transports:
        key = (transport.origin_farm.name, transport.destination_slaughterhouse.name)
        transport_cost_per_trip[key] = transport.transport_cost

    return transport_cost_per_trip

def get_price_per_kg(week_of_year_selected):
    demands = WeeklySlaughterhouseDemand.objects.filter(week_of_year=week_of_year_selected)
    price_per_kg = {}

    for demand in demands:
        slaughterhouse_name = demand.slaughterhouse.name
        price_per_kg[slaughterhouse_name] = demand.live_animal_price_per_kg

    return price_per_kg

def get_average_weight(week_of_year_selected):
    availabilities = WeeklyFarmAnimalAvailability.objects.filter(week_of_year=week_of_year_selected)
    average_weight = {}

    for availability in availabilities:
        farm_name = availability.farm.name
        average_weight[farm_name] = availability.average_weight

    return average_weight

def get_max_transport_capacity(week_of_year_selected):
    capacity = get_object_or_404(WeeklyTransportCapacity, week_of_year=week_of_year_selected)
    return capacity.max_transport_capacity

def get_farms_name():
    return Farm.objects.values_list('name', flat=True)

def get_slaughterhouses_name():
    return Slaugherhouse.objects.values_list('name', flat=True)

def optimize_transport(week_of_year_selected):
    # Crear el solver de programación entera mixta lineal
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        return "El solver SCIP no está disponible."
    
    # Granjas
    farms = get_farms_name()
    
    # Mataderos
    slaughterhouses = get_slaughterhouses_name()
    
    # Número de animales disponibles en cada granja
    animals_available = get_animals_available(week_of_year_selected)
    
    # Demanda de número de animales en cada matadero
    demand = get_demand(week_of_year_selected)
    
    # Coste de transporte por viaje (€)
    transport_cost_per_trip = get_transport_cost_per_trip(week_of_year_selected)
    
    # Precio por kg de carne (€/kg)
    price_per_kg = get_price_per_kg(week_of_year_selected)

    # Peso promedio por animal (kg)
    average_weight = get_average_weight(week_of_year_selected)

    # Capacidad máxima de peso por viaje (kg)
    vehicle_capacity_kg = get_max_transport_capacity(week_of_year_selected)  
    
    # Variables
    x = {}  # Animales transportados
    n = {}  # Número de viajes
    for f in farms:
        if f in animals_available:
            for s in slaughterhouses:
                x[(f, s)] = solver.IntVar(0, animals_available[f], f'x[{f},{s}]')
                n[(f, s)] = solver.IntVar(0, solver.infinity(), f'n[{f},{s}]')

    # Función objetivo: Maximizar ingresos netos
    objective = solver.Objective()
    for f in farms:
        if f in animals_available and f in average_weight:
            for s in slaughterhouses:
                if s in price_per_kg:
                    # Añadiendo ingresos por la venta de carne
                    objective.SetCoefficient(x[(f, s)], price_per_kg[s] * average_weight[f])
                    # Añadiendo costes de transporte por viaje al objetivo
                    objective.SetCoefficient(n[(f, s)], -transport_cost_per_trip[(f, s)])
    objective.SetMaximization()
    # Restricciones
    # Demanda en cada matadero
    for s in slaughterhouses:
        if s in demand:
            solver.Add(sum(x[(f, s)] for f in farms if f in animals_available) >= demand[s], f'Demand[{s}]')

    # Disponibilidad en cada granja
    for f in farms:
        if f in animals_available:
            solver.Add(sum(x[(f, s)] for s in slaughterhouses if s in demand) <= animals_available[f], f'Supply[{f}]')

    # Capacidad de transporte por viaje (peso total)
    for f in farms:
        if f in animals_available:
            for s in slaughterhouses:
                if s in demand:
                    solver.Add(x[(f, s)] * average_weight[f] <= vehicle_capacity_kg * n[(f, s)], f'TripCapacity[{f},{s}]')

    # Solucionar el problema
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        result = 'Solución\n'
        result = f'Ingreso Neto Total: {objective.Value()} €\n'
        for f in farms:
            if f in animals_available:
                for s in slaughterhouses:
                    if s in demand:
                        result += f'Animales de {f} a {s}: {x[(f, s)].solution_value()} animales, viajes: {n[(f, s)].solution_value()}\n'
    else:
        result = "El problema no tiene solución óptima."
    
    return result

