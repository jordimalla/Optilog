from django.shortcuts import get_object_or_404
from ..models import WeeklyTransportCapacity

def get_all_weekly_transport_capacity():
    return WeeklyTransportCapacity.objects.all()

def get_max_transport_capacity(week_of_year_selected):
    capacity = get_object_or_404(WeeklyTransportCapacity, week_of_year=week_of_year_selected)
    return capacity.max_transport_capacity

def get_weeks_of_year_availables():
    weeks = ""
    try:
        weeks = WeeklyTransportCapacity.objects.order_by('week_of_year').values_list('week_of_year', flat=True).distinct('week_of_year')
    except:
        raise Http404("Weekly transport capacity doesn't exist")
    
    return weeks