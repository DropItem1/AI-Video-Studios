import streamlit as st
import streamlit.components.v1 as components

st.title("🎨 3D Bouncing Ball in Streamlit")

# Open your HTML file
with open("index.html", "r") as f:
    html_content = f.read()

# Embed the HTML
components.html(html_content, height=600, scrolling=True)
