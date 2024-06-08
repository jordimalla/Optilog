from ..models import Slaugherhouse

def get_slaughterhouses_name():
    return Slaugherhouse.objects.values_list('name', flat=True)