import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from database import db_utils as db

def show():
    """Display the Database Tables page with all SQL tables."""
    
    # Add custom CSS for selectbox styling
    st.markdown("""
        <style>
        /* Style selectbox to be shorter and have black background */
        div[data-baseweb="select"] {
            max-width: 300px;
        }
        
        div[data-baseweb="select"] > div {
            background-color: #000000;
            border: 1px solid #444444;
        }
        
        /* Dropdown menu styling */
        div[data-baseweb="popover"] {
            background-color: #000000;
        }
        
        ul[role="listbox"] {
            background-color: #000000;
        }
        
        li[role="option"] {
            background-color: #000000;
            color: #ffffff;
        }
        
        li[role="option"]:hover {
            background-color: #333333;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""# <svg xmlns="http://www.w3.org/2000/svg" width="45" height="45" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-database-zap-icon lucide-database-zap"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 15 21.84"/><path d="M21 5V8"/><path d="M21 12L18 17H22L19 22"/><path d="M3 12A9 3 0 0 0 14.59 14.87"/></svg> Database Tables
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ##### This page displays the raw data from the YouTube Trends Database highlighting the SQL Integration of this project via SQLite. 
    ##### Use this to explore the underlying data that powers the analytics on the Analysis page. 
    """
    )
    
    # ============================================================================
    # CATEGORIES TABLE
    # ============================================================================
    st.markdown("### <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#f0f0f0' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='lucide lucide-boxes' style='display: inline-block; vertical-align: -3px; margin-right: 8px;'><path d='M2.97 12.92A2 2 0 0 0 2 14.63v3.24a2 2 0 0 0 .97 1.71l3 1.8a2 2 0 0 0 2.06 0L12 19v-5.5l-5-3-4.03 2.42Z'/><path d='m7 16.5-4.74-2.85'/><path d='m7 16.5 5-3'/><path d='M7 16.5v5.17'/><path d='M12 13.5V19l3.97 2.38a2 2 0 0 0 2.06 0l3-1.8a2 2 0 0 0 .97-1.71v-3.24a2 2 0 0 0-.97-1.71L17 10.5l-5 3Z'/><path d='m17 16.5-5-3'/><path d='m17 16.5 4.74-2.85'/><path d='M17 16.5v5.17'/><path d='M7.97 4.42A2 2 0 0 0 7 6.13v4.37l5 3 5-3V6.13a2 2 0 0 0-.97-1.71l-3-1.8a2 2 0 0 0-2.06 0l-3 1.8Z'/><path d='M12 8 7.26 5.15'/><path d='m12 8 4.74-2.85'/><path d='M12 13.5V8'/></svg> Categories Table", unsafe_allow_html=True)
    st.markdown("*Mapping of category IDs to category names*")
    
    try:
        categories_df = db.get_categories_table()
        st.dataframe(categories_df, use_container_width=True)
        st.caption(f"**Total categories:** {len(categories_df)}")
    except Exception as e:
        st.error(f"Error loading categories table: {e}")
    
    st.markdown("---")
    
    # ============================================================================
    # CHANNEL_STATS TABLE
    # ============================================================================
    st.markdown("### <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#f0f0f0' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='lucide lucide-tv-minimal' style='display: inline-block; vertical-align: -3px; margin-right: 8px;'><path d='M7 21h10'/><rect width='20' height='14' x='2' y='3' rx='2'/></svg> Channel Stats Table", unsafe_allow_html=True)
    st.markdown("*Aggregated statistics for top-performing channels*")
    
    try:
        channel_stats_df = db.get_channel_stats_table(limit=50)
        st.dataframe(channel_stats_df, use_container_width=True)
        
        total_channels = db.get_channel_stats_count()
        st.caption(f"**Showing top 50 channels** | Total channels: {total_channels}")
    except Exception as e:
        st.error(f"Error loading channel_stats table: {e}")
    
    st.markdown("---")
    
    # ============================================================================
    # VIDEOS TABLE
    # ============================================================================
    st.markdown("### <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='#f0f0f0' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' class='lucide lucide-clapperboard' style='display: inline-block; vertical-align: -3px; margin-right: 8px;'><path d='M20.2 6 3 11l-.9-2.4c-.3-1.1.3-2.2 1.3-2.5l13.5-4c1.1-.3 2.2.3 2.5 1.3Z'/><path d='m6.2 5.3 3.1 3.9'/><path d='m12.4 3.4 3.1 4'/><path d='M3 11h18v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z'/></svg> Videos Table", unsafe_allow_html=True)
    st.markdown("*Detailed information about trending videos*")
    
    # Add filter options for videos table
    country_filter_table = st.selectbox(
        "Filter by Country:",
        ["All", "US", "CA", "GB"],
        key="table_country_filter"
    )
    
    try:
        videos_df = db.get_videos_table(country_filter=country_filter_table, limit=100)
        st.dataframe(videos_df, use_container_width=True, height=600)
        
        total_videos = db.get_videos_count()
        filtered_count = db.get_videos_count(country_filter=country_filter_table)
        
        st.caption(f"**Showing top 100 of {filtered_count:,} videos** | Total videos in database: {total_videos:,}")
    except Exception as e:
        st.error(f"Error loading videos table: {e}")
    
    st.markdown("---")
    
    # ============================================================================
    # TABLE SCHEMA INFORMATION
    # ============================================================================
    with st.expander(" View Table Schemas"):
        st.markdown("### Categories Table Schema")
        st.code("""
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT NOT NULL
        )
        """, language="sql")
        
        st.markdown("### Channel Stats Table Schema")
        st.code("""
        CREATE TABLE channel_stats (
            channel_title TEXT PRIMARY KEY,
            total_views INTEGER,
            total_videos INTEGER,
            avg_views_per_video DOUBLE,
            avg_engagement_rate DOUBLE
        )
        """, language="sql")
        
        st.markdown("### Videos Table Schema")
        st.code("""
        CREATE TABLE videos (
            video_id TEXT,
            trending_date DATE,
            title TEXT,
            channel_title TEXT,
            category_id INTEGER,
            publish_time TIMESTAMP,
            tags TEXT,
            views INTEGER,
            likes INTEGER,
            dislikes INTEGER,
            comment_count INTEGER,
            thumbnail_link TEXT,
            comments_disabled BOOLEAN,
            ratings_disabled BOOLEAN,
            video_error_or_removed BOOLEAN,
            description TEXT,
            country TEXT,
            engagement_rate DOUBLE,
            days_to_trending INTEGER,
            publish_hour INTEGER,
            publish_day_of_week INTEGER,
            title_length INTEGER,
            tag_count INTEGER,
            PRIMARY KEY (video_id, trending_date, country),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
        """, language="sql")


# Call the show function to display the page
show()
