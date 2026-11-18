# simulation_engine.py

def run_simulation(carbon_tax, clean_subsidy):
    """
    A simple placeholder EN-ROADS-style math model.
    Calculates temperature rise and emissions based on policy inputs.
    """
    base_temp = 3.5  # Baseline business-as-usual temperature in 2100 (°C)
    
    # Policy levers reduce temperature and emissions
    temp_reduction = (carbon_tax * 0.008) + (clean_subsidy * 0.012)
    final_temp = max(1.5, base_temp - temp_reduction)
    
    # Global CO2 emissions in Gigatons (Gt)
    emissions = max(5.0, 40.0 - (carbon_tax * 0.15) - (clean_subsidy * 0.25))
    
    return round(final_temp, 2), round(emissions, 1)
