"""
Alternative entry point for Streamlit deployment
"""
import sys
import os
sys.path.append('app')
from main import create_streamlit_app
import streamlit as st

st.set_page_config(
    layout="wide", 
    page_title="Cold Email AI Agent", 
    page_icon="🤖",
    initial_sidebar_state="collapsed"
)

create_streamlit_app()