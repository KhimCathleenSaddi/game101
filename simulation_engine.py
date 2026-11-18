# simulation_engine.py
import pandas as pd

def calculate_benefits(user_scores, matrix_df):
    """
    Calculates projected benefit scores (0-5 scale) based on absolute 
    slider settings (0-5) and the benefits matrix weights.
    """
    matrix = matrix_df.set_index("nbs_id")
    benefit_columns = list(matrix.columns)
    
    raw_benefits = {col: 0.0 for col in benefit_columns}
    max_possible_weights = {col: 0.0 for col in benefit_columns}
    
    # Calculate raw absolute impact and the maximum possible ceiling
    for nbs_id, score in user_scores.items():
        if nbs_id in matrix.index:
            for benefit in benefit_columns:
                weight = float(matrix.loc[nbs_id, benefit])
                # Absolute contribution: higher score = higher impact
                raw_benefits[benefit] += (score / 5.0) * weight
                # Track the absolute maximum possible weight if all sliders were set to 5
                max_possible_weights[benefit] += weight

    # Scale the final scores cleanly to a 0.0 - 5.0 range
    final_benefits = {}
    for benefit, raw_val in raw_benefits.items():
        max_limit = max_possible_weights[benefit]
        if max_limit > 0:
            # Scale proportionally against the maximum possible impact for that benefit
            scaled = (raw_val / max_limit) * 5.0
        else:
            scaled = 0.0
            
        final_benefits[benefit] = round(min(5.0, max(0.0, scaled)), 2)
        
    return final_benefits