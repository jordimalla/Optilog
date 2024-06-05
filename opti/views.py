from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render

from .models import WeeklyTransportCapacity, Slaugherhouse, Farm, WeeklyAnimalTransport, WeeklySlaughterhouseDemand, WeeklyFarmAnimalAvailability

def index(request):
    return HttpResponse("Hellow, world. You're at the opti index.")

def detail(request):
    try:
        list_week_of_year_available = WeeklyTransportCapacity.objects.order_by('week_of_year').values_list('week_of_year', flat=True).distinct('week_of_year')
    except WeeklyTransportCapacity.DoesNotExist:
        raise Http404("Weekly transport capacity doesn't exist")
    return render(request, "opti/detail.html", {"weeksOfYear": list_week_of_year_available})

def optimize(request):
    try:
        list_week_of_year_available = WeeklyTransportCapacity.objects.order_by('week_of_year').values_list('week_of_year', flat=True).distinct('week_of_year')
        week_of_year_selected = request.POST["weekOfYear"]
        list_week_animal_transport = WeeklyAnimalTransport.objects.filter(week_of_year=week_of_year_selected)
    except WeeklyTransportCapacity.DoesNotExist:
        raise Http404("Weekly transport capacity doesn't exist")
    return render(request, "opti/detail.html", {"weeksOfYear": list_week_of_year_available, "weekAnimalTransports": list_week_animal_transport})