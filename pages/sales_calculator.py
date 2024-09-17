












def spend_per_conversion_with_condition(cpc, monthly_budget, yes_no):
    # Constant Conversion Rate
    conversion_rate = 0.02  # 2% Conversion Rate
    
    # Calculate the number of clicks generated from the budget (assuming every dollar spent gives a click)
    clicks = monthly_budget / cpc
    
    # Calculate the number of conversions (leads)
    conversions = clicks * conversion_rate
    
    if yes_no.lower() == 'no':
        # If the answer is no, reduce total conversions by 25%
        conversions = conversions * (1 - 0.25)  # Reduce conversions by 25%
        additional_cost = monthly_budget * 0.25  # Add 25% of the budget as additional cost
        total_budget = monthly_budget + additional_cost
    else:
        # If the answer is yes, keep the conversions and budget as is
        total_budget = monthly_budget
    
    if conversions == 0:
        return float('inf'), 0  # Return infinity for cost per conversion if no leads, and 0 for leads
    
    # Calculate the spend per conversion (cost per lead) 
    cost_per_conversion = total_budget / conversions
    
    return conversions, cost_per_conversion

