from ..models import Farm

def get_farms_name():
    return Farm.objects.values_list('name', flat=True)