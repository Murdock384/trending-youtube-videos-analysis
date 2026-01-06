"""
This script sets up the Streamlit application for YouTube Trending Videos Analysis.
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="YouTube Trends Analysis",
    page_icon="<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"#f0f0f0\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" class=\"lucide lucide-file-chart-column-increasing-icon lucide-file-chart-column-increasing\"><path d=\"M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z\"/><path d=\"M14 2v5a1 1 0 0 0 1 1h5\"/><path d=\"M8 18v-2\"/><path d=\"M12 18v-4\"/><path d=\"M16 18v-6\"/></svg>",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Import Roboto font */
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Apply Roboto globally */
    * {
        font-family: 'Roboto', sans-serif;
    }
    
    /* Global background and text colors */
    .main {
        background-color: #282828;
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }
    
    .stApp {
        background-color: #282828;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Streamlit header bar */
    header[data-testid="stHeader"] {
        background-color: #282828;
    }
    
    /* Toolbar */
    .stToolbar {
        background-color: #282828;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #ffffff;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        padding: 2rem 0 1rem 0;
        margin-top: 1rem;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
    }
    
    .main-header img {
        height: 80px;
        vertical-align: middle;
        border-radius: 12px;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #ffffff;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    /* Text color overrides */
    .stMarkdown, .stMarkdown p, .stMarkdown li {
        color: #ffffff;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Metric cards */
    div[data-testid="stMetricValue"] {
        color: #ff0000;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #ffffff;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #3a3a3a;
        color: #ffffff;
        border-left: 4px solid #ff0000;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #3a3a3a;
        color: #ffffff;
        border-left: 4px solid #ff0000;
    }
    
    .streamlit-expanderContent {
        background-color: #3a3a3a;
        color: #ffffff;
    }
    
    /* Multiselect and input styling */
    .stMultiSelect label, .stSelectbox label {
        color: #ffffff;
    }
    
    /* Specific styling for hr inside markdown container */
    div[data-testid="stMarkdownContainer"] hr {
        border: none;
        border-top: 2px solid #ff0000;
        margin: 1rem 0;
    }
    
    /* Insights column styling */
    .insight-content {
        padding-left: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
pg = st.navigation([
    st.Page("pages/home.py", title="Home", default=True),
    st.Page("pages/analysis.py", title=" Analysis"),
    st.Page("pages/database_tables.py", title="Database Tables")
])

# Run the selected page
pg.run()
