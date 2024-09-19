import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import locale
import math
from streamlit import session_state
from streamlit_extras.app_logo import add_logo
from streamlit_extras.stylable_container import stylable_container
locale.setlocale(locale.LC_ALL, 'C')

st.set_page_config(initial_sidebar_state="auto", page_title="Add People Cpl App", page_icon="👋", layout="centered", menu_items=None)

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color:#F7F5F2 ;
        color: #173340;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("logo.png")
    st.write("""
         **Max CPL Calculator Application**
         
         Max CPL Calculator APP version 2.1
        """
    )

with stylable_container(
    key="container_max_cpl_title",
    css_styles="""
        {
            margin-left: 18%;
            margin-right: 50%;
            width: 50%;
        }
    """,
):
    st.title(" Max CPL Calculator App")

with stylable_container(
    key="container_client_lead_deal",
    css_styles="""
        {
            margin: auto;
            width: 50%;
        }
    """,
):
    st.subheader("Change Lead To Deal Calculator")

lead_to_deals_df = pd.DataFrame(
    {
        "Type": ["Total Leads", "Total Deals"],
        "Num": [1, 1],
    }
)

def df_on_change(lead_to_deals_df):
    state = st.session_state["df_editor"]
    for index, updates in state["edited_rows"].items():
        st.session_state["lead_to_deals_df"].loc[st.session_state["lead_to_deals_df"].index == index, "Complete"] = True
        for key, value in updates.items():
            st.session_state["lead_to_deals_df"].loc[st.session_state["lead_to_deals_df"].index == index, key] = value

def lead_to_deals_editor():
    if "lead_to_deals_df" not in st.session_state:
        st.session_state["lead_to_deals_df"] = lead_to_deals_df
    st.data_editor(st.session_state["lead_to_deals_df"], key="df_editor", on_change=df_on_change, args=[lead_to_deals_df],
        column_config={
            "Type": st.column_config.Column(
                disabled=True
            )
        },
        disabled=["Complete"],
        use_container_width=True,
        hide_index=True
    )

lead_to_deals_editor()

leads_to_deals_edited_df = st.session_state["lead_to_deals_df"]
total_leads = leads_to_deals_edited_df['Num'].iloc[0]
total_deals = leads_to_deals_edited_df['Num'].iloc[1]

leads_to_deals = leads_to_deals_edited_df['Num'].iloc[1] / leads_to_deals_edited_df['Num'].iloc[0]

st.info(f"Leads to Deals(%) = {round(leads_to_deals * 100, 2)}%")

st.divider()

with stylable_container(
    key="container_gross_profit",
    css_styles="""
        {
            margin-left: 28%;
            margin-right: 50%;
            width: 50%;
        }
    """,
):
    st.subheader("Client Gross Profit Margin")

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

with stylable_container(
    key="container_caption",
    css_styles="""
        {
            margin-left: 2%;
            margin-right: 50%;
            width: 50%;
        }
    """,
):
    st.caption("Don't know your average cost but know your aov and gross profit margin? Input your gross profit margin in *(Client Input)Gross Profit Margin % (Client Input)*, fill in your AOV then set average cost to 0.")

st.info(f"Gross Profit = {format(round(gross_profit, 2), '.2f')}")
st.info(f"Gross Profit Margin(%) = {round(gross_profit_margin * 100, 2)}%")

with stylable_container(
    key="gross_profit_margin_popover",
    css_styles="""
        {
           width: 100%;
        }
    """,
):
    with st.expander(":information_source:"):
        st.write("**AOV** - Average Order Value. It calculates the average amount of money customers spend on each transaction. To calculate AOV, you sum up the total revenue generated from all orders over a specific period and divide it by the total number of orders.")
        st.write("**Average Cost** - The typical expense incurred by a business to provide a particular service to its customers. This metric encompasses various costs associated with delivering the service, including labour, materials, overhead, and any other direct or indirect expenses related to fulfilling customer needs.")
        st.write("**Gross Profit** - A financial metric that represents the revenue generated by a business after deducting the direct costs associated with producing or delivering the goods or services sold. It provides insight into the profitability of a company's core business operations before considering other expenses such as overhead, taxes, interest, and depreciation.")
        st.write("To calculate Gross Profit, you subtract the Cost of Goods Sold (COGS) from the total revenue generated from sales.")
        st.write("**Gross Profit Margin (%)** - Indicates the gross profit margin as a %")

st.divider()

with stylable_container(
    key="container_break_even",
    css_styles="""
        {
            margin-left: 30%;
            margin-right: 50%;
            width: 50%;
        }
    """,
):
    st.subheader("Break Even Calculation")

break_even_calculation_data_df = pd.DataFrame(
    {
        "Type": ["Campaign Monthly Media Spend", "Management Fee"],
        "Num": [1.50, 1.50],
    }
)

def df_on_change_break_even(break_even_calculation_data_df):
    state_gpm_break_even = st.session_state["df_editor_break_even"]
    for index, updates in state_gpm_break_even["edited_rows"].items():
        st.session_state["break_even_calculation_data_df"].loc[st.session_state["break_even_calculation_data_df"].index == index, "Complete"] = True
        for key, value in updates.items():
            st.session_state["break_even_calculation_data_df"].loc[st.session_state["break_even_calculation_data_df"].index == index, key] = value

def break_even_calculation_data_editor():
    if "break_even_calculation_data_df" not in st.session_state:
        st.session_state["break_even_calculation_data_df"] = break_even_calculation_data_df
    st.data_editor(st.session_state["break_even_calculation_data_df"], key="df_editor_break_even", on_change=df_on_change_break_even, args=[break_even_calculation_data_df],
        column_config={
            "Type": st.column_config.Column(
                disabled=True
            )
        },
        disabled=["Complete"],
        use_container_width=True,
        hide_index=True
    )

break_even_calculation_data_editor()

break_even_calculation_data_edited_df = st.session_state["break_even_calculation_data_df"]
#st.write(break_even_calculation_data_edited_df['num'].iloc[0])
#st.write(break_even_calculation_data_edited_df['num'].iloc[1])
#st.write(client_gross_profit_margin_data_edited_df['num'].iloc[0])
#st.write(gross_profit_margin)

break_even_point = round((break_even_calculation_data_edited_df['Num'].iloc[0] + break_even_calculation_data_edited_df['Num'].iloc[1]) / (client_gross_profit_margin_data_edited_df['Num'].iloc[0] * gross_profit_margin), 2)
break_even_point_round = round(math.ceil(break_even_point), 2)
st.info(f"Break Even Point (BEP) =  {break_even_point}")
st.info(f"Break Even Point (BEP) - Rounded up =  {break_even_point_round}")

with stylable_container(
    key="gross_profit_margin_popover",
    css_styles="""
        {
            width: 100%;
        }
    """,
):
    with st.expander(":information_source:"):
        st.write("**Campaign Monthly Media Spend** - refers to the total amount of money allocated or spent on advertising and promotional activities for a specific marketing campaign within a single month.")
        st.write("**Management Fee** - refers to the total amount of money allocated to Add People, as a management fee, within a single month.")
        st.write("**Break Even Point** - The level of sales at which a company's total revenue equals its total costs, resulting in neither profit nor loss. In other words, it's the point where the company covers all its fixed and variable costs, and beyond which it begins to generate profit. Based on GPM.")
        st.write("Total Cost of the campaign divided by the GPM of the clients AOV")
        st.write("**Break Even Point (Rounded Up)** - Number of actual sales required to break even")

st.divider()

with stylable_container(
    key="container_target_cost",
    css_styles="""
        {
            margin-left: 38%;
            margin-right: 50%;
            width: 50%;
        }
    """,
):
    st.subheader("Target Costs")

total_monthly_cost_of_campaign = break_even_calculation_data_edited_df['Num'].iloc[0] + break_even_calculation_data_edited_df['Num'].iloc[1]
break_even_number_of_leads = break_even_point_round / leads_to_deals
maximum_cpa = total_monthly_cost_of_campaign / break_even_point_round
st.info(f"Total Monthly Cost of Campaign = {round(total_monthly_cost_of_campaign, 2)}")
st.info(f"Break even Number of Leads = {round(break_even_number_of_leads, 2)}")
st.info(f"Maximum CPA = {round(maximum_cpa, 2)}")

with stylable_container(
    key="max_cpa_popover",
    css_styles="""
        {
            width: 100%;
        }
    """,
):
    with st.expander(":information_source:"):
        st.write("**Total Monthly Cost of Campaign** - The total monthly cost of the campaign including monthly media spend and management fee")
        st.write("**Break Even Number of Leads** - Number of leads required using the clients break even point and the client's ability to convert leads.")
        st.write("**Maximum CPA** - Target CPA cost for the campaign divided by BEP")
        st.write("**Maximum Cost Per Lead** - Target Cost per lead, Monthly campaign spend divided by BE Number of Leads")

st.divider()

max_cost_per_lead = total_monthly_cost_of_campaign / break_even_number_of_leads

with stylable_container(
    key="container_break_even",
    css_styles="""
        {
            margin-left: 30%;
            margin-right: 50%;
            width: 50%;
        }
    """,
):
    st.subheader("Maximum Cost Per Lead")

st.success(f"Maximum Cost Per Lead = {round(max_cost_per_lead, 2)}")

st.divider()

left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.text(" ")
    st.image("logo.png")
