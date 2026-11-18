# simulation_engine.py
import pandas as pd

def calculate_benefits(user_scores):
    """
    Translates user slider inputs (0-5 scale for NbS implementation/favorability) 
    into projected benefit scores across 4 key impact areas.
    
    user_scores is a dictionary like: {'urban_forests': 4, 'wetlands': 5, ...}
    """
    # Base coefficients mapping how each NbS contributes to different benefits
    # (Rows = NbS IDs, Columns = Benefit Categories)
    benefit_matrix = {
        'urban_forests':    {'Flood Mitigation': 2.0, 'Biodiversity': 4.0, 'Urban Cooling': 5.0, 'Community Well-being': 4.5},
        'wetlands':         {'Flood Mitigation': 5.0, 'Biodiversity': 5.0, 'Urban Cooling': 2.5, 'Community Well-being': 3.0},
        'green_roofs':      {'Flood Mitigation': 1.5, 'Biodiversity': 2.0, 'Urban Cooling': 4.5, 'Community Well-being': 2.5},
        'regenerative_ag':  {'Flood Mitigation': 3.5, 'Biodiversity': 4.5, 'Urban Cooling': 2.0, 'Community Well-being': 4.0},
        'riparian_buffers': {'Flood Mitigation': 4.5, 'Biodiversity': 5.0, 'Urban Cooling': 3.0, 'Community Well-being': 3.5},
    }
    
    # Calculate weighted aggregate score for each benefit category (capped at 5.0)
    benefits = {'Flood Mitigation': 0.0, 'Biodiversity': 0.0, 'Urban Cooling': 0.0, 'Community Well-being': 0.0}
    
    total_weight = sum(user_scores.values()) if sum(user_scores.values()) > 0 else 1
    
    for nbs_id, score in user_scores.items():
        if nbs_id in benefit_matrix:
            for benefit, weight in benefit_matrix[nbs_id].items():
                # Contribution proportional to score and matrix weight
                benefits[benefit] += (score / 5.0) * weight * (score / total_weight if total_weight > 0 else 0) * 5.0

    # Normalize/clamp final scores between 0 and 5 for a clean reading
    final_benefits = {}
    for benefit, raw_val in benefits.items():
        # Scale relative to max possible impact
        normalized = min(5.0, max(0.5, raw_val * 1.2)) 
        final_benefits[benefit] = round(normalized, 2)
        
    return final_benefits