def calculate_efficiency(building):
    """
    Calculate CO₂ reduction, estimated cost, and eligible subsidies
    for a single building (used for heatmap markers).

    building: dict with keys:
        - num_units
        - total_area_m2
        - num_floors
        - construction_year
        - last_renovation_year
        - heating_system
        - energy_consumption_kwh_m2
    """

    # --- CO2 reduction: simple example ---
    co2_reduction = round(building["num_floors"] * 0.05 * building["total_area_m2"], 2)

    # --- Estimated cost ---
    estimated_cost = int(building["num_units"] * 1000 + building["total_area_m2"] * 50)

    # --- Eligible subsidies ---
    subsidies = []
    # KfW eligibility: buildings built before 2000
    if building["construction_year"] < 2000:
        subsidies.append("KfW")
    # BAFA eligibility: heating type is Gas or Oil
    if building["heating_system"].lower() in ["gas boiler", "oil boiler"]:
        subsidies.append("BAFA")
    # If none, add "None"
    if not subsidies:
        subsidies = ["None"]

    return {
        "co2_reduction_kg_m2": co2_reduction,
        "estimated_cost_eur": estimated_cost,
        "eligible_subsidies": ", ".join(subsidies)
    }