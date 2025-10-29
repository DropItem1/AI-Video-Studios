import os
import streamlit as st
import streamlit.components.v1 as components

st.title("🎨 3D Bouncing Ball in Streamlit")

# Get absolute path to this script's folder
base_path = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(base_path, "index.html")

# Load HTML file safely
try:
    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    components.html(html_content, height=600, scrolling=True)
except FileNotFoundError:
    st.error(f"Could not find index.html at: {html_path}")
