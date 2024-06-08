from django.urls import path
from . import views

app_name = "opti"
urlpatterns = [
    path("", views.index, name="index"),
    path('optimization/', views.optimization_view, name='optimization_view'),
    path("detail/", views.detail, name="detail"),
    path("optimize/", views.optimize, name="optimize"),
]