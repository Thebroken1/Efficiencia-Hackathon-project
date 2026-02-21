from django import forms

class PropertySearchForm(forms.Form):
    district = forms.CharField(max_length=100, required=False)
    postal_code = forms.CharField(max_length=20, required=False)
    construction_year = forms.IntegerField(required=False)
    num_units = forms.IntegerField(required=False)
    total_area_m2 = forms.FloatField(required=False)
    num_floors = forms.IntegerField(required=False)
    heating_system = forms.CharField(max_length=100, required=False)
    last_renovation_year = forms.IntegerField(required=False)
    energy_consumption_kwh_m2 = forms.FloatField(required=False)