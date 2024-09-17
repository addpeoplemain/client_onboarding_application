import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import locale
import math
from streamlit import session_state
from streamlit_extras.app_logo import add_logo
from streamlit_extras.stylable_container import stylable_container 


def spend_per_conversion_with_condition(cpc, monthly_budget, cta_list):
    # Constant Conversion Rate
    conversion_rate = 0.02  # 2% Conversion Rate
    no_count = 0
    
    # Calculate the number of clicks generated from the budget (assuming every dollar spent gives a click)
    clicks = monthly_budget / cpc
    
    # Calculate the number of conversions (leads)
    conversions = clicks * conversion_rate
    
    # Count occurrences of 'no' in cta_list
    for cta in cta_list:
        if 'no' in cta.lower():  # Case-insensitive comparison
            no_count += 1
    
    if no_count > 0:
        # If 'no' was found, reduce total conversions by 25% for each 'no'
        conversions = conversions * (1 - (0.25 * no_count))  # Reduce conversions by 25% for each 'no'
        additional_cost = monthly_budget * (0.25 * no_count)  # Add 25% of the budget as additional cost for each 'no'
        total_budget = monthly_budget + additional_cost
    else:
        # If no 'no' in the list, keep the conversions and budget as is
        total_budget = monthly_budget
    
    if conversions == 0:
        return float('inf'), 0  # Return infinity for cost per conversion if no leads, and 0 for leads
    
    # Calculate the spend per conversion (cost per lead)
    cost_per_conversion = total_budget / conversions
    
    return conversions, cost_per_conversion

clickable_call = st.checkbox("Clickable Call")
clickable_email = st.checkbox("Clickable Email")
contact_form = st.checkbox("Contact Form")
cta_list = ["yes","no","no","no"]

if not clickable_call:
    del cta_list[-1]
if not clickable_email:
    del cta_list[-1]

if not contact_form:
    del cta_list[-1]
    
st.write(cta_list)

client_gross_profit_margin_data_df = pd.DataFrame(
{
    "Type": ["AOV", "Average Cost", "*(Client Input) Gross Profit Margin % (Client Input)*"],
    "Num": [2.50, 1.50, 1.00],
}
)

