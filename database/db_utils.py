"""
Database utility functions for YouTube Trends Streamlit Dashboard
Handles SQLite connections and cached data queries
"""

import sqlite3
import pandas as pd
import streamlit as st
from pathlib import Path


def get_db_path():
    """Get database path relative to this file"""
    current_dir = Path(__file__).parent
    db_path = current_dir.parent / 'database' / 'youtube_trends.db'
    return str(db_path)


@st.cache_data(ttl=3600)
def get_all_countries():
    """Get list of all countries in database"""
    conn = sqlite3.connect(get_db_path())
    query = "SELECT DISTINCT country FROM videos ORDER BY country"
    countries = pd.read_sql_query(query, conn)['country'].tolist()
    conn.close()
    return countries


@st.cache_data(ttl=3600)
def get_all_categories():
    """Get all categories from database"""
    conn = sqlite3.connect(get_db_path())
    query = """
        SELECT category_id, category_name 
        FROM categories 
        ORDER BY category_name
    """
    categories = pd.read_sql_query(query, conn)
    conn.close()
    return categories


@st.cache_data(ttl=3600)
def get_country_stats(countries=None):
    """
    Get aggregated statistics by country
    
    Parameters:
    countries (list): Filter by specific countries, None for all
    
    Returns:
    DataFrame: Country-level statistics
    """
    conn = sqlite3.connect(get_db_path())
    
    where_clause = ""
    if countries:
        country_list = "','".join(countries)
        where_clause = f"WHERE country IN ('{country_list}')"
    
    query = f"""
        SELECT 
            country,
            COUNT(DISTINCT video_id) as video_count,
            AVG(views) as avg_views,
            AVG(engagement_rate) as avg_engagement,
            AVG(days_to_trending) as avg_days_to_trending
        FROM videos
        {where_clause}
        GROUP BY country
        ORDER BY video_count DESC
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def get_category_stats(countries=None, categories=None):
    """
    Get aggregated statistics by category
    
    Parameters:
    countries (list): Filter by countries
    categories (list): Filter by category names
    
    Returns:
    DataFrame: Category-level statistics
    """
    conn = sqlite3.connect(get_db_path())
    
    where_clauses = []
    if countries:
        country_list = "','".join(countries)
        where_clauses.append(f"v.country IN ('{country_list}')")
    if categories:
        category_list = "','".join([cat.replace("'", "''") for cat in categories])
        where_clauses.append(f"c.category_name IN ('{category_list}')")
    
    where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    query = f"""
        SELECT 
            c.category_name,
            COUNT(v.video_id) as video_count,
            AVG(v.views) as avg_views,
            CAST(AVG(v.engagement_rate) as REAL) as avg_engagement,
            AVG(v.like_ratio) as avg_like_ratio
        FROM videos v
        JOIN categories c ON v.category_id = c.category_id
        {where_clause}
        GROUP BY c.category_name
        ORDER BY avg_views DESC
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def get_correlation_data(countries=None):
    """
    Get data for correlation matrix
    
    Parameters:
    countries (list): Filter by countries
    
    Returns:
    DataFrame: Correlation matrix data
    """
    conn = sqlite3.connect(get_db_path())
    
    where_clause = ""
    if countries:
        country_list = "','".join(countries)
        where_clause = f"WHERE country IN ('{country_list}')"
    
    query = f"""
        SELECT 
            views, likes, dislikes, comment_count,
            engagement_rate, like_ratio, title_length, tag_count
        FROM videos
        {where_clause}
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def get_publishing_time_heatmap(countries=None):
    """
    Get average views by day of week and hour
    
    Parameters:
    countries (list): Filter by countries
    
    Returns:
    DataFrame: Publishing time heatmap data
    """
    conn = sqlite3.connect(get_db_path())
    
    where_clause = ""
    if countries:
        country_list = "','".join(countries)
        where_clause = f"WHERE country IN ('{country_list}')"
    
    query = f"""
        SELECT 
            publish_day_of_week,
            publish_hour,
            AVG(views) as avg_views
        FROM videos
        {where_clause}
        GROUP BY publish_day_of_week, publish_hour
        ORDER BY publish_day_of_week, publish_hour
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def get_engagement_by_category(countries=None, top_n=10):
    """
    Get engagement distribution data for box plot
    
    Parameters:
    countries (list): Filter by countries
    top_n (int): Number of top categories to include
    
    Returns:
    DataFrame: Engagement data by category
    """
    conn = sqlite3.connect(get_db_path())
    
    where_clause = ""
    if countries:
        country_list = "','".join(countries)
        where_clause = f"WHERE v.country IN ('{country_list}')"
    
    # First get top N categories
    top_categories_query = f"""
        SELECT c.category_name, COUNT(*) as count
        FROM videos v
        JOIN categories c ON v.category_id = c.category_id
        {where_clause}
        GROUP BY c.category_name
        ORDER BY count DESC
        LIMIT {top_n}
    """
    
    top_cats = pd.read_sql_query(top_categories_query, conn)['category_name'].tolist()
    
    # Get engagement data for top categories
    cat_list = "','".join([cat.replace("'", "''") for cat in top_cats])
    
    additional_where = f"c.category_name IN ('{cat_list}')"
    if where_clause:
        where_clause += f" AND {additional_where}"
    else:
        where_clause = f"WHERE {additional_where}"
    
    query = f"""
        SELECT 
            c.category_name,
            v.engagement_rate
        FROM videos v
        JOIN categories c ON v.category_id = c.category_id
        {where_clause}
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def get_views_engagement_scatter(countries=None, sample_size=4000):
    """
    Get sample data for views vs engagement scatter plot
    
    Parameters:
    countries (list): Filter by countries
    sample_size (int): Number of random samples
    
    Returns:
    DataFrame: Sample data with performance classification
    """
    conn = sqlite3.connect(get_db_path())
    
    where_clause = ""
    if countries:
        country_list = "','".join(countries)
        where_clause = f"WHERE country IN ('{country_list}')"
    
    query = f"""
        SELECT 
            views, engagement_rate, performance_class
        FROM videos
        {where_clause}
        ORDER BY RANDOM()
        LIMIT {sample_size}
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def get_likes_dislikes_data(countries=None, sample_size=3000):
    """
    Get sample data for likes vs dislikes scatter
    
    Parameters:
    countries (list): Filter by countries
    sample_size (int): Number of random samples
    
    Returns:
    DataFrame: Likes and dislikes data
    """
    conn = sqlite3.connect(get_db_path())
    
    where_clause = ""
    if countries:
        country_list = "','".join(countries)
        where_clause = f"WHERE country IN ('{country_list}')"
    
    query = f"""
        SELECT likes, dislikes
        FROM videos
        {where_clause}
        ORDER BY RANDOM()
        LIMIT {sample_size}
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def get_top_channels(countries=None, top_n=20):
    """
    Get top channels by total views
    
    Parameters:
    countries (list): Filter by countries
    top_n (int): Number of top channels
    
    Returns:
    DataFrame: Top channels with total views
    """
    conn = sqlite3.connect(get_db_path())
    
    where_clause = ""
    if countries:
        country_list = "','".join(countries)
        where_clause = f"WHERE country IN ('{country_list}')"
    
    query = f"""
        SELECT 
            channel_title,
            SUM(views) as total_views
        FROM videos
        {where_clause}
        GROUP BY channel_title
        ORDER BY total_views DESC
        LIMIT {top_n}
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def get_days_to_trending(countries=None):
    """
    Get days to trending distribution
    
    Parameters:
    countries (list): Filter by countries
    
    Returns:
    DataFrame: Days to trending data
    """
    conn = sqlite3.connect(get_db_path())
    
    where_clause = "WHERE days_to_trending BETWEEN 0 AND 30"
    if countries:
        country_list = "','".join(countries)
        where_clause += f" AND country IN ('{country_list}')"
    
    query = f"""
        SELECT days_to_trending
        FROM videos
        {where_clause}
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def get_title_length_analysis(countries=None):
    """
    Get title length impact on views
    
    Parameters:
    countries (list): Filter by countries
    
    Returns:
    DataFrame: Title length statistics
    """
    conn = sqlite3.connect(get_db_path())
    
    where_clause = ""
    if countries:
        country_list = "','".join(countries)
        where_clause = f"WHERE country IN ('{country_list}')"
    
    query = f"""
        SELECT 
            CASE 
                WHEN title_length < 30 THEN 'Short (<30)'
                WHEN title_length < 60 THEN 'Medium (30-60)'
                ELSE 'Long (60+)'
            END as title_category,
            AVG(views) as avg_views,
            COUNT(*) as video_count
        FROM videos
        {where_clause}
        GROUP BY title_category
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Ensure correct order
    category_order = ['Short (<30)', 'Medium (30-60)', 'Long (60+)']
    df['title_category'] = pd.Categorical(df['title_category'], categories=category_order, ordered=True)
    df = df.sort_values('title_category')
    
    return df


@st.cache_data(ttl=3600)
def get_tag_analysis(countries=None):
    """
    Get tag count impact on performance
    
    Parameters:
    countries (list): Filter by countries
    
    Returns:
    DataFrame: Tag count analysis
    """
    conn = sqlite3.connect(get_db_path())
    
    where_clause = "WHERE tag_count <= 50"
    if countries:
        country_list = "','".join(countries)
        where_clause += f" AND country IN ('{country_list}')"
    
    query = f"""
        SELECT 
            tag_count,
            AVG(views) as avg_views,
            AVG(engagement_rate) as avg_engagement,
            COUNT(*) as video_count
        FROM videos
        {where_clause}
        GROUP BY tag_count
        HAVING COUNT(*) >= 10
        ORDER BY tag_count
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def get_overall_stats(countries=None):
    """
    Get overall statistics for dashboard overview
    
    Parameters:
    countries (list): Filter by countries
    
    Returns:
    dict: Overall statistics
    """
    conn = sqlite3.connect(get_db_path())
    
    where_clause = ""
    if countries:
        country_list = "','".join(countries)
        where_clause = f"WHERE country IN ('{country_list}')"
    
    query = f"""
        SELECT 
            COUNT(DISTINCT video_id) as total_videos,
            COUNT(DISTINCT channel_title) as unique_channels,
            COUNT(DISTINCT country) as countries,
            AVG(views) as avg_views,
            AVG(engagement_rate) as avg_engagement,
            AVG(days_to_trending) as avg_days_trending
        FROM videos
        {where_clause}
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    return df.iloc[0].to_dict()


# ============================================================================
# DATABASE TABLE DISPLAY FUNCTIONS
# ============================================================================

@st.cache_data(ttl=3600)
def get_categories_table():
    """Get all categories from the database, ordered by category_id."""
    conn = sqlite3.connect(get_db_path())
    query = "SELECT * FROM categories ORDER BY category_id"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def get_channel_stats_table(limit=50):
    """Get channel stats table, ordered by total views descending.
    
    Args:
        limit (int): Maximum number of channels to return
        
    Returns:
        pd.DataFrame: Channel statistics
    """
    conn = sqlite3.connect(get_db_path())
    query = f"SELECT * FROM channel_stats ORDER BY total_views DESC LIMIT {limit}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


@st.cache_data(ttl=3600)
def get_channel_stats_count():
    """Get total count of channels in channel_stats table."""
    conn = sqlite3.connect(get_db_path())
    query = "SELECT COUNT(*) as count FROM channel_stats"
    count = pd.read_sql_query(query, conn)['count'].iloc[0]
    conn.close()
    return count


@st.cache_data(ttl=3600)
def get_videos_table(country_filter=None, limit=100):
    """Get videos table with optional country filter.
    
    Args:
        country_filter (str, optional): Country code to filter by (e.g., 'US', 'CA')
        limit (int): Maximum number of videos to return
        
    Returns:
        pd.DataFrame: Video data with formatted columns
    """
    conn = sqlite3.connect(get_db_path())
    
    query = """
        SELECT 
            video_id,
            title,
            channel_title,
            category_id,
            country,
            views,
            likes,
            dislikes,
            comment_count,
            engagement_rate,
            trending_date,
            publish_time,
            days_to_trending
        FROM videos
    """
    
    if country_filter and country_filter != "All":
        query += f" WHERE country = '{country_filter}'"
    
    query += f" ORDER BY views DESC LIMIT {limit}"
    
    videos_df = pd.read_sql_query(query, conn)
    conn.close()
    
    # Format the dataframe for better display
    if not videos_df.empty:
        # Format numbers with commas
        for col in ['views', 'likes', 'dislikes', 'comment_count']:
            if col in videos_df.columns:
                videos_df[col] = videos_df[col].apply(lambda x: f"{int(x):,}" if pd.notna(x) else "")
        
        # Format engagement_rate as percentage
        if 'engagement_rate' in videos_df.columns:
            videos_df['engagement_rate'] = videos_df['engagement_rate'].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "")
        
        # Format dates
        for col in ['trending_date', 'publish_time']:
            if col in videos_df.columns:
                videos_df[col] = pd.to_datetime(videos_df[col]).dt.strftime('%Y-%m-%d')
    
    return videos_df


@st.cache_data(ttl=3600)
def get_videos_count(country_filter=None):
    """Get count of videos with optional country filter.
    
    Args:
        country_filter (str, optional): Country code to filter by
        
    Returns:
        int: Number of videos matching filter
    """
    conn = sqlite3.connect(get_db_path())
    
    query = "SELECT COUNT(*) as count FROM videos"
    if country_filter and country_filter != "All":
        query += f" WHERE country = '{country_filter}'"
    
    count = pd.read_sql_query(query, conn)['count'].iloc[0]
    conn.close()
    return count
