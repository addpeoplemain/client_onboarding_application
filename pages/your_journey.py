import streamlit as st
from streamlit_tags import st_tags
from streamlit_extras.stylable_container import stylable_container 


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
         
         Onboarding Application 1.0

            """
         )


st.title("Your Journey With Add People")

with stylable_container(
    key="onboarding",
    css_styles="""
        {
            margin: auto;
            width: 50%;
        }
    """,
):

    st.header("Onboarding")
st.divider()
with stylable_container(
    key="container_client_lead_deal",
    css_styles="""
        {
            margin: auto;
            width: 50%;
        }
    """,
):
    st.subheader("Day 2-3 : Welcome Call Booking")
    st.subheader("Day 4-8 : Welcome Call Delivery")
    st.subheader("Day 5-18 : Processes")
    st.subheader("Day 16-19 : Launch Call")
    st.subheader("Day 30-40 : Review Call")
    st.subheader("Day 40+ : Comms")
    st.subheader("Day 40+ : Tech")



