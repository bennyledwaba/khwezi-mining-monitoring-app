import streamlit as st
from modules.auth.login import login_page
from modules.dashboard.dashboard import render_dashboard

st.set_page_config(page_title="Khwezi Mining App", page_icon="⛏️", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""

if not st.session_state.logged_in:
    login_page()
else:
    render_dashboard()
