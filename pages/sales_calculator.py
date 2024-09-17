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

def average_cost_from_gross_profit_margin(gross_profit_margin, aov):
    gross_profit = (gross_profit_margin / 100) * aov
    average_cost = aov - gross_profit
    return average_cost

def df_on_change_gpm(client_gross_profit_margin_data_df):
    state_gpm = st.session_state["df_editor_gpm"]
    for index, updates in state_gpm["edited_rows"].items():
        st.session_state["client_gross_profit_margin_data_df"].loc[st.session_state["client_gross_profit_margin_data_df"].index == index, "Complete"] = True
        for key, value in updates.items():
            st.session_state["client_gross_profit_margin_data_df"].loc[st.session_state["client_gross_profit_margin_data_df"].index == index, key] = value
    
    if st.session_state["client_gross_profit_margin_data_df"]['Num'].iloc[1] == 0 and st.session_state["client_gross_profit_margin_data_df"]['Num'].iloc[2] != 0:
        average_cost = average_cost_from_gross_profit_margin(st.session_state["client_gross_profit_margin_data_df"]['Num'].iloc[2], st.session_state["client_gross_profit_margin_data_df"]['Num'].iloc[0])
        st.session_state["client_gross_profit_margin_data_df"]['Num'].iloc[1] = average_cost

def client_gross_profit_margin_editor():
    if "client_gross_profit_margin_data_df" not in st.session_state:
        st.session_state["client_gross_profit_margin_data_df"] = client_gross_profit_margin_data_df
    st.data_editor(st.session_state["client_gross_profit_margin_data_df"], key="df_editor_gpm", on_change=df_on_change_gpm, args=[client_gross_profit_margin_data_df],
        column_config={
            "Type": st.column_config.Column(
                disabled=True
            )
        },
        disabled=["Complete"],
        use_container_width=True,
        hide_index=True
    )

client_gross_profit_margin_editor()

client_gross_profit_margin_data_edited_df = st.session_state["client_gross_profit_margin_data_df"]
gross_profit = client_gross_profit_margin_data_edited_df['Num'].iloc[0] - client_gross_profit_margin_data_edited_df['Num'].iloc[1]
gross_profit_margin = gross_profit / client_gross_profit_margin_data_edited_df['Num'].iloc[0]
