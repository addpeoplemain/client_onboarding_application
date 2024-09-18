import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from streamlit_tags import st_tags
import requests, lxml, json, time
import tldextract
from bs4 import BeautifulSoup

st.title("Add People App Centre")

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
                 
         **Onboarding Application 1.0**
         
         Onboarding Application 1.0
                 
        

            """
         )
st.subheader("Welcome to the add people app centre")
st.markdown("""
Welcome to our web application, your all-in-one toolkit for smarter digital marketing! 

Explore our four powerful services: the Cost Budget Calculator to uncover your conversions and cost per conversion, the CPL Calculator to discover your cost per lead, Keyword Competitor Analysis to stay ahead of your competition, and Your Journey to help you visualize your journey with addpeople. 

Start leveraging these tools to boost your marketing strategy today!""")


if st.button("Cost Budget Calculator"):
    st.switch_page("pages/cost_budget_calculator.py")
if st.button("Cpl Calculator"):
    st.switch_page("pages/cpl_calculator.py")
if st.button("Keyword Competitor Analyser"):
    st.switch_page("pages/keyword_competitor_analysis.py")
if st.button("Your Journey"):
    st.switch_page("pages/your_journey.py")
