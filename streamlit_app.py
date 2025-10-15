"""
Streamlit Cloud Entry Point
This file serves as the entry point for Streamlit Community Cloud deployment.
It imports and runs the main application from the app directory.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Import and run the main application
from main import create_streamlit_app
import streamlit as st

if __name__ == "__main__":
    # Set page config for Streamlit Cloud
    st.set_page_config(
        layout="wide", 
        page_title="Cold Email AI Agent", 
        page_icon="🤖",
        initial_sidebar_state="collapsed"
    )
    
    # Run the main application
    create_streamlit_app()