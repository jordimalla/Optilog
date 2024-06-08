from django.contrib import admin
from django.urls import path
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
            path('optimization/', self.admin_view(optimization_view), name='optimization_view'),
        ]
        return custom_urls + urls
    
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_link'] = format_html('<a href="{}">Optimization View</a>', 'optimization/')
        return super().index(request, extra_context=extra_context)
    
admin_site = CustomAdminSite(name='custom_admin')

# Register your models here.
admin_site.register(WeeklyAnimalTransport)
admin_site.register(Slaugherhouse)
admin_site.register(Farm)
admin_site.register(WeeklyFarmAnimalAvailability)
admin_site.register(WeeklySlaughterhouseDemand)
admin_site.register(WeeklyTransportCapacity)