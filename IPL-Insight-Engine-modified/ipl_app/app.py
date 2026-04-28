"""
app.py — Entry point. Redirects to the correct page based on session state.
"""
import streamlit as st

st.set_page_config(
    page_title="IPL Orbital Explorer",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Always start at dataset page if no stats loaded
if "stats" not in st.session_state:
    st.switch_page("pages/1_dataset.py")
else:
    st.switch_page("pages/2_teams.py")
