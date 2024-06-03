from django.db import models

# Create your models here.
class WeeklyTransportCapacity(models.Model):
    week_of_year = models.IntegerField()
    max_transport_capacity = models.FloatField(default=0)
    def __str__(self):
        return str(self.week_of_year)

class Slaugherhouse(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class Farm(models.Model):
    name = models.CharField(max_length=300)
    def __str__(self):
        return self.name

class WeeklyAnimalTransport(models.Model):
    origin_farm = models.ForeignKey(Farm, on_delete=models.DO_NOTHING)
    destination_slaughterhouse = models.ForeignKey(Slaugherhouse, on_delete=models.DO_NOTHING)
    transport_cost = models.FloatField(default=0)
    week_of_year = models.IntegerField()
    def __str__(self):
        return str(self.week_of_year) + '_' + self.origin_farm.name + '_' + self.destination_slaughterhouse.name

class WeeklySlaughterhouseDemand(models.Model):
    slaughterhouse = models.ForeignKey(Slaugherhouse, on_delete=models.DO_NOTHING)
    animal_count = models.IntegerField(default=0)
    live_animal_price_per_kg = models.FloatField(default=0)
    week_of_year = models.IntegerField()
    def __str__(self):
        return str(self.week_of_year) + '_' + self.slaughterhouse.name

class WeeklyFarmAnimalAvailability(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.DO_NOTHING)
    animal_count = models.IntegerField(default=0)
    average_weight = models.FloatField(default=0)
    week_of_year = models.IntegerField()
    def __str__(self):
        return str(self.week_of_year) + '_' + self.farm.name