from django.db import models

class Buildings(models.Model):
    building_id = models.CharField(max_length=100, primary_key=True)
    district = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    address = models.TextField()

    latitude = models.FloatField()
    longitude = models.FloatField()

    construction_year = models.IntegerField()
    building_type = models.CharField(max_length=100)
    num_units = models.IntegerField()
    total_area_m2 = models.FloatField()
    num_floors = models.IntegerField()

    heating_system = models.CharField(max_length=100)
    heating_age = models.IntegerField()

    epc_rating = models.CharField(max_length=5)
    energy_consumption_kwh_m2 = models.FloatField()

    last_renovation_year = models.IntegerField(null=True)
    listed_building = models.BooleanField()
    
    class Meta:
        db_table = "building"
        managed = False  # VERY IMPORTANT (table already exists)