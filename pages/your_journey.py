import streamlit as st
from streamlit_tags import st_tags


st.title("Add People")
st.header("Your Journey With Add People")

st.subheader("Sales Call")
st.subheader("Onboarding")
st.write("Day 2-3 : Welcome Call Booking")
st.write("Day 2-3 : Welcome Call Delivery")
st.write("Day 2-3 : Welcome Call Delivery")

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
                 
         **Keyword Competitor Analysis 1.0**
         
         Onboarding Application 1.0
                 
        

            """
         )



