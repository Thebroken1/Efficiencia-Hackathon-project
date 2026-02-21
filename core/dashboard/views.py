from django.shortcuts import render
from django.http import JsonResponse
from .models import Buildings
from .retrofit_efficiency_calculator import calculate_efficiency  # This function calculates CO2, cost, subsidies

# -------------------------------
# Dashboard page
# -------------------------------
def heatmap_view(request):
    """Render the main dashboard page with map + filters"""
    return render(request, "dashboard.html")


# -------------------------------
# Heatmap API
# -------------------------------
def heatmap_data(request):
    qs = Buildings.objects.all()

    # Get filter params
    try: construction_year = int(request.GET.get('construction_year'))
    except: construction_year = None
    try: num_units = int(request.GET.get('num_units'))
    except: num_units = None
    try: num_floors = int(request.GET.get('num_floors'))
    except: num_floors = None
    try: total_area_m2 = float(request.GET.get('total_area_m2'))
    except: total_area_m2 = None
    try: last_renovation_year = int(request.GET.get('last_renovation_year'))
    except: last_renovation_year = None
    district = request.GET.get('district')
    postal_code = request.GET.get('postal_code')
    heating_system = request.GET.get('heating_system')

    # Approximate filters (ranges)
    if construction_year:
        qs = qs.filter(construction_year__gte=construction_year-5,
                       construction_year__lte=construction_year+5)
    if num_units:
        lower = max(1, int(num_units*0.9))
        upper = int(num_units*1.1)
        qs = qs.filter(num_units__gte=lower, num_units__lte=upper)
    if num_floors:
        qs = qs.filter(num_floors__gte=num_floors-1, num_floors__lte=num_floors+1)
    if total_area_m2:
        lower = total_area_m2 * 0.9
        upper = total_area_m2 * 1.1
        qs = qs.filter(total_area_m2__gte=lower, total_area_m2__lte=upper)
    if last_renovation_year:
        qs = qs.filter(last_renovation_year__gte=last_renovation_year-5,
                       last_renovation_year__lte=last_renovation_year+5)

    # Other filters
    if district:
        qs = qs.filter(district__icontains=district)
    if postal_code:
        qs = qs.filter(postal_code__icontains=postal_code)
    if heating_system:
        qs = qs.filter(heating_system__iexact=heating_system)  # STRICT filter for exact match

    # Prepare building data
    buildings_list = []
    for b in qs:
        building_data = {
            "latitude": b.latitude,
            "longitude": b.longitude,
            "address": b.address,
            "energy_consumption_kwh_m2": b.energy_consumption_kwh_m2,
            "num_floors": b.num_floors,
            "num_units": b.num_units,
            "total_area_m2": b.total_area_m2,
            "heating_system": b.heating_system,
            "construction_year": b.construction_year,
            "last_renovation_year": b.last_renovation_year,
        }

        # Calculate CO2 reduction, estimated cost, and subsidies
        calc = calculate_efficiency({
            "num_units": b.num_units,
            "total_area_m2": b.total_area_m2,
            "num_floors": b.num_floors,
            "construction_year": b.construction_year,
            "last_renovation_year": b.last_renovation_year,
            "heating_system": b.heating_system,
            "energy_consumption_kwh_m2": b.energy_consumption_kwh_m2
        })

        building_data.update({
            "co2_reduction_kg_m2": calc["co2_reduction_kg_m2"],
            "estimated_cost_eur": calc["estimated_cost_eur"],
            "eligible_subsidies": calc["eligible_subsidies"]
        })

        buildings_list.append(building_data)

    return JsonResponse(buildings_list, safe=False)