from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.urls import path, reverse
from django.utils.html import format_html

from .views import optimization_view
from .models import (
    WeeklyTransportCapacity, 
    Slaugherhouse, 
    Farm, 
    WeeklyAnimalTransport, 
    WeeklySlaughterhouseDemand, 
    WeeklyFarmAnimalAvailability
)

class CustomAdminSite(admin.AdminSite):
    site_header = 'Custom Admin'
    site_title = 'Admin Site'
    index_title = 'Admin Home'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('opti/optimization/', self.admin_view(optimization_view), name='optimization_view'),
        ]
        return custom_urls + urls
    
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_link'] = format_html('<a href="{}" class="button">Optimization</a>', reverse('admin:optimization_view'))
        extra_context['farm_link'] = format_html('<a href="{}" class="button">Farm</a>', reverse('admin:opti_farm_changelist'))
        extra_context['salughterhouse_link'] = format_html('<a href="{}" class="button">Slaughterhouse</a>', reverse('admin:opti_slaugherhouse_changelist'))
        extra_context['weeklyTransportCapacity_link'] = format_html('<a href="{}" class="button">Transport Capacity</a>', reverse('admin:opti_weeklytransportcapacity_changelist'))
        extra_context['weeklyAnimalTransport_link'] = format_html('<a href="{}" class="button">Animal Transport</a>', reverse('admin:opti_weeklyanimaltransport_changelist'))
        extra_context['weeklySlaughterhouseDemand_link'] = format_html('<a href="{}" class="button">Slaughterhouse Demand</a>', reverse('admin:opti_weeklyslaughterhousedemand_changelist'))
        extra_context['weeklyFarmAnimalAvailability_link'] = format_html('<a href="{}" class="button">Farm Animal Availability</a>', reverse('admin:opti_weeklyfarmanimalavailability_changelist'))
        return super().index(request, extra_context=extra_context)

    def app_index(self, request, app_label, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_link'] = format_html('<a href="{}"  class="button">Optimization</a>', reverse('admin:optimization_view'))
        extra_context['farm_link'] = format_html('<a href="{}" class="button">Farm</a>', reverse('admin:opti_farm_changelist'))
        extra_context['salughterhouse_link'] = format_html('<a href="{}" class="button">Slaughterhouse</a>', reverse('admin:opti_slaugherhouse_changelist'))
        extra_context['weeklyTransportCapacity_link'] = format_html('<a href="{}" class="button">Transport Capacity</a>', reverse('admin:opti_weeklytransportcapacity_changelist'))
        extra_context['weeklyAnimalTransport_link'] = format_html('<a href="{}" class="button">Animal Transport</a>', reverse('admin:opti_weeklyanimaltransport_changelist'))
        extra_context['weeklySlaughterhouseDemand_link'] = format_html('<a href="{}" class="button">Slaughterhouse Demand</a>', reverse('admin:opti_weeklyslaughterhousedemand_changelist'))
        extra_context['weeklyFarmAnimalAvailability_link'] = format_html('<a href="{}" class="button">Farm Animal Availability</a>', reverse('admin:opti_weeklyfarmanimalavailability_changelist'))
        return super().app_index(request, app_label, extra_context=extra_context)

    def each_context(self, request):
        context = super().each_context(request)
        context['custom_link'] = format_html('<a href="{}" class="button">Optimization</a>', reverse('admin:optimization_view'))
        context['farm_link'] = format_html('<a href="{}" class="button">Farm</a>', reverse('admin:opti_farm_changelist'))
        context['salughterhouse_link'] = format_html('<a href="{}" class="button">Slaughterhouse</a>', reverse('admin:opti_slaugherhouse_changelist'))
        context['weeklyTransportCapacity_link'] = format_html('<a href="{}" class="button">Transport Capacity</a>', reverse('admin:opti_weeklytransportcapacity_changelist'))
        context['weeklyAnimalTransport_link'] = format_html('<a href="{}" class="button">Animal Transport</a>', reverse('admin:opti_weeklyanimaltransport_changelist'))
        context['weeklySlaughterhouseDemand_link'] = format_html('<a href="{}" class="button">Slaughterhouse Demand</a>', reverse('admin:opti_weeklyslaughterhousedemand_changelist'))
        context['weeklyFarmAnimalAvailability_link'] = format_html('<a href="{}" class="button">Farm Animal Availability</a>', reverse('admin:opti_weeklyfarmanimalavailability_changelist'))
        return context
    
admin_site = CustomAdminSite(name='custom_admin')

# Register the User and Group models
admin_site.register(User)
admin_site.register(Group)

# Register your models here.
admin_site.register(WeeklyAnimalTransport)
admin_site.register(Slaugherhouse)
admin_site.register(Farm)
admin_site.register(WeeklyFarmAnimalAvailability)
admin_site.register(WeeklySlaughterhouseDemand)
admin_site.register(WeeklyTransportCapacity)