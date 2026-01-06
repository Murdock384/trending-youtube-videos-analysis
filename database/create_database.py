"""
Database Setup Script

This script creates a SQLite database from the cleaned CSV files.
It creates tables optimized for Streamlit dashboard queries.

Tables:
    - categories: Video category reference data
    - channel_stats: Aggregated channel performance metrics
    - videos: Main fact table with all video data
"""

import sqlite3
import pandas as pd
import os

from pathlib import Path

# Define paths
BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_DATA_DIR = BASE_DIR / 'cleaned_data'
DB_PATH = BASE_DIR / 'database' / 'youtube_trends.db'

def create_database():
    """Create SQLite database and tables from CSV files."""
    
    print("="*80)
    print("YOUTUBE TRENDS DATABASE SETUP")
    print("="*80)
    
    # Remove existing database if it exists
    if DB_PATH.exists():
        print(f"\nRemoving existing database: {DB_PATH}")
        os.remove(DB_PATH)
    
    # Create database directory if it doesn't exist
    DB_PATH.parent.mkdir(exist_ok=True)
    
    # Connect to database
    print(f"\nCreating new database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")
    
    print("\n" + "="*80)
    print("STEP 1: Creating Tables")
    print("="*80)
    
  
    # TABLE 1: Categories (Dimension Table)
    print("\nCreating 'categories' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY,
            category_name TEXT NOT NULL UNIQUE
        )
    """)
    
    
    # TABLE 2: Channel Stats (Aggregated Dimension)
    print("Creating 'channel_stats' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channel_stats (
            channel_title TEXT PRIMARY KEY,
            video_count INTEGER NOT NULL,
            total_views INTEGER NOT NULL,
            avg_views REAL NOT NULL,
            avg_engagement REAL NOT NULL
        )
    """)
    

    # TABLE 3: Videos (Main Fact Table)
    print("Creating 'videos' table...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT NOT NULL,
            trending_date TEXT NOT NULL,
            title TEXT,
            channel_title TEXT,
            category_id INTEGER,
            publish_time TEXT,
            tags TEXT,
            views INTEGER,
            likes INTEGER,
            dislikes INTEGER,
            comment_count INTEGER,
            thumbnail_link TEXT,
            comments_disabled INTEGER,
            ratings_disabled INTEGER,
            video_error_or_removed INTEGER,
            description TEXT,
            country TEXT,
            engagement_rate REAL,
            like_ratio REAL,
            comment_rate REAL,
            dislike_ratio REAL,
            days_to_trending REAL,
            publish_hour INTEGER,
            publish_day_of_week INTEGER,
            publish_month INTEGER,
            title_length INTEGER,
            description_length INTEGER,
            tag_count INTEGER,
            performance_class TEXT,
            PRIMARY KEY (video_id, trending_date, country),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """)
    
    conn.commit()
    
    print("\n" + "="*80)
    print("STEP 2: Loading Data from CSV Files")
    print("="*80)
    

    print("\nLoading categories...")
    categories_df = pd.read_csv(CLEANED_DATA_DIR / 'categories.csv')
    # Remove duplicates (same category may appear for different countries)
    categories_df = categories_df.drop_duplicates(subset=['category_id'], keep='last')
    categories_df.to_sql('categories', conn, if_exists='append', index=False)
    print(f"   Loaded {len(categories_df)} unique categories")
    
 
    print("\nLoading channel statistics...")
    channel_stats_df = pd.read_csv(CLEANED_DATA_DIR / 'channel_stats.csv')
    channel_stats_df = channel_stats_df.drop_duplicates(subset=['channel_title'])
    channel_stats_df.to_sql('channel_stats', conn, if_exists='append', index=False)
    print(f"   Loaded {len(channel_stats_df):,} unique channels")
    
    print("\nLoading video data (this may take a minute)...")
    chunk_size = 10000
    total_rows = 0
    first_chunk = True
    
    for chunk in pd.read_csv(CLEANED_DATA_DIR / 'cleaned_videos.csv', chunksize=chunk_size):
        # Validate and log column info on first chunk
        if first_chunk:
            print(f"\n   CSV columns found: {len(chunk.columns)}")
            print(f"   Expected columns: 29")
            extra_cols = set(chunk.columns) - {'video_id', 'trending_date', 'title', 'channel_title', 'category_id',
                                                'publish_time', 'tags', 'views', 'likes', 'dislikes', 'comment_count',
                                                'thumbnail_link', 'comments_disabled', 'ratings_disabled',
                                                'video_error_or_removed', 'description', 'country',
                                                'engagement_rate', 'like_ratio', 'comment_rate', 'dislike_ratio',
                                                'days_to_trending', 'publish_hour', 'publish_day_of_week',
                                                'publish_month', 'title_length', 'description_length',
                                                'tag_count', 'performance_class'}
            if extra_cols:
                print(f"   Warning: Dropping extra columns: {', '.join(extra_cols)}")
            first_chunk = False
        
        # Drop columns not in database schema
        chunk = chunk.drop(columns=['category_name', 'title_length_category'], errors='ignore')
        chunk.to_sql('videos', conn, if_exists='append', index=False)
        total_rows += len(chunk)
        print(f"   Loaded {total_rows:,} videos...", end='\r')
    
    print(f"\n   Loaded {total_rows:,} total videos")
    
    print("\n" + "="*80)
    print("STEP 3: Creating Indexes for Query Performance")
    print("="*80)
    
    # Create indexes for common query patterns
    indexes = [
        ("idx_videos_country", "videos(country)"),
        ("idx_videos_category", "videos(category_id)"),
        ("idx_videos_channel", "videos(channel_title)"),
        ("idx_videos_performance", "videos(performance_class)"),
        ("idx_videos_views", "videos(views)"),
        ("idx_videos_trending_date", "videos(trending_date)"),
        ("idx_videos_publish_time", "videos(publish_time)"),
        ("idx_videos_publish_hour", "videos(publish_hour)"),
        ("idx_videos_publish_day", "videos(publish_day_of_week)"),
    ]
    
    for idx_name, idx_def in indexes:
        print(f"Creating index: {idx_name}")
        cursor.execute(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {idx_def}")
    
    conn.commit()
    
    print("\n" + "="*80)
    print("STEP 4: Database Statistics & Validation")
    print("="*80)
    
    # Get table counts
    tables_info = []
    
    cursor.execute("SELECT COUNT(*) FROM categories")
    cat_count = cursor.fetchone()[0]
    tables_info.append(("categories", cat_count))
    
    cursor.execute("SELECT COUNT(*) FROM channel_stats")
    channel_count = cursor.fetchone()[0]
    tables_info.append(("channel_stats", channel_count))
    
    cursor.execute("SELECT COUNT(*) FROM videos")
    video_count = cursor.fetchone()[0]
    tables_info.append(("videos", video_count))
    
    print("\nTable Row Counts:")
    for table, count in tables_info:
        print(f"   {table:20s}: {count:,} rows")
    
    # Sample queries to validate
    print("\nSample Validation Queries:")
    
    # Query 1: Videos by country
    print("\n   1. Videos by Country:")
    cursor.execute("""
        SELECT country, COUNT(*) as count 
        FROM videos 
        GROUP BY country 
        ORDER BY count DESC
    """)
    for row in cursor.fetchall():
        print(f"      {row[0]}: {row[1]:,} videos")
    
    # Query 2: Top 5 categories
    print("\n   2. Top 5 Categories by Video Count:")
    cursor.execute("""
        SELECT c.category_name, COUNT(*) as count
        FROM videos v
        JOIN categories c ON v.category_id = c.category_id
        GROUP BY c.category_name
        ORDER BY count DESC
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"      {row[0]}: {row[1]:,} videos")
    
    # Query 3: Performance class distribution
    print("\n   3. Performance Class Distribution:")
    cursor.execute("""
        SELECT performance_class, COUNT(*) as count
        FROM videos
        GROUP BY performance_class
        ORDER BY count DESC
    """)
    for row in cursor.fetchall():
        print(f"      {row[0]}: {row[1]:,} videos")
    
    # Query 4: Date range
    print("\n   4. Data Date Range:")
    cursor.execute("""
        SELECT 
            MIN(trending_date) as earliest,
            MAX(trending_date) as latest
        FROM videos
    """)
    earliest, latest = cursor.fetchone()
    print(f"      Earliest: {earliest}")
    print(f"      Latest: {latest}")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*80)
    print("DATABASE SETUP COMPLETE!")
    print("="*80)
    print(f"\nDatabase location: {DB_PATH}")
    print(f"Database size: {DB_PATH.stat().st_size / 1024 / 1024:.2f} MB")
    print("\nReady for Streamlit dashboard queries!")
    print("="*80)

if __name__ == "__main__":
    try:
        create_database()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
