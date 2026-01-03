# YouTube Trending Videos Analysis Dashboard

An interactive Streamlit dashboard analyzing YouTube trending videos across the United States, Canada, and Great Britain to identify key success factors and patterns.

## Research Question

**What patterns and factors determine a video's success on YouTube?**

This project analyzes trending YouTube videos to understand:

- Engagement metrics and patterns
- Optimal publishing strategies
- Category performance differences
- Factors correlating with video success

## Features

- **Interactive Visualizations**: 11 Plotly charts with zoom, pan, and hover capabilities
- **Dynamic Filtering**: Filter by country and category to explore specific markets
- **Comprehensive Analysis**:
  - Cross-country performance comparison
  - Category performance rankings
  - Correlation analysis of key metrics
  - Publishing time optimization
  - Engagement patterns
  - Channel rankings
  - Days-to-trending analysis
  - Title length impact
  - Tag count effectiveness
- **Key Findings**: 7 data-driven insights with expandable sections

## Live Demo

**Streamlit Cloud:**: https://trending-youtube-videos-analysis.streamlit.app

## Local Setup

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd trending-youtube-videos-analysis
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard:**

   ```bash
   streamlit run src/app.py
   ```

4. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

## Project Structure

```
trending-youtube-videos-analysis/
├── src/
│   ├── app.py                              # Main Streamlit application
│   ├── db_utils.py                         # Database query utilities
│   └── data-handling-and-visualization.ipynb  # Jupyter analysis notebook
├── database/
│   ├── youtube_trends.db                   # SQLite database
│   └── create_database.py                  # Database creation script
├── dataset/                                # Raw CSV and JSON files
├── cleaned_data/                           # Processed CSV files
├── requirements.txt                        # Python dependencies
└── README.md                               # This file
```

## Database Schema

**SQLite Database:** `database/youtube_trends.db`

### Tables

1. **categories** - Category ID to name mapping
2. **channel_stats** - Aggregated channel-level statistics
3. **videos** - Main fact table with 29 columns including:
   - Video metadata (id, title, channel, category, country)
   - Engagement metrics (views, likes, dislikes, comments)
   - Derived features (engagement_rate, like_ratio, days_to_trending)
   - Time dimensions (publish_hour, publish_day_of_week, publish_month)
   - Performance classification (Explosive, High-Performing, Standard Trending)


## Data Source

- **YouTube Trending Dataset** (Kaggle)
- **Countries:** United States, Canada, Great Britain
- **Categories:** 18 unique categories
- **Time Period:** Historical trending data
- **Total Videos:** 100,000+ trending videos analyzed

## Analysis Workflow

1. **Data Collection** - Raw CSV files from Kaggle
2. **Data Cleaning** - Handle missing values, duplicates, type conversions
3. **Feature Engineering** - Calculate engagement metrics, time features, performance classes
4. **Database Creation** - Load into SQLite with indexes
5. **Exploratory Analysis** - Jupyter notebook analysis
6. **Dashboard Development** - Interactive Streamlit app
7. **Deployment** - Streamlit Cloud hosting


## License

This project is for educational purposes. Dataset sourced from publicly available YouTube trending data.
