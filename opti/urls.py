from django.urls import path
from . import views

app_name = "opti"
urlpatterns = [
    path("", views.index, name="index"),
    path("detail/", views.detail, name="detail"),
    path("optimize/", views.optimize, name="optimize"),
]