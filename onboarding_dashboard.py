import streamlit as st
import streamlit_tags as st_tags

st.title("Add People: Keyword Analysis Dashobard")

numberOfScrape = st.slider("How many  times do  you wnat the keyword scraper to be ran?",1,5,1)
listOfKeywords = ["plumber","builder","accountant"]

col1,col2= st.columns(2)
with col1:
    selected_keywords = st_tags(
        lable="Add Keyword!"
        text="Press Enter To Adde Another Keyword"
        value=listOfKeywords 
    )