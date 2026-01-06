import streamlit as st

def show():
    """Display the Home page with overview and navigation guide."""
    
    # Adding custom CSS for styling
    st.markdown("""
        <style>
        /* Style info boxes with black background */
        div[data-testid="stAlert"],
        div[data-testid="stAlert"] > div,
        div[data-baseweb="notification"] {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #444444 !important;
            max-width: 1000px !important;
            border-radius: 15px !important;
        }
        
        div[data-testid="stAlert"] p {
            color: #ffffff !important;
        }
        
        div[data-testid="stAlert"] ul {
            color: #ffffff !important;
        }
        
        div[data-testid="stAlert"] li {
            color: #ffffff !important;
        }
        
        div[data-testid="stAlert"] strong {
            color: #ffffff !important;
        }
        
        /* Override Streamlit's default info icon color */
        div[data-testid="stAlert"] svg {
            fill: #ffffff !important;
        }
        
        /* Additional background override for nested divs */
        [data-baseweb="notification"] > div {
            background-color: #000000 !important;
            border-radius: 15px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<div class="main-header"><img src="https://cdn.prod.website-files.com/67fc891ab50af9421bac781e/6823e636ff9ecb8cb9e9eede_6553ed7e-f32b-43ea-9ea5-2932959ed491.avif" alt="YouTube Icon">YouTube Trending Videos Analysis</div>', unsafe_allow_html=True)
    st.markdown("## Research Question: What patterns and factors determine a video's success on YouTube?")
    
    st.markdown("---")
    
    # Page Guide
    st.markdown("## Page Guide")
    
    st.markdown("###  1. Analysis Page")
    st.info("""
    **What you'll find:**
    - **Cross-Country Performance Analysis** comparing US, CA, and GB
    - **Category Performance Insights** across different video types
    - **Correlation Analysis** between engagement metrics
    - **Publishing Time Optimization** recommendations
    - **Performance Classification** of videos by views and engagement
    - **Top Performing Channels** and viral video patterns
    - **Title and Tag Impact Analysis**
    - **Key Findings Summary** with actionable insights
    
    **Best for:** Understanding trends, patterns, and success factors
    """)
    
    st.markdown("###  2. Database Tables Page")
    st.info("""
    **What you'll find:**
    - **Categories Table** - mapping of video category IDs to names
    - **Channel Stats Table** - aggregated statistics for top channels
    - **Videos Table** - detailed information on all trending videos
    - **Table Schemas** showing database structure
    
    **Best for:** Exploring raw data and performing custom analysis
    """)
    
    st.markdown("---")
    
    # Dataset Information
    st.markdown("## Dataset Information")
    
    st.markdown("""
    This analysis uses a cleaned subset of the **YouTube Trending Videos Dataset** sourced from 
    [Kaggle](https://www.kaggle.com/datasets/datasnaek/youtube-new). The original dataset contains 
    trending video data from multiple countries. For this project, we focused on three major English-speaking 
    markets: **United States (US)**, **Great Britain (GB)**, and **Canada (CA)** to get some focused insights. 
    
    The data was cleaned and processed to ensure quality and consistency, removing duplicates, handling 
    missing values, and creating derived metrics such as engagement rates and days to trending. The final 
    dataset includes over **100,000 trending videos** across **15+ video categories** including Entertainment, 
    Music, News, Gaming, Sports, and more.
    """)
    
    st.markdown("---")
    
    # Getting Started
    st.markdown("## Getting Started")
    
    st.info("""
    **Use the sidebar navigation** to switch between pages:
    - Start with **Analysis** to explore insights and visualizations
    - Visit **Database Tables** to examine the raw data
    - Use filters on each page to customize your view
    """)
    
# Calling the show function to display the page
show()
