from django.http import HttpResponse
from django.shortcuts import render

from .services.optimize_services import optimize_transport, get_weeks_of_year_availables
from .services.weekly_transport_capacity_service import get_all_weekly_transport_capacity
from .services.weekly_animal_transport_service import get_all_weekly_animal_transport
from .services.weekly_slaughterhouse_demand_service import get_all_weekly_slaughterhouse_demand
from .services.weekly_farm_animal_avilability_service import get_all_weekly_farm_animal_availability

def index(request):
    return HttpResponse("Hellow, world. You're at the opti index.")

def detail(request):
    list_week_of_year_available = get_weeks_of_year_availables()

    return render(request, "opti/detail.html", {"weeksOfYear": list_week_of_year_available})

def optimize(request):
    result = ""

    if request.method == 'POST':
        week_of_year_selected = request.POST.get('weekOfYear')
        result = optimize_transport(week_of_year_selected)

    list_week_of_year_available = get_weeks_of_year_availables()

    context = {
        'weeksOfYear': list_week_of_year_available,
        'result': result,
    }

    return render(request, "opti/detail.html", context)

def optimization_view(request):
    list_week_of_year_available = get_weeks_of_year_availables()
    week_of_year_selected = request.GET.get('week_of_year_selected')
    weekly_transport_capacity = get_all_weekly_transport_capacity()
    weekly_animal_transport = get_all_weekly_animal_transport()
    weekly_slaughterhouse_demand = get_all_weekly_slaughterhouse_demand()
    weekly_farm_animal_availability = get_all_weekly_farm_animal_availability()
    
    if week_of_year_selected:
        weekly_transport_capacity = weekly_transport_capacity.filter(week_of_year=week_of_year_selected)
        weekly_animal_transport = weekly_animal_transport.filter(week_of_year=week_of_year_selected)
        weekly_slaughterhouse_demand = weekly_slaughterhouse_demand.filter(week_of_year=week_of_year_selected)
        weekly_farm_animal_availability = weekly_farm_animal_availability.filter(week_of_year=week_of_year_selected)
    
    context = {
        "weeks_of_year": list_week_of_year_available,
        'weekly_transport_capacity': weekly_transport_capacity,
        'weekly_animal_transport': weekly_animal_transport,
        'weekly_slaughterhouse_demand': weekly_slaughterhouse_demand,
        'weekly_farm_animal_availability': weekly_farm_animal_availability,
        'week_of_year_selected': week_of_year_selected,
    }
    return render(request, 'admin/optimization_view.html', context)