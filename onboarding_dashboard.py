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
