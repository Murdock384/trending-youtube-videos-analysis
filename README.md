# Final Project – README

**Student: David Abraham**
Student ID: 487868

## Project Description

This project analyzes YouTube trending videos across the United States, Canada, and Great Britain to identify key success factors and patterns that determine a video's success on YouTube.

The interactive Streamlit dashboard provides comprehensive insights into:

- **Engagement metrics and patterns**: How viewers interact with trending content through likes, comments, and dislikes
- **Optimal publishing strategies**: Best times and days to publish videos for maximum trending potential
- **Category performance differences**: Which video categories dominate the trending page and achieve the highest engagement
- **Correlation analysis**: Relationships between views, engagement rate, title length, tag counts, and virality
- **Performance classification**: Videos are categorized as Explosive (top 10% views + fastest 25% trending), High-Performing (top 25% views OR fast trending), or Standard Trending based on reach and speed-to-trending

The analysis combines data from 100,000+ trending videos to uncover actionable insights. Key findings include: Music videos achieve the highest average views but lowest engagement rates (passive consumption); explosive viral growth requires both massive reach AND rapid trending speed within 4 days median; early morning publishing (5 AM UTC) correlates with higher views; and engagement rate shows negative correlation with view counts, indicating that viral videos often have lower interaction rates due to passive viewing behaviors.

The dashboard features interactive Plotly visualizations with dynamic country and category filtering, allowing users to explore cross-country performance comparisons, channel rankings, publishing time heatmaps, correlation matrices, and days-to-trending distributions. The project demonstrates data cleaning workflows, feature engineering techniques, SQLite database design with optimized indexes, and leveraging Streamlit to make a functinonal web app.

## Dataset

**Original dataset link:**  
https://www.kaggle.com/datasets/datasnaek/youtube-new

**Dataset Description:**  
The YouTube Trending Video Dataset contains daily records of trending videos across 10 countries. This project uses data from three Western English-speaking countries (United States, Canada, Great Britain) to ensure consistent analysis across similar markets.

**Note:**  
Dataset file names are kept exactly as in the original download.

## Requirements

- Python Python 3.13
- pip (Python package installer)
- IDE with jupyter notebook support like VSCode.
If you are using VSCode have not installed the jupyter extension please follow the pop up or 
https://code.visualstudio.com/docs/datascience/jupyter-notebooks

## How to Run

1. **Extract the project and create a virtual environment:**

   ```bash
   cd trending-youtube-videos-analysis-main
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # source venv/bin/activate  # On macOS/Linux
   ```

2. **Install dependencies inside the virtual environment:**

   ```bash
   pip install -r requirements.txt
   pip install ipykernel
   python -m ipykernel install --user --name=trending-youtube-venv --display-name "Python (trending-youtube-venv)"
   ```

   **Note:** The `ipykernel` commands make your virtual environment available as a kernel in VS Code's Jupyter notebook interface.

3. **Download the dataset from Kaggle:**

   - Visit: https://www.kaggle.com/datasets/datasnaek/youtube-new
   - Click "Download"
   - Extract the downloaded zip file
   - Place the extracted files in the `dataset/` folder in the project root where you should see files named like `USvideos.csv`, `US_category_id.json` and 10 different countries in total.

4. **Run the Jupyter notebook to process and clean the data:**

   - Open `src/data-handling-and-visualization.ipynb` in VS Code
   - Select the kernel: Click the kernel picker in the top-right corner and choose **"Python (trending-youtube-venv)"** which should be available under the Jupyter Kernels section.
   If this is not visible please try restarting the IDE

   - Execute all cells in the notebook (Run All or cell-by-cell)
   - This will create the `cleaned_data/` folder with 3 CSV files:
     - `cleaned_videos.csv` (~107,000 video records)
     - `categories.csv` (18 categories)
     - `channel_stats.csv` (aggregated channel statistics)

5. **Create the SQLite database:**
   To setup the database run the following command

   ```bash
   python database/create_database.py
   ```

   - This creates `database/youtube_trends.db` from the cleaned CSV files
   - Expected output: Database with 3 tables and 9 indexes

6. **Run the Streamlit dashboard:**
   ```bash
   streamlit run src/app.py
   ```
   - The app will automatically open in your browser at `http://localhost:8501`
   - If not, manually navigate to the URL shown in the terminal
