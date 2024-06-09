from ortools.linear_solver import pywraplp

from .farm_service import get_farms_name
from .slaughterhouse_service import get_slaughterhouses_name
from .weekly_transport_capacity_service import get_max_transport_capacity
from .weekly_animal_transport_service import get_transport_cost_per_trip
from .weekly_slaughterhouse_demand_service import get_demand, get_price_per_kg
from .weekly_farm_animal_avilability_service import get_animals_available, get_average_weight

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