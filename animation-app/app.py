import streamlit as st
import streamlit.components.v1 as components

st.title("🎨 3D Bouncing Ball")

# Load HTML
with open("index.html", "r") as f:
    html_content = f.read()

# Embed in Streamlit
components.html(html_content, height=600, scrolling=True)
