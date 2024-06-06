from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from ortools.linear_solver import pywraplp

from .services.optimize_services import optimize_transport, get_weeks_of_year_availables

from .models import WeeklyTransportCapacity, Slaugherhouse, Farm, WeeklyAnimalTransport, WeeklySlaughterhouseDemand

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

    list_week_of_year_available = WeeklyTransportCapacity.objects.order_by('week_of_year').values_list('week_of_year', flat=True).distinct('week_of_year')

    context = {
        'weeksOfYear': list_week_of_year_available,
        'result': result,
    }

    return render(request, "opti/detail.html", context)